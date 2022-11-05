from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent

long_description = ''
with open(here.joinpath('README.md'), encoding='utf-8') as f:
    long_description = f.read()

requirements = []
with open(here.joinpath('requirements.txt'), encoding='utf-8') as f:
    requirements = f.readlines()

test_requirements = []
with open(here.joinpath('requirements-test.txt'), encoding='utf-8') as f:
    test_requirements = f.readlines()


setup(
    name='find-py-imports',
    # version=version,
    install_requires=requirements,
    description='find import statement',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='hassaku63',
    author_email='hassaku63@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Japanese'
    ],
    keywords=['python', 'import'],
    url='https://github.com/hassaku63/find-py-imports',
    entry_points={
        'console_scripts': [
            'find_py_imports = find_py_imports:cli.main'
        ],
    },
    packages=find_packages(exclude=['tests*']),
    python_requires=">=3.6",
    tests_require=test_requirements,
    project_urls={
        'Source': 'https://github.com/hassaku63/find-py-imports',
    }
)