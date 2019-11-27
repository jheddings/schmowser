# py2app setup file for schmowser

import setuptools

# TODO need app icons...

# override app bundle metadata
plist = dict(
    CFBundleVersion='0.1.0',
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
    LSUIElement=True
)

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
