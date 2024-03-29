# Makefile for schmowser

BASEDIR ?= $(PWD)
SRCDIR ?= $(BASEDIR)/src

BUILD_DIR ?= $(BASEDIR)/build
DIST_DIR ?= $(BASEDIR)/dist
PYENV_DIR ?= $(BASEDIR)/.pyenv

APPNAME ?= Schmowser.app
APPDIR ?= $(HOME)/Applications
APPCFG ?= $(HOME)/.schmowserc

APPVER ?= $(shell git describe)
PYENV += APPVER=$(APPVER)

# commands used in the makefile
PY := $(PYENV) python3
DELETE := rm -vf
RMDIR := rm -Rvf
COPY := cp -avf
MOVE := mv -vf
PRINT := @echo
PY2APP := $(PY) setup.py py2app --dist-dir=$(DIST_DIR) --bdist-base=$(BUILD_DIR)

################################################################################
.PHONY: all env build rebuild test dist install clean cleanenv

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
rebuild: clean build

################################################################################
build: clean test
	$(PY2APP) --alias --argv-emulation --no-strip -O0
	$(COPY) $(DIST_DIR)/$(APPNAME)/Contents/Info.plist $(BASEDIR)/test/TestInfo.plist

################################################################################
dist: clean test
	$(PY2APP) --argv-emulation --strip -O1

################################################################################
install: dist
	$(RMDIR) $(APPDIR)/$(APPNAME)
	$(MOVE) $(DIST_DIR)/$(APPNAME) $(APPDIR)
	[ -f $(APPCFG) ] || $(COPY) $(BASEDIR)/config_example $(APPCFG)
	cd $(APPDIR) && open -a Schmowser --hide

################################################################################
test:
	cd $(SRCDIR) && $(PY) -m unittest discover -v -s $(BASEDIR)/test

################################################################################
clean:
	$(RMDIR) $(SRCDIR)/__pycache__
	$(RMDIR) $(BASEDIR)/__pycache__
	$(RMDIR) $(BASEDIR)/test/__pycache__
	$(RMDIR) $(BASEDIR)/.eggs
	$(RMDIR) $(BUILD_DIR)
	$(RMDIR) $(DIST_DIR)

################################################################################
cleanenv:
	$(RMDIR) $(PYENV_DIR)

