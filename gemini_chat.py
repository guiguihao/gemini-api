#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini 聊天机器人
提供简洁的命令行聊天界面
"""

import google.generativeai as genai
import os
from datetime import datetime

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GeminiChatBot:
    def __init__(self):
        """初始化聊天机器人"""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 GOOGLE_API_KEY 环境变量")
        
        genai.configure(api_key=self.api_key)
        
        # 从 .env 文件读取模型配置
        model_name = os.getenv("DEFAULT_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(model_name)
        self.chat = None
        self.conversation_count = 0
    
    def start_chat(self, system_prompt=None):
        """开始新的聊天会话"""
        if system_prompt:
            # 使用系统提示初始化
            self.chat = self.model.start_chat(history=[
                {"role": "user", "parts": [system_prompt]},
                {"role": "model", "parts": ["好的，我明白了。我会按照您的要求进行对话。"]}
            ])
        else:
            self.chat = self.model.start_chat(history=[])
        
        self.conversation_count = 0
        print("🤖 聊天会话已开始！")
    
    def send_message(self, message):
        """发送消息"""
        try:
            response = self.chat.send_message(message)
            self.conversation_count += 1
            return response.text
        except Exception as e:
            return f"❌ 发送失败：{e}"
    
    def get_chat_history(self):
        """获取聊天历史"""
        if self.chat and self.chat.history:
            return self.chat.history
        return []
    
    def save_conversation(self, filename=None):
        """保存对话"""
        if not self.chat or not self.chat.history:
            print("📝 没有可保存的对话内容")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Gemini 聊天记录\n")
                f.write(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"对话轮数：{self.conversation_count}\n")
                f.write("="*50 + "\n\n")
                
                for i, content in enumerate(self.chat.history):
                    role = "👤 用户" if content.role == "user" else "🤖 Gemini"
                    f.write(f"{role}：\n{content.parts[0].text}\n\n")
            
            print(f"💾 对话已保存到：{filename}")
        except Exception as e:
            print(f"❌ 保存失败：{e}")

def main():
    """主函数 - 聊天机器人界面"""
    print("🚀 Gemini 聊天机器人")
    print("="*50)
    print("💡 提示：")
    print("   • 输入 'quit' 或 'exit' 退出")
    print("   • 输入 'save' 保存对话")
    print("   • 输入 'clear' 清空对话历史")
    print("   • 输入 'help' 查看帮助")
    print("="*50)
    
    try:
        bot = GeminiChatBot()
        
        # 询问是否使用系统提示
        use_system = input("是否设置聊天角色？(y/N): ").lower().strip()
        if use_system == 'y':
            system_prompt = input("请输入角色设定（例如：你是一个友善的助手）：")
            bot.start_chat(system_prompt)
        else:
            bot.start_chat()
        
        print("\n🎯 开始聊天吧！")
        
        while True:
            try:
                user_input = input("\n👤 您：").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("👋 再见！感谢使用 Gemini 聊天机器人！")
                    break
                elif user_input.lower() == 'save':
                    bot.save_conversation()
                    continue
                elif user_input.lower() == 'clear':
                    bot.start_chat()
                    print("🧹 对话历史已清空")
                    continue
                elif user_input.lower() == 'help':
                    print("\n📖 可用命令：")
                    print("   quit/exit - 退出聊天")
                    print("   save - 保存当前对话")
                    print("   clear - 清空对话历史")
                    print("   help - 显示此帮助")
                    continue
                
                # 发送消息并获取回复
                print("🤖 Gemini：", end="", flush=True)
                response = bot.send_message(user_input)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 检测到 Ctrl+C，正在退出...")
                break
            except Exception as e:
                print(f"\n❌ 发生错误：{e}")
                continue
    
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        print("请确保已正确设置 GOOGLE_API_KEY 环境变量")

if __name__ == "__main__":
    main()
