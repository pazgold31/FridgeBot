import setuptools
from FridgeBot.version import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="FridgeBot",
    version=__version__,
    author="Paz",
    author_email="paz@fridgebots.com",
    description="A Fridge bot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    scripts=['FridgeBot/Utils/update.sh'],
    install_requires=["python-telegram-bot >= 13"],
    package_data={'': ['FridgeBot/Bot/keys.json',]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
