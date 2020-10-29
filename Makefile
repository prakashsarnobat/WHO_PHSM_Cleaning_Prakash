#need: docs

#wants logging & change history and reporting (basic) & custom github CI

# Search for .env file variables

#Build a new docker image
build:
	docker build -t who_clean .

#Run image python
up:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/who_clean/ who_clean

#Run image bash
bash:
	docker run -it --rm --mount type=bind,source="${PWD}",target=/usr/who_clean/ who_clean bash

#Run tests in container
test:
	docker run --rm --mount type=bind,source=${PWD},target=/usr/who_clean/ who_clean tox

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

#Build docs
docs: FORCE
	sphinx-apidoc -f -o docs/source src
	sphinx-apidoc -f -o docs/source tests
	cd ./docs && $(MAKE) html

data: preprocess process postprocess manually_cleaned logs report

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

logs:
	python src/report.py

report: tech_report

tech_report:
	jupyter nbconvert --to html --TemplateExporter.exclude_input=True --execute reporting/technical_report.ipynb

#Phony target to force rebuilds
.PHONY: FORCE
FORCE:
