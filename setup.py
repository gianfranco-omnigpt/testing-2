"""Setup script for to-do CLI app."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="todo-cli",
    version="1.0.0",
    author="gianfranco-omnigpt",
    description="A simple command-line to-do list application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gianfranco-omnigpt/testing-2",
    py_modules=['todo', 'tasks', 'storage'],
    install_requires=[
        'click>=8.0.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'todo=todo:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)