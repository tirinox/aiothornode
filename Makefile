.PHONY = compile upload clean help

.DEFAULT_GOAL: help

PYPI_USER=tirinox

help:
	@echo "make compile|upload|clean"

compile:
	@echo "Compile and check!"
	python setup.py sdist && twine check dist/*

upload:
	@echo "Uploading to PyPi!"
	make clean
	python setup.py sdist
	twine upload -u $(PYPI_USER) dist/*

clean:
	@echo "Cleaning!"
	rm -r dist/*
