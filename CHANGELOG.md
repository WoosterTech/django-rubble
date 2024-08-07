## 0.5.0b0 (2024-07-17)

### Feat

- **numbers**: add "any_to_float" function

## 0.4.2 (2024-06-25)

### Fix

- **db_forms**: use named argument for `Percent` to satisfy BaseModel

## 0.4.1 (2024-06-25)

## 0.4.0 (2024-06-25)

### Feat

- **number**: add numbers as a new model with admin

## 0.3.0 (2024-06-19)

### Feat

- **stamped_admin**: add StampedTabularInline

## 0.2.3 (2024-06-05)

### Fix

- **pyproject**: fix django constraint *again*
- **pyproject**: add metadata for pypi and "fix" django deps

## 0.2.2 (2024-06-02)

### Refactor

- **functions**: simplification of some number functions to better utilize Decimal methods

## 0.2.1 (2024-06-02)

### Fix

- **django-version**: previous change didn't allow django >5.0 :clown_face:

### Refactor

- **rename-package**: from django-utils (already taken) to django-rubble

## 0.2.0 (2024-05-30)

### Feat

- **percentage_field**: add percentage field as model field with form field and Percent type

### Fix

- **django-version**: was ~5.0 which doesn't work with 4.x versions... changed to <=5.0
