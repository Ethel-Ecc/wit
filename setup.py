"""
    It provides a standard wrapper-interface for presenting this datasets in a unified view and offering direct
    download from source, without any local hosting/storage of the dataset itself.
"""

import setuptools


with open("README.rst", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="ckan-wit",
    version="0.1.6",
    author="EO",
    author_email="c.obinna@stud.uni-goettingen.de",
    description="A Wrapper Interface Tool (WIT) that verifies, aggregates, and filters metadata infos across CKAN-compatible Open Data"
                "portals",
    long_description=long_description,
    url="https://ckan-wit-documentation.readthedocs.io/en/latest/",
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    include_package_data=True,
    zip_safe=False,

    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
