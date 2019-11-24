# Makefile for schmowser

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

BUILD_DIR ?= $(BASEDIR)/build
DIST_DIR ?= $(BASEDIR)/dist
PYENV_DIR ?= $(BASEDIR)/.pyenv

# commands used in the makefile
PYENV := source $(PYENV_DIR)/bin/active &&
PY := PYTHONPATH="$(SRCDIR)" $(shell which python3)
DELETE := rm -vf
RMDIR := rm -Rvf
COPY := cp -avf
PRINT := @echo
PY2APP := $(PY) setup.py py2app --dist-dir=$(DIST_DIR) --bdist-base=$(BUILD_DIR)

APPNAME ?= Schmowser.app
APPDIR ?= $(HOME)/Applications

################################################################################
.PHONY: all env build rebuild test clean distclean

################################################################################
all: env build

################################################################################
env:
	virtualenv $(PYENV_DIR)
	$(PYENV_DIR)/bin/pip install py2app
	$(PYENV_DIR)/bin/pip install pyyaml
	$(PRINT) "Virtual environment is ready.  To activate, execute the following:"
	$(PRINT) "# source $(PYENV_DIR)/bin/activate"

################################################################################
rebuild: distclean build

################################################################################
build: clean test
	$(PY2APP) --alias --no-strip -O0

################################################################################
dist: distclean test
	$(PY2APP) --strip -O1

################################################################################
install: dist
	$(RMDIR) $(APPDIR)/$(APPNAME)
	$(COPY) $(DIST_DIR)/$(APPNAME) $(APPDIR)

################################################################################
test:
	$(PY) -m unittest discover -v -s $(BASEDIR)/test

################################################################################
clean:
	$(RMDIR) $(SRCDIR)/__pycache__
	$(RMDIR) $(BASEDIR)/__pycache__
	$(RMDIR) $(BUILD_DIR)

################################################################################
distclean: clean
	$(RMDIR) $(DIST_DIR)
	$(RMDIR) $(BASEDIR)/.eggs

################################################################################
cleanenv:
	$(RMDIR) $(PYENV_DIR)

