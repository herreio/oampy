from setuptools import setup

setup(
    name="oampy",
    version="0.1.0",
    author="Donatus Herre",
    author_email="donatus.herre@slub-dresden.de",
    description="Open Access Monitor API Client",
    license="GPLv3",
    url="https://github.com/herreio/oampy",
    packages=["oampy"],
    install_requires=["requests", "click"],
    entry_points={
      'console_scripts': ['oampy = oampy.__main__:main'],
    },
)
