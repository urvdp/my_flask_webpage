from setuptools import setup, find_packages

setup(
    name='my_flask_webpage',
    version='0.1.0',
    packages=find_packages(include=['__init__']),
    test_suite = 'test',
    install_requires=[
        "flask >= 2.0.0"
    ],
    python_requires='>=3.6'
)