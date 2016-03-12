from distutils.core import setup
setup(
    name='lexeme',
    packages=['lexeme'],
    version='1.0.0',
    description='A conlang word database and generation program.',
    author='Cadel Watson',
    author_email='cadel@cadelwatson.com',
    url='https://github.com/kdelwat/Lexeme',
    keywords=['linguistics'],
    classifiers=[
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': [
            'lexeme = lexeme.lexeme:main',
        ],
    },
    install_requires=[
        'dataset',
        'tabulate',
    ],
    package_data={'lexeme': ['default-config.txt']}
)
