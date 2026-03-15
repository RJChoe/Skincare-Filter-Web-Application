---
name: Feature Request
about: Suggest a new feature for this project
title: "[FEATURE] "
labels: enhancement
assignees: ''
---

## User Story

**As a** [type of user]
**I want** [goal/desire]
**So that** [benefit/value]

## Affected Apps

<!-- Check all that apply -->

- [ ] `allergies` - Allergy management and filtering
- [ ] `users` - User authentication and profiles
- [ ] `skincare_project` - Project-level configuration
- [ ] `templates` - UI/UX templates
- [ ] Other: ___________

## Acceptance Criteria

<!-- Define what "done" looks like -->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Approach

<!-- Optional: Suggest implementation approach -->

**Models:**
- [ ] Create new model: `_________`
- [ ] Modify existing model: `_________`
- [ ] Add fields: `_________`

**Views:**
- [ ] Create new view: `_________`
- [ ] Modify existing view: `_________`
- [ ] Add URL route: `_________`

**Templates:**
- [ ] Create new template: `_________`
- [ ] Modify existing template: `_________`

**Forms:**
- [ ] Create new form: `_________`
- [ ] Add validation logic: `_________`

## API Changes

- [ ] No API changes required
- [ ] New API endpoint: `_________`
- [ ] Modify existing endpoint: `_________`
- [ ] Breaking change (requires version bump)

## Database Migrations

- [ ] No database changes
- [ ] Add new table(s)
- [ ] Add field(s) to existing table(s)
- [ ] Modify existing field(s)
- [ ] Delete table(s) or field(s) (data migration required)

## Development Gates Checklist

<!-- All features must follow these gates in order -->

- [ ] **Gate 1:** Dependencies installed (`uv add <package>`)
- [ ] **Gate 2:** Logging added to all new modules
- [ ] **Gate 3:** Error handling implemented (`@transaction.atomic`, try-except)
- [ ] **Gate 4:** Forms created with validation (if applicable)
- [ ] **Gate 5:** Tests written (minimum 80% coverage for new code)

## Security Considerations

- [ ] No security implications
- [ ] Requires authentication/authorization
- [ ] Handles sensitive data (requires GDPR compliance)
- [ ] Exposes new API endpoint (requires rate limiting)
- [ ] Requires security review before implementation

## Performance Considerations

- [ ] No performance impact expected
- [ ] May affect database query performance (requires `.select_related()`)
- [ ] May impact page load time (requires caching)
- [ ] May require background task processing

## Additional Context

<!-- Add any other context, mockups, or screenshots about the feature request here -->

---

**For AI Agents:**
- Read [.github/instructions/copilot-instructions.md](.github/instructions/copilot-instructions.md) FIRST
- Follow Development Gates in strict order (dependency → logging → error handling → forms → tests)
- Write tests with ≥80% coverage for new code
- Update copilot-instructions.md if introducing new patterns
- Use `uv run` prefix for all commands
