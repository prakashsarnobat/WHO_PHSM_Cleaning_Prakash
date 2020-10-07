# WHO_PHSM_Cleaning
Cleaning PHSM provider data for WHO

Cleaning routines for Non-pharmaceutical intervention data from 7 providers:

* CDC-ITF
* John's Hopkins HIT-COVID
* ACAPS
* GPHIN
* WHO IHR
* CSH Vienna
* OxCGRT

### Guide for contributors

This project is developed in the [Docker Python 3.8 container](https://hub.docker.com/_/python).

To develop this project locally - alter the project directory in the `.env` file.

Build the Docker image with:

``` ${shell} 
make build
```

Start a container for development with:

``` ${shell} 
make up
```

Or start a container and use `bash` with:

``` ${shell} 
make bash
```

### Linting

Once in the container, run [`isort`](https://pypi.org/project/isort/), [`black`](https://pypi.org/project/black/), and [`flake8`](https://pypi.org/project/flake8/) with:

``` ${shell} 
make lint
```

### Testing

This project uses [`tox`](https://tox.readthedocs.io/en/latest/) for automated unit testing.

Run unit tests with:

``` ${shell} 
tox
```
