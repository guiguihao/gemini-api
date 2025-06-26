#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 .env 文件配置
"""

import os
from dotenv import load_dotenv

def test_env_config():
    """测试环境变量配置"""
    print("🧪 测试 .env 文件配置")
    print("="*40)
    
    # 显示当前工作目录
    print(f"📁 当前目录: {os.getcwd()}")
    
    # 检查 .env 文件是否存在
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ 找到 .env 文件: {env_file}")
        
        # 读取并显示 .env 文件内容（隐藏敏感信息）
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.strip().split('\n')
            print("\n📄 .env 文件内容:")
            for line in lines:
                if line.strip() and not line.strip().startswith('#'):
                    if 'API_KEY' in line:
                        key, value = line.split('=', 1)
                        print(f"   {key}=***{value[-4:] if len(value) > 4 else '***'}")
                    else:
                        print(f"   {line}")
                elif line.strip().startswith('#'):
                    print(f"   {line}")
    else:
        print(f"❌ 未找到 .env 文件: {env_file}")
        return False
    
    # 测试环境变量加载前
    print(f"\n🔍 加载前 GOOGLE_API_KEY: {os.getenv('GOOGLE_API_KEY', '未设置')}")
    
    # 加载 .env 文件
    print("\n🔄 正在加载 .env 文件...")
    load_result = load_dotenv()
    print(f"📊 load_dotenv() 结果: {load_result}")
    
    # 测试环境变量加载后
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print(f"✅ 加载后 GOOGLE_API_KEY: ***{api_key[-4:] if len(api_key) > 4 else '***'}")
        print(f"📏 API Key 长度: {len(api_key)} 字符")
    else:
        print("❌ 加载后 GOOGLE_API_KEY: 仍未设置")
        return False
    
    # 测试其他配置
    print("\n🔧 其他配置:")
    model = os.getenv('DEFAULT_MODEL', '未设置')
    temp = os.getenv('DEFAULT_TEMPERATURE', '未设置')
    tokens = os.getenv('DEFAULT_MAX_TOKENS', '未设置')
    
    print(f"   DEFAULT_MODEL: {model}")
    print(f"   DEFAULT_TEMPERATURE: {temp}")
    print(f"   DEFAULT_MAX_TOKENS: {tokens}")
    
    return True

def test_gemini_connection():
    """测试 Gemini API 连接"""
    print("\n🤖 测试 Gemini API 连接")
    print("="*40)
    
    try:
        import google.generativeai as genai
        
        # 加载环境变量
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if not api_key:
            print("❌ API 密钥未找到")
            return False
        
        # 配置 API
        genai.configure(api_key=api_key)
        
        # 尝试列出模型
        print("📋 正在获取可用模型...")
        models = list(genai.list_models())
        
        if models:
            print(f"✅ 成功连接！找到 {len(models)} 个模型")
            print("🤖 前几个可用模型:")
            for i, model in enumerate(models[:3]):
                if 'generateContent' in model.supported_generation_methods:
                    print(f"   • {model.name}")
        else:
            print("⚠️ 连接成功但未找到模型")
        
        # 测试简单的文本生成
        print("\n🧪 测试文本生成...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("请说 '你好'")
        print(f"✅ 测试成功！回复: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

if __name__ == "__main__":
    print("🔬 Gemini API 环境配置测试")
    print("="*50)
    
    # 测试 .env 文件
    env_ok = test_env_config()
    
    if env_ok:
        # 测试 API 连接
        api_ok = test_gemini_connection()
        
        if api_ok:
            print("\n🎉 所有测试通过！环境配置正确。")
        else:
            print("\n❌ API 连接测试失败。")
    else:
        print("\n❌ .env 文件配置测试失败。")
    
    print("\n" + "="*50)
