upload:
	#Upload new version to PyPI
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

install:
	pip install .

clean:
	#Clean unnecessary package upload generated files
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -name '__pycache__' -exec rm -rf {} +