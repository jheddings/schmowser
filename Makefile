# Makefile for schmowser

BASEDIR ?= .
SRCDIR ?= $(BASEDIR)/src

BUILD_DIR ?= $(BASEDIR)/build
DIST_DIR ?= $(BASEDIR)/dist

# commands used in the makefile
#PY := $(shell which python)
PY := PYTHONPATH="$(SRCDIR)" /usr/local/bin/python3
DELETE := rm -vf
RMDIR := rm -Rvf
COPY := cp -avf
PY2APP := $(PY) setup.py py2app --dist-dir=$(DIST_DIR) --bdist-base=$(BUILD_DIR)

APPNAME := Schmowser.app
APPDIR := $(HOME)/Applications

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
test: build test
	$(PY) -m unittest discover -v -s $(BASEDIR)/test

################################################################################
dist: distclean
	cd $(BASEDIR) && $(PY2APP) --strip -O1

################################################################################
install: dist
	[ -d "$(APPDIR)/$(APPNAME)" ] && $(RMDIR) $(APPDIR)/$(APPNAME)
	$(COPY) $(DIST_DIR)/$(APPNAME) $(APPDIR)

################################################################################
clean:
	$(RMDIR) $(BASEDIR)/__pycache__
	$(RMDIR) $(BUILD_DIR)

################################################################################
distclean: clean
	$(RMDIR) $(DIST_DIR)
	$(RMDIR) $(BASEDIR)/.eggs
