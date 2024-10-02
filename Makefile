# Define variables
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# Default target
.PHONY: all
all: install

# Create virtual environment
$(VENV_DIR):
	python3 -m venv $(VENV_DIR)

# Install main dependencies
.PHONY: install
install: $(VENV_DIR)
	$(PIP) install .

# Install development dependencies
.PHONY: install-dev
install-dev: $(VENV_DIR)
	$(PIP) install -r requirements-dev.txt

# Run tests
.PHONY: test
test: $(VENV_DIR)
	$(PIP) install -r requirements-dev.txt
	$(VENV_DIR)/bin/pytest

# Clean up
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
	find . -type d -name "__pycache__" -exec rm -r {} +

# Linting (optional)
.PHONY: lint
lint: $(VENV_DIR)
	$(PIP) install flake8
	$(VENV_DIR)/bin/flake8 doctly tests

# Format code (optional)
.PHONY: format
format: $(VENV_DIR)
	$(PIP) install black
	$(VENV_DIR)/bin/black doctly tests

# Run all checks (optional)
.PHONY: check
check: lint test