# Forms & Validation

> Gate 4 reference. **Do not implement until Gates 2 and 3 are complete.**
> Check [STATUS.md](../../STATUS.md) before starting.

## Gate 4 Tasks

1. Create `allergies/forms.py` with `AllergenSelectionForm` and `UserAllergyDetailForm`
2. Create `allergies/services.py` with `check_ingredients(ingredient_text, user)` matching logic
3. Wire create/edit/check views in `allergies/views.py`
4. Add `{% csrf_token %}` to all POST templates
5. Write form tests (80% coverage required for new code)

## `AllergenSelectionForm` Pattern (batch create)

```python
# allergies/forms.py
from django import forms
from allergies.models import Allergen, UserAllergy

class AllergenSelectionForm(forms.Form):
    """Batch allergen selection. Renders grouped checkboxes — no JS required."""

    allergens = forms.ModelMultipleChoiceField(
        queryset=Allergen.objects.filter(is_active=True).order_by("subcategory", "allergen_key"),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
```

The template groups checkboxes using Django's `{% regroup %}` tag on `allergen.subcategory`.
The view passes the queryset directly — no choices constant or pk mapping dict needed.

## `UserAllergyDetailForm` Pattern (edit)

```python
class UserAllergyDetailForm(forms.ModelForm):
    """Edit severity, confirmation, source, and reaction details for one allergen."""

    class Meta:
        model = UserAllergy
        fields = ["severity_level", "is_confirmed", "source_info", "user_reaction_details"]
        widgets = {
            "user_reaction_details": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self) -> dict:
        cleaned_data = super().clean()
        severity_level = cleaned_data.get("severity_level")
        if severity_level in ("severe", "life_threatening") and not cleaned_data.get("is_confirmed"):
            raise ValidationError("Severe allergies require confirmation.")
        return cleaned_data
```

## Product Check Form Pattern

```python
class ProductCheckForm(forms.Form):
    """Paste ingredient list; returns matching allergens via services.check_ingredients"""

    ingredient_list = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 6, "placeholder": "Paste full ingredient list…"}),
        label="Ingredient List",
    )
```

View:

```python
# allergies/views.py
from allergies import services

@login_required
def check_product(request: HttpRequest) -> HttpResponse:
    form = ProductCheckForm(request.POST or None)
    matches: list | None = None
    if request.method == "POST" and form.is_valid():
        matches = services.check_ingredients(
            form.cleaned_data["ingredient_list"],
            request.user,
        )
    return render(request, "allergies/check_product.html", {"form": form, "matches": matches})
```

Result display in template:

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Check</button>
</form>

{% if matches is not None %}
    {% if matches %}
        <p>Unsafe — contains the following allergens:</p>
        <ul>{% for allergen in matches %}<li>{{ allergen }}</li>{% endfor %}</ul>
    {% else %}
        <p>Safe — no known allergens detected.</p>
    {% endif %}
{% endif %}
```

## Template Pattern (batch allergen selection)

```html
<form method="post">
    {% csrf_token %}
    {% regroup allergens by subcategory as subcategory_groups %}
    {% for group in subcategory_groups %}
        <fieldset>
            <legend>{{ group.grouper }}</legend>
            {% for allergen in group.list %}
                <label>
                    <input type="checkbox" name="allergens" value="{{ allergen.pk }}"
                        {% if allergen in form.allergens.value %}checked{% endif %}>
                    {{ allergen.label }}
                </label>
            {% endfor %}
        </fieldset>
    {% endfor %}
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

@login_required
@transaction.atomic
def create_allergies(request: HttpRequest) -> HttpResponse:
    allergens = Allergen.objects.filter(is_active=True).order_by("subcategory", "allergen_key")
    form = AllergenSelectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        for allergen in form.cleaned_data["allergens"]:
            UserAllergy.objects.get_or_create(user=request.user, allergen=allergen)
        return redirect("allergies:list")
    return render(request, "allergies/allergy_form.html", {
        "form": form,
        "allergens": allergens,
    })
```

Matching logic for the product check view lives in `allergies/services.py`
(see `services.check_ingredients`).
