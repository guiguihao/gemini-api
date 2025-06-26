#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 功能测试脚本
"""

import sys
import traceback
from gemini_advanced import GeminiAdvanced

def test_function(test_name, test_func):
    """测试单个功能"""
    print(f"\n🧪 测试: {test_name}")
    print("-" * 40)
    try:
        result = test_func()
        if result:
            print(f"✅ 成功: {result[:100]}..." if len(str(result)) > 100 else f"✅ 成功: {result}")
        else:
            print("✅ 成功执行（无返回值）")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        print(f"🔍 错误详情: {traceback.format_exc()}")
        return False

def main():
    print("🚀 Gemini API 完整功能测试")
    print("=" * 60)
    
    # 初始化
    try:
        gemini = GeminiAdvanced()
        print("✅ GeminiAdvanced 初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        return
    
    # 测试项目列表
    tests = [
        ("配置显示", lambda: gemini.show_config()),
        ("模型列表", lambda: gemini.list_available_models()),
        ("简单文本生成", lambda: gemini.generate_text("Hello", max_output_tokens=50)),
        ("翻译功能", lambda: gemini.translate_text("Good morning", "中文")),
        ("文本摘要", lambda: gemini.summarize_text("人工智能是一项革命性的技术。", 20)),
        ("代码生成", lambda: gemini.generate_code("打印Hello World", "Python")),
        ("创意写作", lambda: gemini.creative_writing("阳光", "短诗")),
        ("多轮对话", lambda: test_chat(gemini)),
    ]
    
    # 执行测试
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_function(test_name, test_func):
            passed += 1
    
    # 总结
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    if passed == total:
        print("🎉 所有功能测试通过！")
    else:
        print(f"⚠️ 有 {total - passed} 项测试失败")

def test_chat(gemini):
    """测试多轮对话"""
    chat = gemini.start_chat()
    response1 = gemini.chat_with_history("你好", chat)
    response2 = gemini.chat_with_history("我叫小明", chat)
    return f"对话1: {response1[:50]}... 对话2: {response2[:50]}..."

if __name__ == "__main__":
    main()
