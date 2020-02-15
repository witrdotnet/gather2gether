from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gather2gether",
    version="0.0.2",
    packages=find_packages("src"),
    package_dir={"": "src"},
    author="witrdotnet",
    author_email="witr.net@gmail.com",
    description="Helps remote people to accomplish tasks together",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/witrdotnet/gather2gether",
    entry_points = {
        'console_scripts': ['gather2gether=gather2gether.run:main'],
    },
    install_requires=[
        'Flask',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.0',
)
