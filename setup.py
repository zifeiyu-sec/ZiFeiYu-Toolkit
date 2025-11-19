#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子非鱼工具箱 - 安装配置
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pentest-tool-manager",
    version="1.0.0",
    description="子非鱼工具箱 - 一个分类管理和运行渗透测试工具的图形界面应用",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="User",
    author_email="user@example.com",
    url="https://github.com/user/pentest-tool-manager",
    packages=find_packages(),
    package_data={
        '': ['*.png', '*.json'],
    },
    include_package_data=True,
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        'console_scripts': [
            'pentest-tool-manager=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)