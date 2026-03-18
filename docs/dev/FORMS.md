# Forms & Validation

> Gate 4 reference. **Do not implement until Gates 2 and 3 are complete.**
> Check [STATUS.md](../../STATUS.md) before starting.

## Gate 4 Tasks

1. Create `allergies/forms.py` with `UserAllergyForm`
2. Add a JSON endpoint (`get_allergen_keys`) for dynamic category → allergen filtering
3. Wire create/edit views in `allergies/views.py`
4. Add `{% csrf_token %}` to all POST templates
5. Write form tests (80% coverage required for new code)

## `UserAllergyForm` Pattern

```python
# allergies/forms.py
from django import forms
from django.core.exceptions import ValidationError
from allergies.models import UserAllergy, Allergen
import logging

logger = logging.getLogger(__name__)


class UserAllergyForm(forms.ModelForm):
    """Form for creating/editing user allergies with dynamic allergen filtering."""

    class Meta:
        model = UserAllergy
        fields = [
            "allergen",
            "severity_level",
            "is_confirmed",
            "source_info",
            "user_reaction_details",
        ]
        widgets = {
            "user_reaction_details": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["allergen"].queryset = Allergen.objects.filter(is_active=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        severity_level = cleaned_data.get("severity_level")
        if severity_level == "severe" and not cleaned_data.get("is_confirmed"):
            logger.warning(
                "Severe allergy submitted without confirmation — "
                "user %s", self.instance.user_id if self.instance.pk else "new"
            )
            raise ValidationError("Severe allergies require confirmation.")
        return cleaned_data
```

## Dynamic Category → Allergen Filtering

`allergen_key` choices are category-dependent. The recommended approach is a
lightweight JSON view — no HTMX dependency, fits the current no-partials constraint.

```python
# allergies/views.py — add this alongside existing views
from django.http import JsonResponse
from allergies.constants.choices import CATEGORY_TO_ALLERGENS_MAP

def get_allergen_keys(request: HttpRequest) -> JsonResponse:
    """Return allergen key/label pairs for a given category."""
    category = request.GET.get("category", "")
    choices = CATEGORY_TO_ALLERGENS_MAP.get(category, [])
    return JsonResponse({"allergens": [{"key": k, "label": l} for k, l in choices]})
```

```javascript
// Minimal JS — fetch allergens when category changes
document.getElementById("id_category").addEventListener("change", function () {
    fetch(`/allergies/allergen-keys/?category=${this.value}`)
        .then(r => r.json())
        .then(data => {
            const select = document.getElementById("allergen-key-select");
            select.innerHTML = '<option value="">Select allergen…</option>';
            data.allergens.forEach(a => {
                select.insertAdjacentHTML("beforeend",
                    `<option value="${a.key}">${a.label}</option>`);
            });
        });
});
```

## Template Pattern

```html
<form method="post" id="allergy-form">
    {% csrf_token %}

    <select name="category" id="id_category">
        <option value="">Select category…</option>
        {% for value, label in CATEGORY_CHOICES %}
            <option value="{{ value }}">{{ label }}</option>
        {% endfor %}
    </select>

    <select name="allergen_key" id="allergen-key-select">
        <option value="">Select allergen…</option>
    </select>

    {{ form.as_p }}
    <button type="submit">Save</button>
</form>
```

## Error Display

```html
{% if form.errors %}
    <div class="error-messages">
        {{ form.non_field_errors }}
        {% for field in form %}
            {% if field.errors %}
                <p>{{ field.label }}: {{ field.errors }}</p>
            {% endif %}
        {% endfor %}
    </div>
{% endif %}
```

## CSRF

- Always include `{% csrf_token %}` in POST forms — middleware is already configured.
- For JavaScript POST requests, pass the `X-CSRFToken` header:
  ```javascript
  headers: { "X-CSRFToken": document.cookie.match(/csrftoken=([^;]+)/)?.[1] }
  ```

## Validation Order

1. `Form.clean()` — cross-field validation (severity + confirmation, etc.)
2. `Model.clean()` — model constraints; `UserAllergy.clean()` enforces JSONField
   key discipline and rejects future `symptom_onset_date`
3. `Model.save()` — database constraints (unique together, foreign keys)

Always call `form.is_valid()` before accessing `form.cleaned_data`.

## View Pattern (create)

```python
# allergies/views.py
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.exceptions import ValidationError

@login_required
@transaction.atomic
def create_allergy(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserAllergyForm(request.POST)
        if form.is_valid():
            try:
                allergy = form.save(commit=False)
                allergy.user = request.user
                allergy.full_clean()
                allergy.save()
                logger.info(
                    "User %s created allergy %s", request.user.id, allergy.id
                )
                return redirect("allergies:list")
            except ValidationError as e:
                logger.warning(
                    "Validation failed for user %s: %s", request.user.id, e
                )
                transaction.set_rollback(True)
                form.add_error(None, e)
    else:
        form = UserAllergyForm()
    return render(request, "allergies/allergy_form.html", {"form": form})
```
