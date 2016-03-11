from distutils.core import setup
setup(
    name='lexeme',
    packages=['lexeme'],
    version='0.9.1.9.6',
    description='A conlang word database and generation program.',
    author='Cadel Watson',
    author_email='cadel@cadelwatson.com',
    url='https://github.com/kdelwat/Lexeme',
    # download_url='https://github.com/kdelwat/Lexeme/tarball/0.9.1',
    keywords=['testing'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'lexeme = lexeme.lexeme:main',
        ],
    },
    install_requires=[
        'dataset',
        'tabulate',
    ],
)
