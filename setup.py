from distutils.core import setup
import os

import climate_downloader

def _strip_comments(l):
    return l.split('#', 1)[0].strip()

def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]

def _reqs(*f):
    return [
        _pip_requirement(r) for r in (
            _strip_comments(l) for l in open(
                os.path.join(os.getcwd(), 'requirements', *f)).readlines()
        ) if r]

def reqs(*f):
    """Parse requirement file.
    Returns:
        List[str]: list of requirements specified in the file.
    Example:
        reqs('default.txt')          # requirements/default.txt
        reqs('extras', 'redis.txt')  # requirements/extras/redis.txt
    """
    return [req for subreq in _reqs(*f) for req in subreq]

def install_requires():
    """Get list of requirements required for installation."""
    return reqs('requirements.txt')

setup(
    name             = 'climate_downloader',
    version          = climate_downloader.__version__,
    description      = climate_downloader.__description__,
    long_description = open('README.md').read(),
    keywords         = climate_downloader.__keywords__,
    author           = climate_downloader.__author__,
    author_email     = climate_downloader.__contact__,
    url              = climate_downloader.__url__,
    license          = 'LICENSE.txt',
    python_requires  = ">=3.7",
    install_requires = install_requires(),
    packages         = ['climate_downloader', 'climate_downloader.test'],
    package_data     = {'climate_downloader' : ['resources/*']},
    scripts          = [
	'scripts/download/download_csiro_area.py',
	'scripts/download/download_csiro_pointlist.py',
	'scripts/download/download_csiro_datamap.py',
	'scripts/download/download_mjo.py',
	'scripts/download/download_noaa_wmo.py',
	],
)

