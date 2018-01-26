import sys
from setuptools import setup

setup(
    name = "nootp",
    version = "0.1",
    packages=["nootp"],
    install_requires=[
        "pyotp",
        "pyperclip"
    ],
    author="Andrey Khokhlin",
    author_email = "khokhlin@gmail.com",
    description = "Quick connection to the Anyconnect VPN withdout cellular",
    license = "GPL",
    keywords= "anyconnect cisco vpn python otp",
    url = "http://github.com/khokhlin/nootp/",
    entry_points = {
        "console_scripts": [
            "nootp = nootp.nootp:main",
        ],
    }
)


