# 导入所需的库
import google.generativeai as genai
import os

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("💡 提示：安装 python-dotenv 以支持 .env 文件: pip install python-dotenv")

# 配置您的 API 密钥
# 建议将 API 密钥存储在环境变量中，以提高安全性
# 您可以在 Google AI Studio 或 Google Cloud Platform 中获取 API 密钥
# 例如：export GOOGLE_API_KEY='YOUR_API_KEY'

# 从环境变量中读取 API 密钥
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("错误：请设置 GOOGLE_API_KEY 环境变量。")
    # 或者在这里直接设置您的 API 密钥（不推荐用于生产环境）
    # API_KEY = "YOUR_API_KEY"
    exit()

# 初始化 Gemini 客户端
genai.configure(api_key=API_KEY)

# 列出可用的模型
print("可用的 Gemini 模型：")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")

# 使用 .env 文件中的模型配置
model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
model = genai.GenerativeModel(model_name)

# 从 .env 文件读取生成参数配置
generation_config = {
    "temperature": float(os.getenv("DEFAULT_TEMPERATURE", "0.7")),
    "top_p": float(os.getenv("DEFAULT_TOP_P", "0.8")),
    "top_k": int(os.getenv("DEFAULT_TOP_K", "40")),
    "max_output_tokens": int(os.getenv("DEFAULT_MAX_TOKENS", "1000")),
}

def generate_text(prompt_text, model_instance=None):
    """生成文本的函数"""
    if model_instance is None:
        model_instance = model
    
    try:
        response = model_instance.generate_content(
            prompt_text,
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        return f"生成内容时发生错误：{e}"

# 示例用法
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🤖 Gemini API 文本生成示例")
    print("="*50)
    
    # 示例1：基础文本生成
    prompt1 = "请写一个关于人工智能未来发展的简短段落。"
    print(f"\n📝 提示：{prompt1}")
    print(f"🔮 回答：{generate_text(prompt1)}")
    
    # 示例2：代码生成
    prompt2 = "用Python写一个计算斐波那契数列的函数。"
    print(f"\n📝 提示：{prompt2}")
    print(f"🔮 回答：{generate_text(prompt2)}")
    
    # 示例3：创意写作
    prompt3 = "写一首关于科技与自然和谐共存的现代诗。"
    print(f"\n📝 提示：{prompt3}")
    print(f"🔮 回答：{generate_text(prompt3)}")
    
    print("\n" + "="*50)
    print("✅ 示例运行完成！")
    print("="*50)
