# WHO_PHSM_Cleaning
[![GitHub Actions (Tests)](https://github.com/lshtm-gis/WHO_PHSM_Cleaning/workflows/Tests/badge.svg)](https://github.com/lshtm-gis/WHO_PHSM_Cleaning)

Cleaning PHSM provider data for WHO

Cleaning routines for Non-pharmaceutical intervention data from 7 providers:

* ACAPS
* CDC-ITF
* John's Hopkins HIT-COVID
* OxCGRT
* WHO Europe Regional Office

### Guide for contributors

This project is developed in the [Docker Python 3.8 container](https://hub.docker.com/_/python).

To develop this project locally - alter the project directory in the `.env` file.

Build the Docker image with:

``` ${shell}
make build
```

Enter a container and use `bash` with:

``` ${shell}
make bash
```

### Testing

This project uses [`tox`](https://tox.readthedocs.io/en/latest/) for automated unit testing.

Run unit tests with:

``` ${shell}
make test
```

Once in the container, run unit tests with:

``` ${shell}
tox
```

### Cleaning

Run the full cleaning routine with:

``` ${shell}
make data
```

**Please note:** Some files may be required in a `data` directory which is not tracked in this repository.

To run individual components of the cleaning routine, see the targets available in the `Makefile`.


### Linting

Once in the container, run [`isort`](https://pypi.org/project/isort/), [`black`](https://pypi.org/project/black/), and [`flake8`](https://pypi.org/project/flake8/) with:

``` ${shell}
make lint
```
