#need: docs

#wants logging & change history and reporting (basic) & custom github CI

# Search for .env file variables

# Build a new docker image
build:
	docker build -t who_clean .

# Run image python
up:
	docker run -it --rm --mount type=bind,source=${PWD},target=/usr/who_clean/ who_clean

# Run image bash 
bash:
	winpty docker run -it --rm --mount type=bind,source=${PWD},target=/usr/who_clean/ who_clean bash

# Run tests in container
test:
	docker run --rm --mount type=bind,source=${PWD},target=/usr/who_clean/ who_clean tox

# Build docs
docs: FORCE
	docker run --rm --mount type=bind,source=${PWD}/docs,target=/usr/who_clean/docs who_clean /bin/sh -c 'cd ./docs; make html'

# Lint code with isort -> black -> flake8
lint: isort black flake8

# Apply black to all src files
black:
	python -m black src

# Apply flake8 to all src files
flake8:
	python -m flake8 src

# Apply isort to all src files
isort:
	python -m isort src

# The original line had 'logs' mentioned in it.
data: preprocess process postprocess manually_cleaned master report bundle final_numbers



logs:
	# python src/report.py


# The next 3 lines each have 'logs' and 'report bundle final_numbers' mentioned in the original version.

postprocess+: postprocess manually_cleaned master 
manually_cleaned+: manually_cleaned master report bundle final_numbers
master+: master 

preprocess:
	python src/preprocess.py

process:
	python src/process.py

postprocess:
	python src/postprocess.py

manually_cleaned:
	python src/manually_cleaned.py

master:
	python src/master.py


