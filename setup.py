from setuptools import setup, find_packages

setup(
    name='archive',
    version='0.1.2',
    url='',
    license='',
    author='clueless',
    author_email='',
    description='export logs for various platforms',
    packages=find_packages(),
    install_requires=[
        'slackclient',
        'jinja2',
        'requests'
    ],
    data_files=[],
    package_data={'archive': ['web/*']},
    include_package_data=True,
)
