from pathlib import Path
from setuptools import setup, find_packages


setup(
    name="outta",
    version="0.3.0",
    packages=find_packages("source"),
    author="Austin Bingham",
    author_email="austin.bingham@protonmail.com",
    description="ANSI control code parsing",
    license="LGPL",
    keywords="",
    url="http://github.com/abingham/outta",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],
    platforms="any",
    include_package_data=True,
    package_dir={"": "source"},
    # package_data={'outta': . . .},
    install_requires=[
        "pyte",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax, for
    # example: $ pip install -e .[dev,test]
    extras_require={
        "dev": ["black", "bump2version", "flake8"],
        # 'doc': ['sphinx', 'cartouche'],
        "test": ["pytest"],
    },
    entry_points={
        # 'console_scripts': [
        #    'outta = outta.cli:main',
        # ],
    },
    long_description=Path("README.rst").read_text(encoding="utf-8"),
)
