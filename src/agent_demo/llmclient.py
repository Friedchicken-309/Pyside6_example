import json
from pathlib import Path
from openai import OpenAI

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config.json"  # 项目根目录下的 config.json


class LLMClient:
    def __init__(self, config_path: Path = CONFIG_PATH) -> None:
        config = self._load_config(config_path)

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
