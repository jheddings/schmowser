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

## Performance

On my MacBook Pro, using Python directly to process links takes about 0.2 sec.  On
the same system, using `open` for links with Schmowser takes up to 0.5 sec with an
average of 0.35 sec.  The same call to `open` using Safari take 0.1 sec or less.

## Troubleshooting

Enabling logging may give you some clues about what's happening with the app.  Set the levels
to `DEBUG` for each handler.  Standard out & standard error are sent to the Console, so a
log file may be easier to debug.

*NOTE* the current directory for the app is `Schmowser.app/Contents/Resources`.  This is
where the default log file will be created unless you specify an absolute path.

A great tool for troubleshooting application handlers is
[RCDefaultApp](http://www.rubicode.com/Software/RCDefaultApp/) from Rubicode.

## TODO

- Improve the overall install experience.
- Look into releasing the app as an installable package bundle.
- Find more ways to to test the app.
- Improve performance when opening links.
- Handle machine / platform specific config sections.
- Rename this project to 'schlep' ?
- Make an app icon - look into `sips`.
