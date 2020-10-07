# Search for .env file variables
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

#Build a new docker image
build:
	docker build -t who_clean .

#Run image python
up:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/who_clean/ who_clean

#Run image bash
bash:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/who_clean/ who_clean bash

#Lint code with isort -> black -> flake8
lint: isort black flake8

#Apply black to all src files
black:
	python -m black src

#Apply flake8 to all src files
flake8:
	python -m flake8 src

#Apply isort to all src files
isort:
	python -m isort src

#dummy test target
test_read:
	python src/test.py

#need: docs & testing (tox?)

#wants logging & change history and reporting (basic)
