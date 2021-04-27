.PHONY = compile upload

compile:
	@echo "Compile and check!"
	python setup.py sdist && twine check dist/*

upload:
	@echo "Uploading to PiPy!"
	make clean
	python setup.py sdist
	twine upload dist/*

clean:
	@echo "Cleaning!"
	rm -r dist/*
