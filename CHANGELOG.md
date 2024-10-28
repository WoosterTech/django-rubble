## 0.7.0b6 (2024-10-28)

## 0.7.0b5 (2024-10-17)

### Fix

- **Secrets**: cast client secret to LongSecretStr explicitly when read from environment

## 0.7.0b4 (2024-10-17)

## 0.7.0b3 (2024-10-17)

### Feat

- **secrets**: add secrets module for Infisical and creating sample env file from settings.py

## 0.7.0b2 (2024-10-16)

## 0.7.0b1 (2024-10-16)

### Feat

- **strings.py**: add uuid_ish function

## 0.7.0b0 (2024-09-18)

### Feat

- **utils**: add `truncate_string` function with tests and docs

## 0.6.0 (2024-09-17)

### Feat

- **context**: cache versions in ProjectRegistry to avoid db hits before apps are ready

## 0.5.2 (2024-08-30)

## 0.5.1 (2024-08-29)

### Fix

- **models**: remove TestNumberModel

## 0.5.0 (2024-08-29)

### Feat

- **django**: support django 5.1

## 0.5.0b1 (2024-08-22)

### Feat

- **neapolitan**: add enums and other helpers to work with neapolitan-sundae

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
