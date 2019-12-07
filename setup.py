# py2app setup file for schmowser

import os, re
import setuptools

# TODO need app icons...

#-------------------------------------------------------------------------------
# determine version information...
appver_full = None
if 'APPVER' in os.environ:
    appver_full = os.environ['APPVER']

# make a short version string...
appver_short = '0.0.0'
if appver_full is not None:
    m = re.search('[0-9]+\.[0-9]+\.[0-9]+', appver_full)
    if m is not None:
        appver_short = m.group(0)

#-------------------------------------------------------------------------------
# override app bundle metadata
plist = dict(
    CFBundleVersion=appver_short,
    CFBundleShortVersionString=appver_short,
    CFBundleLongVersionString=appver_full,
    CFBundleIdentifier='com.heddings.schmowser',
    CFBundleURLTypes=[
        dict(
            CFBundleURLName='Web URLs',
            CFBundleURLSchemes=['http', 'https']
        ),
        dict(
            CFBundleURLName='Local URLs',
            CFBundleURLSchemes=['file']
        )
    ],

    LSUIElement=True,  # run in background / no dock icon
    LSMinimumSystemVersion='10.8.0',

    NSHumanReadableCopyright='Copyright Jason Heddings. All Rights Reserved',

    NSAppTransportSecurity=dict(
        NSAllowsArbitraryLoads=True
    ),
)

#-------------------------------------------------------------------------------
# perform the bundling using setuptools with py2app
setuptools.setup(
    name='Schmowser',
    description='Utility for redirecting links to a user-specified browser...  a.k.a browser-shmowser',
    url='https://github.com/jheddings/schmowser',
    license='MIT',

    app=['src/schmowser.py'],
    setup_requires=['py2app'],

    options=dict(
        py2app=dict(
            plist=plist,
        )
    ),
)
