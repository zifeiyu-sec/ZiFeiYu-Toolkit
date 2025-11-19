from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                            QToolBar, QAction, QMessageBox, QInputDialog, QApplication, 
                            QLineEdit, QActionGroup, QMenu, QToolButton, QStatusBar, 
                            QProgressBar, QLabel)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize, QSettings
import os
import sys

# 导入自定义模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.data_manager import DataManager
from core.image_manager import ImageManager
from ui.category_view import CategoryView
from ui.subcategory_view import SubcategoryView
from ui.tool_card import ToolCardContainer
from ui.image_selector import ImageSelectorDialog
from ui.tool_config_dialog import ToolConfigDialog

class PentestToolManager(QMainWindow):
    def __init__(self, config_dir=None):
        super().__init__()
        # 设置应用程序信息
        self.app_name = "子非鱼工具箱"
        self.version = "1.0.0"
        
        # 初始化管理器
        self.data_manager = DataManager(config_dir=config_dir)
        self.image_manager = ImageManager(config_dir=config_dir)
        
        # 创建默认背景图片
        self.image_manager.create_default_backgrounds()
        
        # 当前选中的分类
        self.current_category = None
        
        # 初始化UI
        self.init_ui()
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle(f"{self.app_name} - v{self.version}")
        self.setGeometry(100, 100, 1500, 900)
        # 固定窗口大小，不允许缩放
        self.setFixedSize(1200, 800)
        
        # 创建主组件
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.create_statusbar()
        self.create_main_widget()
        
        # 应用样式
        self.apply_styles()
    
    def create_actions(self):
        """创建动作"""
        # 文件操作
        self.new_tool_action = QAction("新建工具", self)
        self.new_tool_action.setShortcut("Ctrl+N")
        self.new_tool_action.triggered.connect(self.on_new_tool)
        
        self.exit_action = QAction("退出", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        
        # 分类操作
        self.new_category_action = QAction("新建分类", self)
        self.new_category_action.triggered.connect(self.on_new_category)
        
        self.new_subcategory_action = QAction("新建子分类", self)
        self.new_subcategory_action.triggered.connect(self.on_new_subcategory)
        
        self.delete_category_action = QAction("删除分类", self)
        self.delete_category_action.triggered.connect(self.on_delete_category)
        
        self.delete_subcategory_action = QAction("删除子分类", self)
        self.delete_subcategory_action.triggered.connect(self.on_delete_subcategory)
        
        # 视图操作
        self.refresh_action = QAction("刷新", self)
        self.refresh_action.setShortcut("F5")
        self.refresh_action.triggered.connect(self.refresh_all)
        
        # 帮助
        self.about_action = QAction("关于", self)
        self.about_action.triggered.connect(self.on_about)
    
    def create_menus(self):
        """创建菜单"""
        # 文件菜单
        file_menu = self.menuBar().addMenu("文件")
        file_menu.addAction(self.new_tool_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)
        
        # 视图菜单
        view_menu = self.menuBar().addMenu("视图")
        view_menu.addAction(self.refresh_action)
        
        # 帮助菜单
        help_menu = self.menuBar().addMenu("帮助")
        help_menu.addAction(self.about_action)
    
    def create_toolbars(self):
        """创建工具栏"""
        # 主工具栏
        main_toolbar = QToolBar("主工具栏", self)
        main_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(main_toolbar)
        
        # 添加工具按钮
        main_toolbar.addAction(self.new_tool_action)
        main_toolbar.addSeparator()
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索工具...")
        self.search_input.setMaximumWidth(200)
        self.search_input.textChanged.connect(self.on_search)
        main_toolbar.addWidget(QLabel("搜索: "))
        main_toolbar.addWidget(self.search_input)
        
        # 右侧填充
        main_toolbar.addSeparator()
        main_toolbar.addWidget(QWidget())
        
        # 刷新按钮
        main_toolbar.addAction(self.refresh_action)
    
    def create_statusbar(self):
        """创建状态栏"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # 显示工具数量
        self.tool_count_label = QLabel("工具数量: 0")
        self.statusBar.addPermanentWidget(self.tool_count_label)
        
        # 显示状态信息
        self.statusBar.showMessage("就绪")
    
    def create_main_widget(self):
        """创建主窗口组件"""
        # 中心部件
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #1a1a1a;")
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧一级分类视图
        self.category_view = CategoryView(self.data_manager)
        self.category_view.category_selected.connect(self.on_category_selected)
        # 连接右键菜单信号
        self.category_view.new_category_requested.connect(self.on_new_category)
        self.category_view.new_subcategory_requested.connect(self.on_new_subcategory)
        self.category_view.delete_category_requested.connect(self.on_delete_category)
        splitter.addWidget(self.category_view)
        
        # 中间二级分类视图
        self.subcategory_view = SubcategoryView(self.data_manager)
        self.subcategory_view.subcategory_selected.connect(self.on_subcategory_selected)
        # 连接右键菜单信号
        self.subcategory_view.new_subcategory_requested.connect(self.on_new_subcategory)
        self.subcategory_view.delete_subcategory_requested.connect(self.on_delete_subcategory)
        splitter.addWidget(self.subcategory_view)
        
        # 右侧工具卡片容器
        right_widget = QWidget()
        right_widget.setStyleSheet("background-color: #1a1a1a;")
        right_layout = QVBoxLayout(right_widget)
        
        # 顶部信息栏
        info_bar = QWidget()
        info_bar.setStyleSheet("background-color: #000000; border-bottom: 2px solid #00ff00;")
        info_layout = QHBoxLayout(info_bar)
        
        self.category_info_label = QLabel("所有工具")
        self.category_info_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #90ee90;")
        
        info_layout.addWidget(self.category_info_label)
        info_layout.addStretch()
        
        # 只使用网格视图，移除视图切换功能
        
        right_layout.addWidget(info_bar)
        
        # 右侧工具卡片容器
        self.tool_container = ToolCardContainer()
        self.tool_container.deleted.connect(self.on_delete_tool)
        self.tool_container.edit_requested.connect(self.on_edit_tool)
        self.tool_container.new_tool_requested.connect(self.on_new_tool)
        
        right_layout.addWidget(self.tool_container, 1)
        
        splitter.addWidget(right_widget)
        
        # 设置初始大小
        splitter.setSizes([200, 180, 820])
        
        main_layout.addWidget(splitter, 1)
    
    def apply_styles(self):
        """应用样式 - 简约高级的玻璃主题"""
        # 设置全局样式表 - 玻璃主题
        style_sheet = """
        /* 主窗口样式 */
        QMainWindow {
            background-color: #1a1a2e;
            border: none;
        }
        
        /* 菜单栏样式 */
        QMenuBar {
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        QMenuBar::item {
            padding: 5px 10px;
        }
        
        QMenuBar::item:selected {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }
        
        /* 弹出菜单样式 */
        QMenu {
            background: rgba(26, 26, 46, 0.95);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 5px;
        }
        
        QMenu::item {
            padding: 8px 20px;
            border-radius: 4px;
        }
        
        QMenu::item:selected {
            background: rgba(103, 232, 249, 0.2);
        }
        
        /* 工具栏样式 */
        QToolBar {
            background: rgba(255, 255, 255, 0.05);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px;
            spacing: 12px;
        }
        
        /* 工具栏按钮 */
        QToolButton {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 8px 16px;
            border-radius: 8px;
            color: #ffffff;
            font-weight: 500;
        }
        
        QToolButton:hover {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(103, 232, 249, 0.5);
        }
        
        QToolButton:pressed {
            background: rgba(103, 232, 249, 0.2);
        }
        
        /* 状态栏 */
        QStatusBar {
            background: rgba(255, 255, 255, 0.05);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 12px;
        }
        
        /* 分割器 */
        QSplitter {
            background-color: #1a1a2e;
        }
        
        QSplitter::handle {
            background: rgba(255, 255, 255, 0.1);
            width: 6px;
            border-radius: 3px;
        }
        
        QSplitter::handle:hover {
            background: rgba(103, 232, 249, 0.3);
        }
        
        /* 输入框 */
        QLineEdit {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            color: #ffffff;
            font-size: 13px;
        }
        
        QLineEdit:focus {
            border: 1px solid rgba(103, 232, 249, 0.5);
            background: rgba(255, 255, 255, 0.08);
            outline: none;
        }
        
        /* 按钮 */
        QPushButton {
            background: rgba(103, 232, 249, 0.1);
            border: 1px solid rgba(103, 232, 249, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
            color: #ffffff;
            font-weight: 500;
            font-size: 13px;
        }
        
        QPushButton:hover {
            background: rgba(103, 232, 249, 0.2);
            border: 1px solid rgba(103, 232, 249, 0.5);
        }
        
        QPushButton:pressed {
            background: rgba(103, 232, 249, 0.3);
        }
        
        QPushButton:default {
            border: 1px solid rgba(103, 232, 249, 0.5);
        }
        
        /* 分组框 */
        QGroupBox {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            margin-top: 10px;
            padding: 15px;
        }
        
        QGroupBox::title {
            background-color: transparent;
            color: #ffffff;
            font-weight: 600;
            font-size: 14px;
            padding: 0 10px;
            margin-top: -10px;
        }
        
        /* 标签 */
        QLabel {
            color: #ffffff;
            font-size: 13px;
        }
        
        /* 文本编辑框 */
        QTextEdit {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 10px;
            color: #ffffff;
            font-size: 13px;
        }
        
        QTextEdit:focus {
            border: 1px solid rgba(103, 232, 249, 0.5);
            background: rgba(255, 255, 255, 0.08);
            outline: none;
        }
        
        /* 下拉组合框 */
        QComboBox {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            color: #ffffff;
            font-size: 13px;
            min-height: 30px;
        }
        
        QComboBox:hover {
            border-color: rgba(103, 232, 249, 0.3);
        }
        
        QComboBox:focus {
            border-color: rgba(103, 232, 249, 0.5);
            background-color: rgba(255, 255, 255, 0.08);
        }
        
        QComboBox QAbstractItemView {
            background-color: rgba(26, 26, 46, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            color: #ffffff;
        }
        
        QComboBox QAbstractItemView::item {
            padding: 8px 12px;
            min-height: 25px;
        }
        
        QComboBox QAbstractItemView::item:hover {
            background-color: rgba(103, 232, 249, 0.2);
        }
        
        QComboBox QAbstractItemView::item:selected {
            background-color: rgba(103, 232, 249, 0.3);
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: url(:/qt-project.org/styles/commonstyle/images/down-underline-24.png);
            width: 16px;
            height: 16px;
        }
        
        /* 复选框 */
        QCheckBox {
            color: #ffffff;
            font-size: 13px;
            spacing: 8px;
        }
        
        QCheckBox::indicator {
            width: 18px;
            height: 18px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.05);
        }
        
        QCheckBox::indicator:checked {
            background: rgba(103, 232, 249, 0.3);
            border-color: rgba(103, 232, 249, 0.5);
            image: url(:/qt-project.org/styles/commonstyle/images/checkindicator.png);
        }
        
        /* 旋转框 */
        QSpinBox {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 6px;
            color: #90ee90;
            font-size: 13px;
        }
        
        QSpinBox:focus {
            border: 1px solid #4caf50;
            outline: none;
        }
        
        /* 对话框样式 */
        QDialog {
            background-color: #1a1a2e;
            border-radius: 10px;
            color: #ffffff;
        }
        
        /* 输入对话框样式 */
        QInputDialog {
            background-color: #1a1a2e;
            color: #ffffff;
        }
        
        QInputDialog QLabel {
            color: #ffffff;
        }
        
        QInputDialog QLineEdit {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            color: #ffffff;
            font-size: 13px;
        }
        
        QInputDialog QPushButton {
            background: rgba(103, 232, 249, 0.1);
            border: 1px solid rgba(103, 232, 249, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
            color: #ffffff;
            font-weight: 500;
            font-size: 13px;
        }
        
        QInputDialog QPushButton:hover {
            background: rgba(103, 232, 249, 0.2);
            border: 1px solid rgba(103, 232, 249, 0.5);
        }
        
        QInputDialog QPushButton:pressed {
            background: rgba(103, 232, 249, 0.3);
        }
        
        /* 滚动条 */
        QScrollBar:vertical {
            background-color: #f5f2eb;
            width: 10px;
            border-radius: 5px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 #d4cbc1, stop:1 #c9b8a5);
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                      stop:0 #c9b8a5, stop:1 #b8a38c);
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            background: none;
            height: 0;
        }
        
        /* 列表视图 */
        QListWidget {
            background-color: #faf8f5;
            border: 1px solid #e6e0d8;
            border-radius: 6px;
            padding: 5px;
        }
        """
        self.setStyleSheet(style_sheet)
    
    def on_category_selected(self, category_id):
        """处理一级分类选择"""
        self.current_category = category_id
        
        # 加载并显示该分类下的子分类
        self.subcategory_view.load_subcategories(category_id)
        
        # 更新分类信息标签
        categories = self.data_manager.load_categories()
        category_name = "所有工具"
        for category in categories:
            if isinstance(category, dict) and category.get('id') == category_id:
                category_name = category.get('name', "未知分类")
                break
        
        self.category_info_label.setText(category_name)
        
        # 加载该分类下的所有工具（不区分子分类）
        tools = self.data_manager.get_tools_by_category(category_id)
        self.tool_container.display_tools(tools)
        self.refresh_tool_count()
    
    def on_subcategory_selected(self, category_id, subcategory_id):
        """处理二级分类选择"""
        # 更新分类信息标签
        categories = self.data_manager.load_categories()
        category_name = "所有工具"
        subcategory_name = ""
        
        # 查找当前分类和子分类
        for category in categories:
            if isinstance(category, dict) and category.get('id') == category_id:
                category_name = category.get('name', "未知分类")
                
                # 如果有子分类ID，查找子分类名称
                if subcategory_id is not None and 'subcategories' in category:
                    for subcategory in category['subcategories']:
                        if isinstance(subcategory, dict) and subcategory.get('id') == subcategory_id:
                            subcategory_name = f" - {subcategory.get('name', '未知子分类')}"
                            break
                break
        
        self.category_info_label.setText(category_name + subcategory_name)
        
        # 加载并显示该子分类下的工具
        tools = self.data_manager.get_tools_by_category(category_id, subcategory_id)
        self.tool_container.display_tools(tools)
        self.refresh_tool_count()
    
    def on_new_tool(self):
        """处理新建工具"""
        # 获取所有分类
        categories_data = self.data_manager.load_categories()
        if not categories_data:
            QMessageBox.warning(self, "警告", "请先创建分类！")
            return
        
        # 格式化分类数据，确保每个分类都有subcategories字段
        formatted_categories = []
        for cat in categories_data:
            # 确保cat是字典格式
            if isinstance(cat, dict):
                # 添加subcategories字段（如果不存在）
                if "subcategories" not in cat:
                    cat["subcategories"] = []
                formatted_categories.append(cat)
        
        # 打开工具配置对话框
        dialog = ToolConfigDialog(categories=formatted_categories, parent=self)
        if dialog.exec_():
            # 获取工具数据
            tool_data = dialog.get_tool_data()
            
            # 保存工具
            new_tool = self.data_manager.add_tool(tool_data)
            if new_tool:
                QMessageBox.information(self, "成功", "工具创建成功！")
                # 刷新当前视图
                self.refresh_current_view()
            else:
                QMessageBox.warning(self, "失败", "工具创建失败！")
    
    def on_edit_tool(self, tool_data):
        """处理编辑工具"""
        # 获取工具ID
        tool_id = tool_data['id']
        # 获取最新工具信息
        tool = self.data_manager.get_tool_by_id(tool_id)
        if not tool:
            return
        
        # 获取所有分类
        categories = self.data_manager.get_all_categories()
        
        # 打开工具配置对话框
        dialog = ToolConfigDialog(tool_data=tool, categories=categories, parent=self)
        if dialog.exec_():
            # 获取更新后的工具数据
            updated_tool = dialog.get_tool_data()
            
            # 更新工具
            if self.data_manager.update_tool(updated_tool['id'], updated_tool):
                QMessageBox.information(self, "成功", "工具更新成功！")
                self.refresh_current_view()
            else:
                QMessageBox.warning(self, "失败", "工具更新失败！")
    
    def on_edit_background(self, tool_data):
        """处理编辑背景图片"""
        # 获取工具ID
        tool_id = tool_data['id']
        # 获取工具信息
        tool = self.data_manager.get_tool_by_id(tool_id)
        if not tool:
            return
        
        # 打开图片选择对话框
        dialog = ImageSelectorDialog(self.image_manager, tool.get("background_image", ""), self)
        if dialog.exec_():
            selected_image = dialog.get_selected_image()
            
            # 更新工具背景
            tool["background_image"] = selected_image
            
            if self.data_manager.update_tool(tool_id, tool):
                self.refresh_current_view()
    
    def on_delete_tool(self, tool_id):
        """处理删除工具"""
        # 调用数据管理器删除工具
        if self.data_manager.delete_tool(tool_id):
            QMessageBox.information(self, "成功", "工具删除成功！")
            self.refresh_current_view()
        else:
            QMessageBox.warning(self, "失败", "工具删除失败！")
    
    def on_new_category(self):
        """处理新建分类"""
        category_name, ok = QInputDialog.getText(self, "新建分类", "请输入分类名称:")
        if ok and category_name:
            # 创建分类
            category = {
                "name": category_name,
                "icon": "default_icon",
                "subcategories": []
            }
            
            # 保存分类
            if self.data_manager.add_category(category):
                QMessageBox.information(self, "成功", "分类创建成功！")
                self.category_view.refresh()
            else:
                QMessageBox.warning(self, "失败", "分类创建失败！")
    
    def on_new_subcategory(self):
        """处理新建子分类"""
        # 获取当前选中的分类
        current_category = self.category_view.current_category
        # 检查current_category是否为整数ID或None
        if not current_category:
            QMessageBox.warning(self, "警告", "请先选择一个主分类！")
            return
        
        # 获取子分类名称
        subcategory_name, ok = QInputDialog.getText(self, "新建子分类", "请输入子分类名称:")
        if ok and subcategory_name:
            # 创建子分类
            subcategory = {
                "name": subcategory_name
            }
            
            # 保存子分类 - current_category已经是整数ID
            if self.data_manager.add_subcategory(current_category, subcategory):
                QMessageBox.information(self, "成功", "子分类创建成功！")
                self.category_view.refresh()
            else:
                QMessageBox.warning(self, "失败", "子分类创建失败！")
    

    
    def on_delete_category(self):
        """处理删除分类"""
        # 获取当前选中的分类
        current_category = self.category_view.current_category
        current_subcategory = self.subcategory_view.current_subcategory
        
        # 如果选中了子分类，不能直接删除主分类
        if current_subcategory:
            QMessageBox.warning(self, "警告", "请先取消选择子分类，然后再删除主分类！")
            return
        
        if not current_category:
            QMessageBox.warning(self, "警告", "请先选择一个要删除的主分类！")
            return
        
        # 弹出确认对话框
        reply = QMessageBox.question(self, "确认删除", 
                                    f"确定要删除选中的分类吗？\n删除前请确保该分类下没有工具和子分类。",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 调用数据管理器删除分类
            success, message = self.data_manager.delete_category(current_category)
            if success:
                QMessageBox.information(self, "成功", "分类删除成功！")
                self.category_view.refresh()
                # 重置当前选中状态
                self.current_category = None
                self.tool_container.display_tools([])
            else:
                QMessageBox.warning(self, "失败", message)
    
    def on_delete_subcategory(self):
        """处理删除子分类"""
        # 获取当前选中的子分类
        current_subcategory = self.subcategory_view.current_subcategory
        
        if not current_subcategory:
            QMessageBox.warning(self, "警告", "请先选择一个要删除的子分类！")
            return
        
        # 弹出确认对话框
        reply = QMessageBox.question(self, "确认删除", 
                                    f"确定要删除选中的子分类吗？\n删除前请确保该子分类下没有工具。",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # 调用数据管理器删除子分类
            success, message = self.data_manager.delete_subcategory(current_subcategory)
            if success:
                QMessageBox.information(self, "成功", "子分类删除成功！")
                self.category_view.refresh()
                # 重置当前选中状态
                self.subcategory_view.current_subcategory = None
                # 显示当前分类下的所有工具
                self.on_category_selected(self.category_view.current_category)
            else:
                QMessageBox.warning(self, "失败", message)
    
    # 移除视图切换功能，只保留网格视图
    
    def on_search(self, text):
        """处理搜索"""
        # 根据当前分类和搜索文本过滤工具
        tools = []
        if self.current_category:
            tools = self.data_manager.get_tools_by_category(self.current_category)
        else:
            tools = self.data_manager.get_all_tools()
        
        # 过滤工具
        filtered_tools = [tool for tool in tools if text.lower() in tool["name"].lower() or 
                          ("description" in tool and text.lower() in tool["description"].lower())]
        
        # 更新工具列表
        self.tool_container.set_tools(filtered_tools)
        self.refresh_tool_count()
    
    def on_about(self):
        """处理关于对话框"""
        QMessageBox.about(self, "关于", 
                         f"{self.app_name}\n版本: {self.version}\n\n用于管理渗透测试工具的图形化界面应用。")
    
    def refresh_all(self):
        """刷新所有视图"""
        self.category_view.refresh()
        self.refresh_current_view()
    
    def refresh_current_view(self):
        """刷新当前视图"""
        # 如果有选中的分类，重新加载该分类下的工具
        if self.current_category:
            # 传递正确的参数给on_category_selected
            self.on_category_selected(self.current_category)
        else:
            # 否则加载所有工具（使用load_tools方法）
            tools = self.data_manager.load_tools()
            self.tool_container.display_tools(tools)
        
        self.refresh_tool_count()
    
    def refresh_tool_count(self):
        """刷新工具数量显示"""
        # 从数据管理器获取当前显示的工具数量
        if self.current_category:
            # 如果有选中的分类，获取该分类下的工具数量
            tools = self.data_manager.get_tools_by_category(self.current_category, None)
        else:
            # 否则获取所有工具数量
            tools = self.data_manager.load_tools()
        
        tool_count = len(tools)
        self.tool_count_label.setText(f"工具数量: {tool_count}")
    
    def show_status_message(self, message, timeout=2000):
        """显示状态栏消息"""
        self.statusBar.showMessage(message, timeout)
    
    def closeEvent(self, event):
        """处理窗口关闭事件"""
        reply = QMessageBox.question(self, '确认', '确定要退出吗？',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# 主函数
if __name__ == "__main__":
    # 确保中文显示正常
    if hasattr(Qt, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # 获取当前脚本所在目录的父目录，即项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建主窗口，明确传递项目根目录作为配置目录
    window = PentestToolManager(config_dir=project_root)
    window.show()
    
    # 加载初始工具列表
    window.refresh_current_view()
    
    sys.exit(app.exec_())