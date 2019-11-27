# schmowser

Schmowser is a simple utility that routes parameters to desired applications based on a
user-defined set of patterns.  The most obvious use case for this is to use a specific
web browser for specific websites, such as using Chrome for all google.com links.

## Requirements

Schmowser has been tested against Python 3, though it should generally work against
earlier versions.

The following Python libraries are required:

- PyYAML
- py2app

Alternatively, use `virtualenv` as follows:

    make env
    source .pyenv/bin/activate

## Installation

    make test
    make install

*NOTE* occasionally the install step will end with an error.  If this happens, you may need
to run Schmowser manually to register the URL handlers.  Simply double-clicking the app
from your `~/Applications` folder will do it.

Edit `~/.schmowserc` config file; use `config_example` as a starting point.

Set your default browser to Schmowser under System Preferences -> General.

Give it a spin!

## Configuration

The configuration file is YAML syntax.  For now, hopefully it is self-explanatory enough to
get you started.  At least until I get more time to write up the documentation.

### Logging

Schmowser supports the built-in Python logging facility.  This may be configured according
to the dictConfig syntax under a `Logging` section in the user configuration file.  To
disable logging, simply remove this section.

## TODO

- Improve the overall install experience.
- Look into releasing the app as an installable package bundle.
- Find more ways to to test the app.
- Improve performance when opening links.
