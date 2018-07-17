from distutils.core import setup

setup(
    name='wikibase-tools',
    version='0.0.1',
    author='Greg Stupp',
    author_email='stuppie@gmail.com',
    url='https://github.com/stuppie/wikibase-tools',
    description='Tools for working with a wikibase',
    license='MIT',
    keywords='ontology wikidata wikibase',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ],
    packages=['wikibase_tools'],
)
