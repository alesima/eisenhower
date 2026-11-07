#!/usr/bin/env python3
"""
Setup script for Eisenhower Matrix application.

Note: desktop file, AppStream metainfo and icons are installed by the
Flatpak manifest (and must NOT be duplicated here to avoid conflicts).
"""

from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text() if (this_directory / "README.md").exists() else ""

setup(
    name="eisenhower-matrix",
    version="1.1.1",
    description="A GUI tool for task prioritization using the Eisenhower Matrix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alex Silva",
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
            "flake8>=4.0",
            "black>=22.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "eisenhower-gui=eisenhower_matrix.infrastructure.ui.application:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business",
        "Topic :: Utilities",
        "Environment :: X11 Applications :: GTK",
    ],
    keywords="productivity, task-management, eisenhower-matrix, gui, gtk, time-management",
)
