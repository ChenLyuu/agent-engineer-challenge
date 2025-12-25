# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "openai",
# ]
# ///

import os
import json
import sys
import time
from openai import OpenAI

# ==========================================
# 配置区域
# ==========================================
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")

if not API_KEY:
    print("❌ Error: 请设置环境变量 DEEPSEEK_API_KEY")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


class LongArticleAgent:
    def __init__(self, topic):
        self.topic = topic
        self.outline = []
        self.articles = []

    def step1_generate_outline(self):
        """Step 1: 生成章节大纲"""
        print(f"📋 正在规划主题: {self.topic}...")

        # Prompt: 强制要求输出 JSON 格式的大纲
        prompt = f"""
        请为主题《{self.topic}》生成一个专业的文章大纲。

        【要求】
        1. 生成 12-15 个章节标题。
        2. 章节需要有逻辑递进关系。
        3. 每个章节标题要具体、有吸引力。

        【输出格式】
        必须严格输出以下 JSON 格式（不允许有任何其他文字）：
        {{
          "outline": [
            "章节1标题",
            "章节2标题",
            "章节3标题"
          ]
        }}
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的写作规划师，只输出严格的 JSON 格式。"},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            content = response.choices[0].message.content

            # 容错处理
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()

            data = json.loads(content)

            # 多层容错逻辑：处理 LLM 可能返回的不同 JSON 结构
            if "outline" in data and isinstance(data["outline"], list):
                self.outline = data["outline"]
            elif isinstance(data, list):
                self.outline = data
            elif isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        self.outline = value
                        break

            if not self.outline:
                raise ValueError("未找到有效的大纲列表")

            print(f"✅ 大纲已生成 ({len(self.outline)} 个章节):")
            for i, chapter in enumerate(self.outline, 1):
                print(f"   {i}. {chapter}")

        except Exception as e:
            print(f"❌ 大纲生成失败: {e}")
            sys.exit(1)

    def step2_generate_content_loop(self):
        """Step 2: 循环生成内容，并维护 Context"""
        if not self.outline:
            return

        # 初始化上下文摘要
        previous_summary = f"这是一篇关于《{self.topic}》的专业文章，即将开始第一章的撰写。"

        print("\n🚀 开始撰写正文...")
        for i, chapter in enumerate(self.outline):
            print(f"[{i + 1}/{len(self.outline)}] 正在撰写: {chapter}...")

            # 核心 Prompt: 注入前文摘要 (Context)
            prompt = f"""
            你是一位专业作家，正在撰写一篇关于《{self.topic}》的深度文章。

            【当前任务】
            撰写章节："{chapter}"

            【前文摘要】
            {previous_summary}

            【撰写要求】
            1. 字数：1000 字左右。
            2. 必须承接【前文摘要】的逻辑，确保连贯性。
            3. 不要重复前文已经讲过的内容。
            4. 只输出正文内容，不要输出章节标题。
            """

            try:
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                content = response.choices[0].message.content.strip()
                self.articles.append(f"## {chapter}\n\n{content}")

                # 更新 Context: 使用 LLM 压缩当前章节为摘要
                previous_summary = self._compress_context(content, chapter)

                # 显示进度
                word_count = sum(len(article) for article in self.articles)
                print(f"   ✅ 完成（当前总字数：约 {word_count} 字）")

                # 避免 API 速率限制
                time.sleep(1)

            except Exception as e:
                print(f"⚠️ 章节 {chapter} 生成失败: {e}")

    def _compress_context(self, content: str, chapter_title: str) -> str:
        """
        【核心方法】Context 压缩策略
        使用 LLM 自动生成前文摘要，避免 Token 溢出
        """
        # 如果内容过短，直接返回
        if len(content) < 200:
            return content

        compress_prompt = f"""
        请将以下章节内容压缩为 100 字以内的摘要，保留核心观点。
        章节：{chapter_title}
        内容：{content}
        """

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": compress_prompt}],
                temperature=0.3
            )
            summary = response.choices[0].message.content.strip()
            return f"已完成章节《{chapter_title}》，核心内容：{summary}"
        except Exception:
            return f"已完成章节《{chapter_title}》。"

    def save_result(self):
        if not self.articles:
            print("⚠️ 没有生成任何内容")
            return

        filename = "final_article.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {self.topic}\n\n")
            f.write("\n\n".join(self.articles))
        print(f"\n🎉 文章已保存至 {filename}")


if __name__ == "__main__":
    print(f"🔌 Endpoint: {BASE_URL}")
    print(f"🧠 Model: {MODEL_NAME}\n")

    agent = LongArticleAgent("2025年 AI Agent 对软件开发模式的变革")
    agent.step1_generate_outline()
    agent.step2_generate_content_loop()
    agent.save_result()
