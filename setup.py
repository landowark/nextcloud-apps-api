from setuptools import setup, find_packages
from pathlib import Path

VERSION = '0.0.1'
DESCRIPTION = 'API interface to popular nextcloud apps.'
LONG_DESCRIPTION = 'Nexcloud Notes & Bookmarks API'
this_dir = Path(__file__).parent

with open(Path.joinpath(this_dir, "requirements.txt").__str__(), "r") as fp:
    requirements = [line.strip() for line in fp.readlines()]

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="nextcloud_apps_api",
    version=VERSION,
    author="Landon Wark",
    author_email="<lando.wark@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=requirements,  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Linux :: Linux"
    ]
)