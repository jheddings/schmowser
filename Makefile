# Makefile for schmowser

# XXX how should this interact (or not) with setup.py?

BASEDIR ?= .
SRCDIR ?= $(BASEDIR)/src

BUILD_DIR ?= $(BASEDIR)/build
DIST_DIR ?= $(BASEDIR)/dist

# commands used in the makefile
#PY := $(shell which python)
PY := /usr/local/bin/python3
DELETE := rm -vf
RMDIR := rm -Rvf
PY2APP := $(PY) $(SRCDIR)/setup.py py2app --dist-dir=$(DIST_DIR) --bdist-base=$(BUILD_DIR)

################################################################################
.PHONY: all build rebuild clean distclean

################################################################################
all: build

################################################################################
rebuild: distclean build

################################################################################
build: clean
	cd $(BASEDIR) && $(PY2APP) --alias --no-strip -O0

################################################################################
dist: distclean
	cd $(BASEDIR) && $(PY2APP) --strip -O1

################################################################################
clean:
	$(RMDIR) $(BUILD_DIR)

################################################################################
distclean: clean
	$(RMDIR) $(DIST_DIR)
	$(RMDIR) $(BASEDIR)/.eggs
