from setuptools import setup, find_packages

setup(
    name = 'sssg',
    version = '1.0.0',
    author = 'stupidcomputer',
    author_email = 'ryan@beepboop.systems',
    url = 'https://git.beepboop.systems/stupidcomputer/sssg',
    description = 'the stupid static site generator',
    license = 'GPLv3',
    entry_points = {
        'console_scripts': [
            'sssg = sssg.__main__:main'
        ]
    },
    packages=["sssg"],
    classifiers = (
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console"
    ),
    zip_safe = False
)
