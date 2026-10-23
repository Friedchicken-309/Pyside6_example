import json
import sys
from pathlib import Path

from openai import OpenAI


def resource_path(name: str) -> Path:
    """定位资源文件。

    开发运行：取模块所在目录；
    打包运行：优先 exe 旁边的同名文件（改配置不用重新打包），否则用打包进 exe 的副本。
    """
    if getattr(sys, "frozen", False):
        beside_exe = Path(sys.executable).resolve().parent / name
        if beside_exe.exists():
            return beside_exe
        return Path(sys._MEIPASS) / name  # PyInstaller 单文件运行时的解压目录
    return Path(__file__).resolve().parent / name


class LLMClient:
    def __init__(self, config_path: Path | None = None) -> None:
        config = self._load_config(config_path or resource_path("config.json"))

        # 获取API——KEY
        self.api_key = config.get("api_key")
        if not self.api_key:
            raise ValueError(
                "未找到 API Key：请在 config.json 的 api_key 字段或环境变量 OPENAI_API_KEY 中提供。"
            )
        self.base_url = config.get("base_url")
        self.model = config.get("model")

        self.client = OpenAI(api_key=self.api_key,
                              base_url=self.base_url)

    def chat(self, text: str) -> str:
        """发送一条用户消息，返回模型回复的文本。"""
        response = self.client.responses.create(
            model=self.model,
            instructions="你是一个翻译助手，收到的文本如果是中文，就翻译成英文；如果是英文，就翻译成中文\n保留原文的专有名词和术语\n不要解释\n不要输出任何多余的内容\n只输出翻译后的文本",
            input=text,
        )
        return response.output_text


    @staticmethod
    def _load_config(path: Path) -> dict:
        """读取本地 JSON 配置文件；文件不存在时返回空字典。"""
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
