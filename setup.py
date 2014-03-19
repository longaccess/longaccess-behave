from setuptools import setup
from behave_cli import __version__

setup(version=unicode(__version__),
      name="behave_cli",
      author="Konstantinos Koukopoulos",
      author_email='kk@longaccess.com',
      license="Apache",
      description="Longaccess BDD CLI step library",
      long_description=open('README.md').read(),
      packages=['behave_cli', 'behave_cli.api', 'behave_cli.s3mock',
                'behave_cli.expect', 'behave_cli.netrc', 'behave_cli.files'],
      install_requires=['behave', 'pexpect', 'requests', 'moto', 'mock'],
      url='https://github.com/longaccess/longaccess-behave/',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Information Technology',
          'Natural Language :: English',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Testing',
      ]
      )
