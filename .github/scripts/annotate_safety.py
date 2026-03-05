#!/usr/bin/env python3
"""Annotate GitHub Actions step summary with Safety vulnerability scan results."""

import json
import os
import sys
from pathlib import Path


def write_summary(summary_file: str, lines: list[str]) -> None:
    with Path(summary_file).open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> None:
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY", os.devnull)
    report = Path("safety-output.json")

    if not report.exists() or report.stat().st_size == 0:
        write_summary(
            summary_file,
            [
                "### \U0001f512 Safety Vulnerability Scan",
                "",
                "\u26a0\ufe0f No safety report found or report was empty.",
            ],
        )
        sys.exit(0)

    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        write_summary(
            summary_file,
            [
                "### \U0001f512 Safety Vulnerability Scan",
                "",
                "\u26a0\ufe0f Could not parse safety-output.json.",
            ],
        )
        sys.exit(0)

    # Auth check: Safety 3.x sets meta.authenticated = False when no API key is present.
    # A missing key is a misconfigured security gate — fail the step so CI blocks the merge.
    if data.get("meta", {}).get("authenticated") is False:
        write_summary(
            summary_file,
            [
                "### 🔒 Safety Vulnerability Scan",
                "",
                "⚠️ Safety scan ran unauthenticated — `SAFETY_API_KEY` secret may be missing or expired.",
                "",
                "See [CI/CD Secrets](docs/DEPLOYMENT.md#cicd-secrets) for setup instructions.",
            ],
        )
        sys.exit(1)

    # Walk Safety 3.x schema:
    # scan_results -> projects[] -> files[] -> results -> dependencies[] -> specifications[]
    # -> vulnerabilities -> known_vulnerabilities[]
    # Use .get() + `or {}` safe-navigation at every nullable level to prevent KeyError
    # if Safety returns a partial response (e.g. zero projects or zero files scanned).
    vulns_found = []
    schema_reached = False
    for project in data.get("scan_results", {}).get("projects", []):
        for f in project.get("files", []):
            for dep in f.get("results", {}).get("dependencies", []):
                pkg_name = dep.get("name", "unknown")
                for spec in dep.get("specifications", []):
                    schema_reached = True
                    vuln_obj = spec.get("vulnerabilities") or {}
                    for v in vuln_obj.get("known_vulnerabilities", []):
                        vulns_found.append((pkg_name, v))

    # Safety 2.x fallback: flat top-level "vulnerabilities" key
    if not schema_reached:
        legacy = data.get("vulnerabilities")
        if legacy is not None:
            for v in legacy:
                pkg = v.get("package_name") or v.get("package", "unknown")
                vulns_found.append((pkg, v))
            schema_reached = True

    lines: list[str] = ["### 🔒 Safety Vulnerability Scan", ""]

    # Compute non_ignored before branching so it is always in scope for the exit check below.
    non_ignored = [(p, v) for p, v in vulns_found if not v.get("ignored")]

    if not schema_reached:
        lines.append("⚠️ Could not identify vulnerability list (unexpected schema).")
    elif not vulns_found:
        lines.append("✅ No vulnerabilities found.")
    else:
        ignored_count = len(vulns_found) - len(non_ignored)
        lines.append(
            f"❌ **{len(non_ignored)} active vulnerability(s) found** ({ignored_count} ignored by policy)"
        )
        lines.append("")
        lines.append("| Package | Vuln ID | Affected Spec | Ignored |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for pkg_name, v in vulns_found:
            pkg_cell = f"`{pkg_name}`"
            vid_cell = f"`{v.get('id', 'N/A')}`"
            spec_cell = f"`{v.get('vulnerable_spec', 'N/A')}`"
            ign = v.get("ignored") or {}
            ign_cell = f"`{ign['code']}`" if ign else "No"
            lines.append(f"| {pkg_cell} | {vid_cell} | {spec_cell} | {ign_cell} |")
            if not ign:
                print(
                    f"::warning title=Safety::{pkg_name} vuln {v.get('id', 'N/A')} ({v.get('vulnerable_spec', '')})"
                )

    write_summary(summary_file, lines)

    # Fail CI if any non-ignored vulnerabilities were found.
    # Policy-ignored vulns (e.g. environment-dependency) are intentional — do not fail.
    if non_ignored:
        sys.exit(1)


if __name__ == "__main__":
    main()
