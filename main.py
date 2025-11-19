#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
子非鱼工具箱 - 主入口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont
from core.app import PentestToolManager

# 设置中文字体支持
def setup_fonts():
    font = QFont()
    font.setFamily("Microsoft YaHei")
    return font

# 确保配置目录存在
def ensure_config_dir():
    # 获取用户目录
    home_dir = os.path.expanduser("~")
    config_dir = os.path.join(home_dir, ".pentest_tool_manager")
    
    # 创建配置目录
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    # 创建图片目录
    image_dir = os.path.join(config_dir, "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    return config_dir

def main():
    # 设置高DPI支持
    from PyQt5.QtCore import Qt
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # 创建Qt应用
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 设置字体
    app.setFont(setup_fonts())
    
    # 使用当前目录作为配置目录
    config_dir = os.path.abspath(".")
    
    # 确保图片目录存在
    images_dir = os.path.join(config_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    # 创建主窗口
    window = PentestToolManager(config_dir=config_dir)
    
    # 显示窗口
    window.show()
    
    # 运行应用
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()