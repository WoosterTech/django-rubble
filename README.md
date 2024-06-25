# django-rubble

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

Extend [django-model-utils](https://github.com/jazzband/django-model-utils) and [django-extensions](https://github.com/django-extensions/django-extensions).

>Version 0.4.0 code got deleted but still exists on PyPI.

## Features

- Serialized Number Generation (e.g. PN-0001, PN-0001; MY1, MY2)
- Useful Model and Form fields
  - `SimplePercentageField`
- Several Useful Utility Functions
  - `is_number`: checks if number could be coerced to a `float`
  - `ratio_to_whole`: .1 to 10; useful for percentages to "human"
  - `whole_to_ration`: 10 to .1; useful for "human" to "percentages"
  - perhaps others, see docs when they're published

## Installation

### From PyPI

`pip install django-rubble`

### From GitHub (for development)

1. Clone the repository: `git clone https://github.com/WoosterTech/django-rubble.git`
2. Install the dependencies: `poetry install`

## Usage

Simply use the functions, fields, models.

The biggest "gotcha" is that `NamedSerialNumber` needs to be imported in your `urls.py` file; not actually sure why, perhaps someone can help me with that?

To use the automatic numbering, subclass `NumberedModel` and make sure to include a `number_config = SerialNumberConfig(...)` attribute. It will set defaults, but just as a standard integer starting at "1" with no prefix.

```python
class PartNumber(NumberedModel):
    name = models.CharField("Part Description", max_length=100)
    number_config = SerialNumberConfig(
        initial_value=10, prefix="PN-", width=4
    )
```

Numbers will be generated starting with "PN-0010" (note the padding to make a width of 4) and increment by the default step of "1."


Contributions are welcome! Please follow the guidelines in
[CONTRIBUTING.md](CONTRIBUTING.md).


This project is licensed under the [MIT License](LICENSE).

## Contact

- Author: Karl Wooster
- Email: <karl@woostertech.com>
- Website: [woostertech.com](https://woostertech.com)

## License

MIT (see [License](LICENSE))

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
