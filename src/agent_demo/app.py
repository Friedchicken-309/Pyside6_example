import sys
from agent_demo.llmclient import LLMClient
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QPlainTextEdit,
    QPushButton,
    QCheckBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWidgets import QSizePolicy

class MainWindow(QMainWindow):
    #--- 界面的初始化---#
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Title")
        self.resize(1080, 720)  # 窗口初始大小（像素）
    #--- 基本布局框定---#
        row = QHBoxLayout()
        function_options = QVBoxLayout()
        main_workspace = QVBoxLayout()
        container = QWidget()
        container.setLayout(row)
        row.addLayout(main_workspace)  # stretch=4：主工作区占据剩余宽度
        row.addLayout(function_options, stretch=1)  # stretch=1：输入框占据剩余宽度
        self.setCentralWidget(container)
    #--- 基本布局框定---#
        self.client = LLMClient()  # 挂到 self 上，槽函数才能访问
    #--- 功能选项布局---#
        
        send_button = QPushButton("GO")
        send_button.setFixedSize(100, 100)
        function_options.addWidget(send_button)
        send_button.clicked.connect(self.translate)
  
    #--- 功能选项布局---#

    #-- 主工作区布局---#
        self.input_text = QPlainTextEdit()
        self.input_text.setPlaceholderText("请输入原文")
        self.input_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_workspace.addWidget(self.input_text)


        self.output_text = QPlainTextEdit()
        self.output_text.setPlaceholderText("等待输出")
        self.output_text.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_workspace.addWidget(self.output_text)

    #-- 主工作区布局---#

    #---槽函数---#
    def translate(self) -> None:
        # 获取输入文本
        text = self.input_text.toPlainText()
        # 发送请求
        if text.strip():  # 检查输入是否为空（含纯空白）
            response = self.client.chat(text)
            # 显示输出文本
            self.output_text.setPlainText(response)


    #---槽函数---#


BASE_DIR = Path(__file__).resolve().parent
QSS_PATH = BASE_DIR / "style.qss"  # 与 llmclient.py 的 CONFIG_PATH 同款写法

def load_qss(path)-> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet(load_qss(QSS_PATH))  # 加载样式表
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
