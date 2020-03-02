from setuptools import setup, find_packages

with open("src/gather2gether/VERSION", "r") as version_file:
    __version__ = version_file.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gather2gether",
    version=__version__,
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={'gather2gether': ['VERSION']},
    author="witrdotnet",
    author_email="witr.net@gmail.com",
    description="Helps remote people to accomplish tasks together",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/witrdotnet/gather2gether",
    entry_points = {
        'console_scripts': [
            'gather2gether=gather2gether.run:main',
            'g2g=gather2gether.g2g:cli',
        ],
        'flask.commands': [
            'db=gather2gether.cli:db',
            'tasks=gather2gether.cli_task:tasks',
            'users=gather2gether.cli_user:users',
            'projects=gather2gether.cli_project:projects',
        ],
    },
    install_requires=[
        'Flask',
        'Jinja2',
        'peewee',
        'pymysql',
        'configparser',
        'tabulate',
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)
