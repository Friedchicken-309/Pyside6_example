from agent_demo.llmclient import LLMClient

def main():
    client = LLMClient()
    while True:
        text = input("请输入文本（输入 'exit' 退出）：")
        if text.lower() == "exit":
            break
        response = client.chat(text)
        print("模型回复：", response)

if __name__ == "__main__":
    main()
