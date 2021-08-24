.PHONY = compile upload

PYPI_USER=tirinox

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
