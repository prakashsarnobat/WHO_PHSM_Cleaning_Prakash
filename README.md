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

This project is developed in the Docker Python 3.8 container.

To develop this project locally - alter the project directory in the `.env` file.

### Local Development

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

Once in the container, run `isort`, `black`, and `flake8` with:

``` ${shell} 
make lint
```

### Testing

Run unit tests with:

``` ${shell} 
tox
```
