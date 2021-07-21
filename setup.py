from setuptools import setup, find_packages

setup(
    name='idiomatch',
    version='1.0',
    description='A SpaCy Matcher for identifying idioms',
    url='https://github.com/eubinecto/idiomatch',
    author='Eu-Bin KIM',
    python_requires='>=3.6',
    author_email='tlrndk123@gmail.com',
    license='MIT LICENSE',
    # this is needed to include the subdirectories in the library
    # will include all subdirectories that include __init__.py file.
    # https://stackoverflow.com/a/43254082
    packages=find_packages(),
    install_requires=[
        'spacy>=3.0.1',  # 3.0 is now officially supported
        # https://stackoverflow.com/a/53383704
        'en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.1.0/en_core_web_sm-3.1.0-py3-none-any.whl'
    ],
    # include the patterns and target idioms.
    package_data={
        'idiomatch': ['resources/idiom_patterns.tsv', 'resources/idioms.txt']
    }
)
