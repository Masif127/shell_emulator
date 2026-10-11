.PHONY: test run clean

run:
	python3 -m src.gui

test:
	python3 -m unittest discover -s tests -p "test_*.py"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete