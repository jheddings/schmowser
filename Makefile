# Makefile for schmowser

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

BUILD_DIR ?= $(BASEDIR)/build
DIST_DIR ?= $(BASEDIR)/dist

# commands used in the makefile
PY := PYTHONPATH="$(SRCDIR)" $(shell which python3)
DELETE := rm -vf
RMDIR := rm -Rvf
COPY := cp -avf
PY2APP := $(PY) setup.py py2app --dist-dir=$(DIST_DIR) --bdist-base=$(BUILD_DIR)

APPNAME ?= Schmowser.app
APPDIR ?= $(HOME)/Applications

################################################################################
.PHONY: all build rebuild test clean distclean

################################################################################
all: build

################################################################################
rebuild: distclean build

################################################################################
build: clean test
	cd $(BASEDIR) && $(PY2APP) --alias --no-strip -O0

################################################################################
dist: distclean test
	cd $(BASEDIR) && $(PY2APP) --strip -O1

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
	$(RMDIR) $(BASEDIR)/test/__pycache__
	$(RMDIR) $(BUILD_DIR)

################################################################################
distclean: clean
	$(RMDIR) $(DIST_DIR)
	$(RMDIR) $(BASEDIR)/.eggs
