from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'bundle_files': 1}},
    service = ['vulnservice'],
    zipfile = None,
)
