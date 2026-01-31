#!/usr/bin/env python3
"""
Setup script for Eisenhower Matrix application
"""

from setuptools import setup, find_packages
from pathlib import Path
import shutil

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="eisenhower-matrix",
    version="1.0.2",
    description="A GUI tool for task prioritization using the Eisenhower Matrix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alex",
    author_email="",
    url="https://github.com/alesima/eisenhower",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "PyGObject>=3.42.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "flake8>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "eisenhower-gui=eisenhower_matrix.infrastructure.ui.application:main",
        ],
    },
    scripts=[
        "eisenhower-gui",
    ],
    data_files=[
        ("share/applications", ["com.github.alesima.eisenhower.desktop"]),
        ("share/metainfo", ["com.github.alesima.eisenhower.metainfo.xml"]),
        ("share/icons/hicolor/scalable/apps", ["data/icons/com.github.alesima.eisenhower.svg"]),
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Utilities",
        "Environment :: X11 Applications :: GTK",
    ],
    keywords="productivity, task-management, eisenhower-matrix, cli, gui, gtk, time-management",
)
