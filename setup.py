from setuptools import setup

from src.config import VERSION

setup(
    name='ubarec',
    description='Universal backup and recovery using S3 repo',
    url='http://github.com/fgbm/ubarec',
    author='Chmelyuk Vladislav',
    author_email='neimp@yandex.ru',
    license='MIT',
    version=VERSION + '.1',
    packages=['src'],
    install_requires=[
        'typer==0.3.2',
        'pyodbc==4.0.30',
        'colorama==0.4.4',
        'boto3==1.17.4',
        'appdirs==1.4.4'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': ['ubarec=src.main:app'],
    }
)
