from setuptools import find_packages, setup

setup(
    name = "EmBat",
    version = "0.1",
    packages = find_packages(),
    scripts = ['src/Imap.py', 'src/baseController.py', 'src/Credentials.py', 'src/EmBat.py'],
    
    entry_points = {
        "console_scripts": [
            "EmBat = EmBat:run"
            ]
        },

    install_requires = [ ],

    author = "Dtripp",
    author_email = "dtrippx@gmail.com",
    description = "Automated batching of e-mail accounts to validate credentials",
    license = "MIT",
    long_description = open("README.md").read(),
    url = "http://github.com/dtrip/embat"
)

