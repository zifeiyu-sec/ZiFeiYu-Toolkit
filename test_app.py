#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试子非鱼工具箱应用程序
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入必要的模块
from core.data_manager import DataManager
from core.image_manager import ImageManager

def test_data_manager():
    """测试数据管理器是否能正确加载分类数据"""
    print("测试数据管理器...")
    
    # 创建数据管理器实例，使用当前目录作为配置目录
    config_dir = os.path.abspath(".")
    data_manager = DataManager(config_dir=config_dir)
    
    # 加载分类数据
    categories = data_manager.load_categories()
    
    if categories:
        print(f"成功加载 {len(categories)} 个一级分类")
        for category in categories:
            print(f"  - {category['name']} (ID: {category['id']})")
        return True
    else:
        print("无法加载分类数据")
        return False

def test_image_manager():
    """测试图片管理器是否能正确列出背景图片"""
    print("\n测试图片管理器...")
    
    # 创建图片管理器实例，使用当前目录作为配置目录
    config_dir = os.path.abspath(".")
    image_manager = ImageManager(config_dir=config_dir)
    
    # 列出所有图片
    images = image_manager.list_images()
    
    if images:
        print(f"成功加载 {len(images)} 个背景图片")
        for image in images:
            print(f"  - {image}")
        return True
    else:
        print("无法加载背景图片")
        return False

if __name__ == "__main__":
    print("子非鱼工具箱 - 功能测试")
    print("=" * 50)
    
    # 测试数据管理器
    data_ok = test_data_manager()
    
    # 测试图片管理器
    image_ok = test_image_manager()
    
    print("\n测试结果:")
    print(f"数据管理器: {'✓' if data_ok else '✗'}")
    print(f"图片管理器: {'✓' if image_ok else '✗'}")
    
    if data_ok and image_ok:
        print("\n✅ 所有测试通过! 应用程序应该可以正常运行。")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败! 请检查应用程序配置。")
        sys.exit(1)