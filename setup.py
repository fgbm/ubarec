import re

from setuptools import setup

with open("loguru/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.md", "rb") as file:
    readme = file.read().decode("utf-8")

setup(
    name='ubarec',
    version=version,
    description='Universal backup and recovery using S3 repo',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='http://github.com/fgbm/ubarec',
    author='Chmelyuk Vladislav',
    author_email='neimp@yandex.ru',
    license='MIT',
    packages=['ubarec'],
    install_requires=[
        'typer==0.3.2',
        'pyodbc==4.0.30',
        'colorama==0.4.4',
        'boto3==1.17.4',
        'appdirs==1.4.4'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': ['ubarec=ubarec.main:app'],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Russian",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.7",
)
