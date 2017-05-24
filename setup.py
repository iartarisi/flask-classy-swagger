"""Flask-Classy-Swagger.

---------------

Generate swagger definitions from Flask-Classy API modules.
"""
from setuptools import setup, find_packages


with open('README.md') as f:
    description = f.read()

setup(
    name='Flask-Classy-Swagger',
    version='0.9.1',
    url='https://github.com/jetbridge/flask-classy-swagger',
    license='BSD',
    author='Ionuț Arțăriși and Alfred Perlstein and Mischa Spiegelmock',
    author_email='alfred@freebsd.org',
    description='Autogenerate swagger from flask classy api',
    long_description=description,
    packages=find_packages(exclude=['ez_setup', 'examples']),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'pytest-cov',
        'coverage',
        'flask-classy',
        'undecorated',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
