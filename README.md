# 子非鱼工具箱 (ZiFeiYu Toolkit)

一个现代化、功能齐全的渗透测试工具分类管理平台，专为安全测试人员设计，帮助快速组织和访问各种渗透测试工具。

## 📋 项目概述

子非鱼工具箱是一个基于PyQt5开发的跨平台渗透测试工具管理系统，提供直观的图形界面，帮助安全测试人员更高效地管理和使用各类渗透测试工具。
![alt text](image.png)

## ✨ 功能特性

### 核心功能
- **分类管理**：支持多级工具分类，按功能、应用场景等方式组织工具
- **工具卡片**：美观的卡片式布局展示工具信息，支持自定义背景图片
- **快速搜索**：实时搜索工具名称和描述，快速定位所需工具
- **工具执行**：直接从界面运行工具，支持参数配置
- **数据管理**：JSON格式存储工具信息，支持数据导入/导出
- **背景图片**：支持自定义工具卡片背景图片，提升视觉体验
- **跨平台**：支持Windows、Linux和macOS系统

### 已实现的分类
- 信息收集 (Information Gathering)
- 漏洞分析 (Vulnerability Analysis)
- Web应用渗透 (Web Application Penetration)
- 数据库评估 (Database Assessment)
- 密码攻击 (Password Attacks)
- 无线攻击 (Wireless Attacks)
- 逆向工程 (Reverse Engineering)
- 漏洞利用 (Exploitation Tools)
- 嗅探与欺骗 (Sniffing & Spoofing)
- 后利用 (Post Exploitation)
- 数字取证 (Digital Forensics)
- 报告工具 (Reporting Tools)
- 社会工程 (Social Engineering)
- 硬件黑客 (Hardware Hacking)
- 压力测试 (Stress Testing)
- 维护访问与匿名 (Maintaining Access & Anonymity)
- 杂项工具 (Miscellaneous Tools)

## 🛠️ 技术栈

- **语言**：Python 3.7+
- **GUI框架**：PyQt5
- **数据存储**：JSON
- **图像处理**：PyQt5内置图像处理
- **打包工具**：PyInstaller

## 📦 安装说明

### 从源代码安装

1. **克隆仓库**
```bash
git clone https://github.com/yourusername/Vodafone-Pentest-Toolkit.git
cd Vodafone-Pentest-Toolkit
```

2. **安装依赖**
```bash
pip install PyQt5
```

3. **运行应用**
```bash
python main.py
```

### 从可执行文件安装

1. 从GitHub Releases页面下载最新版本的可执行文件
2. 解压到任意目录
3. 双击 `Vodafone-Pentest-Toolkit.exe` 运行应用
或者
直接下载源码后双击dist目录下的exe文件可以直接运行，等同于上图

## 🚀 使用指南

### 基本操作

1. **浏览工具**：在左侧分类树中选择分类，右侧将显示该分类下的所有工具
2. **搜索工具**：在搜索框中输入关键词，实时筛选工具
3. **运行工具**：点击工具卡片上的"运行"按钮，根据提示配置参数
4. **添加工具**：点击"添加工具"按钮，填写工具信息和命令
5. **编辑工具**：右键点击工具卡片，选择"编辑"菜单修改工具信息
6. **设置背景**：右键点击工具卡片，选择"设置背景"更换背景图片

### 配置工具

工具配置支持以下功能：
- 自定义工具名称和描述
- 设置工具命令和参数
- 选择分类和子分类
- 上传自定义背景图片
- 配置默认运行参数

## 📁 项目结构

```
Vodafone-Pentest-Toolkit/
├── main.py                 # 程序入口
├── core/                   # 核心功能模块
│   ├── app.py              # 主应用程序
│   ├── data_manager.py     # 数据管理
│   └── image_manager.py    # 图片管理
├── ui/                     # 用户界面模块
│   ├── category_view.py    # 分类视图
│   ├── subcategory_view.py # 子分类视图
│   ├── tool_card.py        # 工具卡片组件
│   ├── image_selector.py   # 图片选择器
│   └── tool_config_dialog.py # 工具配置对话框
├── data/                   # 数据存储目录
│   ├── categories.json     # 分类数据
│   └── tools.json          # 工具数据
├── images/                 # 背景图片资源
│   └── ...                 # 默认背景图片
├── resources/              # 资源文件
│   └── icons/              # 分类图标
├── setup.py                # 安装配置
└── README.md               # 项目说明文档
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 开发流程
1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 为新增功能添加文档注释
- 保持代码简洁易读

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub Issues：https://github.com/yourusername/Vodafone-Pentest-Toolkit/issues
- Email：your-email@example.com

## 📊 更新日志

### v1.0.0 (2023-10-15)
- 初始版本发布
- 实现17个工具分类
- 支持工具卡片自定义背景
- 实现工具搜索功能
- 支持工具运行和配置

## 📌 注意事项

1. 本工具仅供合法的渗透测试和安全评估使用
2. 使用本工具进行任何未授权的测试均属非法行为
3. 作者对使用本工具造成的任何后果不承担责任
4. 请在使用前遵守当地法律法规

---

**沃达丰工具箱** - 让渗透测试更高效、更便捷！