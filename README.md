# schmowser

Schmowser is a simple utility that routes parameters to desired applications based on a
user-defined set of patterns.  The most obvious use case for this is to use a specific
web browser for specific websites, such as using Chrome for all google.com links.

## Requirements

Schmowser has been tested against Python 3, though it should generally work against
earlier versions.

The following Python libraries are required:

- PyYAML

## Installation

TODO

## Configuration

The configuration file is YAML syntax.

### Options

    DefaultApp: app

### Applications

    app: full_path_to_app_folder

### Handlers

Handlers are specified in a dictionary using a regular expression syntax.

    regex: app

### Logging

Schmowser supports the built-in Python logging facility.  This may be configured according
to the dictConfig syntax under a `Logging` section in the user configuration file.
