upload:
	#Upload new version to PyPI
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

install:
	pip install .

clean:
	# Clean unnecessary package upload generated files
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info
	find . -name '__pycache__' -exec rm -rf {} +

local-install:
	pip uninstall -y gpit
	make clean
	python3 setup.py sdist bdist_wheel
	pip install dist/*.whl

# Save to .bashrc and export the key (persistent across sessions)
# Usage: make save_key key=YOUR_KEY value=YOUR_VALUE
save_key:
	@echo "export $(key)=$(value)" >> ~/.bashrc
	@source ~/.bashrc
	@echo "Saved $(key)=$(value) to ~/.bashrc and applied the changes"