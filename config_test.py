#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置验证脚本
验证所有文件都正确使用 .env 配置
"""

import os
from dotenv import load_dotenv

def test_env_configuration():
    """测试 .env 配置"""
    print("🔧 .env 配置验证")
    print("="*50)
    
    # 加载 .env 文件
    load_dotenv()
    
    # 显示所有配置
    configs = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY", "未设置"),
        "DEFAULT_MODEL": os.getenv("DEFAULT_MODEL", "未设置"),
        "DEFAULT_TEMPERATURE": os.getenv("DEFAULT_TEMPERATURE", "未设置"),
        "DEFAULT_MAX_TOKENS": os.getenv("DEFAULT_MAX_TOKENS", "未设置"),
        "DEFAULT_TOP_P": os.getenv("DEFAULT_TOP_P", "未设置"),
        "DEFAULT_TOP_K": os.getenv("DEFAULT_TOP_K", "未设置"),
        "SAFETY_LEVEL": os.getenv("SAFETY_LEVEL", "未设置"),
    }
    
    print("📋 当前配置:")
    for key, value in configs.items():
        if "API_KEY" in key and value != "未设置":
            print(f"   {key}: {value[:8]}...")
        else:
            print(f"   {key}: {value}")
    
    # 测试各个模块能否正确读取配置
    print("\n🧪 模块配置测试:")
    
    try:
        from gemini_advanced import GeminiAdvanced
        gemini = GeminiAdvanced()
        print("✅ GeminiAdvanced 配置读取成功")
        print(f"   模型: {gemini.model_name}")
        print(f"   温度: {gemini.default_config['temperature']}")
        print(f"   最大tokens: {gemini.default_config['max_output_tokens']}")
    except Exception as e:
        print(f"❌ GeminiAdvanced 配置读取失败: {e}")
    
    try:
        from gemini_chat import GeminiChatBot
        chat_bot = GeminiChatBot()
        print("✅ GeminiChatBot 配置读取成功")
    except Exception as e:
        print(f"❌ GeminiChatBot 配置读取失败: {e}")
    
    try:
        from image_prompt_generator import SimpleImagePromptGenerator
        prompt_gen = SimpleImagePromptGenerator()
        print("✅ SimpleImagePromptGenerator 配置读取成功")
    except Exception as e:
        print(f"❌ SimpleImagePromptGenerator 配置读取失败: {e}")

def test_functionality():
    """测试基本功能"""
    print("\n🎯 功能测试:")
    
    try:
        from gemini_advanced import GeminiAdvanced
        gemini = GeminiAdvanced()
        
        # 简单测试
        result = gemini.generate_text("测试", max_output_tokens=50)
        if "生成失败" not in result:
            print("✅ 文本生成功能正常")
        else:
            print(f"⚠️ 文本生成有问题: {result}")
            
        # 翻译测试
        result = gemini.translate_text("Hello", "中文")
        if "生成失败" not in result:
            print("✅ 翻译功能正常")
        else:
            print(f"⚠️ 翻译功能有问题: {result}")
            
    except Exception as e:
        print(f"❌ 功能测试失败: {e}")

if __name__ == "__main__":
    test_env_configuration()
    test_functionality()
    print("\n🎉 配置验证完成!")
