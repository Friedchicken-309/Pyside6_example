import sys
import threading

from agent_demo.llmclient import LLMClient, resource_path

from PySide6.QtCore import QObject, Signal
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


class ChatWorker(QObject):
    """在子线程里执行网络请求，结果通过信号送回 UI 线程。"""
    finished = Signal(str)  # 请求成功，携带模型回复
    failed = Signal(str)    # 请求失败，携带错误信息

    def __init__(self, client: LLMClient, text: str) -> None:
        super().__init__()
        self.client = client
        self.text = text

    def run(self) -> None:
        """这个方法在子线程里执行，不要在这里直接碰任何界面控件。"""
        try:
            response = self.client.chat(self.text)
            self.finished.emit(response)  # 跨线程 emit 会自动排队到 UI 线程执行
        except Exception as exc:
            self.failed.emit(str(exc))


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
        
        self.send_button = QPushButton("GO")
        self.send_button.setFixedSize(100, 100)
        function_options.addWidget(self.send_button)
        self.send_button.clicked.connect(self.translate)
  
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
        if not text.strip():  # 检查输入是否为空（含纯空白）
            return
        # UI 线程只负责发起：禁用按钮，立即返回，界面不卡
        self.send_button.setEnabled(False)
        self.output_text.setPlainText("翻译中…")

        self.worker = ChatWorker(self.client, text)  # 持有引用，防止子线程被垃圾回收
        self.worker.finished.connect(self.on_chat_finished)
        self.worker.failed.connect(self.on_chat_failed)
        threading.Thread(target=self.worker.run, daemon=True).start()

    def on_chat_finished(self, response: str) -> None:
        """子线程完成后由信号触发，此时已在 UI 线程，可以安全操作控件。"""
        self.output_text.setPlainText(response)
        self.send_button.setEnabled(True)

    def on_chat_failed(self, message: str) -> None:
        self.output_text.setPlainText(f"请求失败：{message}")
        self.send_button.setEnabled(True)
    #---槽函数---#


QSS_PATH = resource_path("style.qss")  # 开发时取源码目录，打包后取解压目录或 exe 旁

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
