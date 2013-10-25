from setuptools import setup
from behave_cli import __version__

setup(version=unicode(__version__),
      name="behave_cli",
      author="Konstantinos Koukopoulos",
      description="Longaccess BDD CLI step library",
      long_description=open('README.md').read(),
      packages=['behave_cli', 'behave_cli.api', 'behave_cli.s3mock',
                'behave_cli.expect', 'behave_cli.netrc', 'behave_cli.files'],
      install_requires=['behave', 'pexpect', 'requests', 'moto', 'mock']
      )
