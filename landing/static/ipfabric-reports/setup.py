# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ipfabric-reports",
    version="1.0.4",
    author="Milan Zapletal",
    author_email="milan.zapletal@ipfabric.io",
    description="A package to generate reports from IP Fabric data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ip-fabric/integrations/scripts/ipfabric-reports",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "ipfabric",
        "python-dotenv",
        "jinja2",
        "weasyprint",
        "matplotlib",
        "pandas",
        "openpyxl",
        "setuptools",
        "loguru",
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "ipfabric-report=ipfabric_reports.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ipfabric_reports": ["templates/*", "styles/*"],
    },
)
