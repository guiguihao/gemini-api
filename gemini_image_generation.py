#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini API 图片生成功能
结合 Gemini 的文本生成能力和第三方图片生成API
"""

import google.generativeai as genai
import os
import requests
import json
import base64
from datetime import datetime
from typing import Optional, Dict, Any
import time

# 加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class GeminiImageGenerator:
    def __init__(self, api_key: str = None):
        """初始化图片生成器"""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 GOOGLE_API_KEY 环境变量")
        
        genai.configure(api_key=self.api_key)
        
        # 从 .env 文件读取模型配置
        model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(model_name)
        
        # 支持的图片生成服务
        self.supported_services = {
            "huggingface": "Hugging Face Inference API",
            "stability": "Stability AI API", 
            "replicate": "Replicate API",
            "local": "本地 Stable Diffusion"
        }
    
    def generate_image_prompt(self, description: str, style: str = "现实主义", 
                            quality: str = "高质量", language: str = "英文") -> str:
        """使用 Gemini 生成优化的图片提示词"""
        prompt = f"""
        请根据以下描述生成一个详细的图片生成提示词：
        
        描述：{description}
        风格：{style}
        质量要求：{quality}
        输出语言：{language}
        
        请生成一个适合AI图片生成的详细提示词，包含：
        1. 主要内容描述
        2. 艺术风格
        3. 光线和色彩
        4. 质量修饰词
        5. 技术参数建议
        
        请直接输出提示词，不要包含解释文字。
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"❌ 提示词生成失败：{e}"
    
    def enhance_prompt(self, basic_prompt: str) -> str:
        """增强提示词"""
        enhance_prompt = f"""
        请优化以下图片生成提示词，使其更专业、更详细：
        
        原始提示词：{basic_prompt}
        
        请添加：
        - 专业的艺术术语
        - 详细的视觉描述
        - 质量和风格修饰词
        - 适当的技术参数
        
        输出优化后的英文提示词：
        """
        
        try:
            response = self.model.generate_content(enhance_prompt)
            return response.text.strip()
        except Exception as e:
            return basic_prompt
    
    def generate_negative_prompt(self, positive_prompt: str) -> str:
        """生成负面提示词"""
        negative_prompt = f"""
        基于以下正面提示词，生成相应的负面提示词（negative prompt）：
        
        正面提示词：{positive_prompt}
        
        请生成英文负面提示词，用于排除不需要的元素，如：
        - 低质量、模糊、扭曲
        - 不合适的内容
        - 技术缺陷
        - 不协调的元素
        
        请直接输出负面提示词：
        """
        
        try:
            response = self.model.generate_content(negative_prompt)
            return response.text.strip()
        except Exception as e:
            return "low quality, blurry, distorted, ugly, bad anatomy"
    
    def generate_with_huggingface(self, prompt: str, model_id: str = "runwayml/stable-diffusion-v1-5") -> Dict[str, Any]:
        """使用 Hugging Face API 生成图片"""
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if not hf_token:
            return {"error": "请设置 HUGGINGFACE_TOKEN 环境变量"}
        
        api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        headers = {"Authorization": f"Bearer {hf_token}"}
        
        data = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 30,
                "guidance_scale": 7.5,
                "width": 512,
                "height": 512
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                # 保存图片
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}.png"
                
                with open(filename, "wb") as f:
                    f.write(response.content)
                
                return {
                    "success": True,
                    "filename": filename,
                    "prompt": prompt,
                    "model": model_id
                }
            else:
                return {"error": f"API 请求失败：{response.status_code} - {response.text}"}
                
        except Exception as e:
            return {"error": f"生成失败：{e}"}
    
    def create_image_story(self, theme: str, num_images: int = 4) -> Dict[str, Any]:
        """创建图片故事（生成多个相关图片的提示词）"""
        story_prompt = f"""
        请基于主题 "{theme}" 创建一个由 {num_images} 张图片组成的视觉故事。
        
        为每张图片生成：
        1. 场景描述
        2. 详细的英文提示词
        3. 在故事中的作用
        
        请用 JSON 格式输出，结构如下：
        {{
            "story_title": "故事标题",
            "story_description": "整体故事描述",
            "images": [
                {{
                    "sequence": 1,
                    "scene_description": "场景描述",
                    "prompt": "英文提示词",
                    "role": "在故事中的作用"
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(story_prompt)
            return {"success": True, "story": response.text}
        except Exception as e:
            return {"error": f"故事生成失败：{e}"}
    
    def analyze_generated_image(self, image_path: str) -> str:
        """分析生成的图片"""
        try:
            from PIL import Image
            
            img = Image.open(image_path)
            analysis_prompt = """
            请详细分析这张图片，包括：
            1. 主要内容和构图
            2. 艺术风格和技法
            3. 色彩和光线
            4. 整体质量评价
            5. 可能的改进建议
            """
            
            vision_model = genai.GenerativeModel('gemini-1.5-flash')
            response = vision_model.generate_content([analysis_prompt, img])
            
            return response.text
        except ImportError:
            return "❌ 请安装 Pillow 库：pip install Pillow"
        except Exception as e:
            return f"❌ 图片分析失败：{e}"
    
    def get_style_suggestions(self, content_type: str) -> str:
        """获取风格建议"""
        style_prompt = f"""
        请为 "{content_type}" 类型的图片生成推荐的艺术风格列表。
        
        包括：
        1. 传统艺术风格（如油画、水彩等）
        2. 现代艺术风格（如抽象、极简等）
        3. 数字艺术风格（如赛博朋克、蒸汽波等）
        4. 摄影风格（如纪实、肖像等）
        5. 动画风格（如动漫、迪士尼等）
        
        为每种风格提供简短描述和适用场景。
        """
        
        try:
            response = self.model.generate_content(style_prompt)
            return response.text
        except Exception as e:
            return f"❌ 风格建议生成失败：{e}"

def interactive_image_generator():
    """交互式图片生成器"""
    print("🎨 Gemini AI 图片生成助手")
    print("="*50)
    print("💡 功能说明：")
    print("   • 使用 Gemini 生成和优化图片提示词")
    print("   • 支持多种图片生成服务")
    print("   • 提供创意建议和分析功能")
    print("="*50)
    
    try:
        generator = GeminiImageGenerator()
        
        while True:
            print("\n🎯 请选择功能：")
            print("1. 🎨 生成图片提示词")
            print("2. ✨ 优化现有提示词")
            print("3. 🚫 生成负面提示词")
            print("4. 🖼️  生成图片 (Hugging Face)")
            print("5. 📚 创建图片故事")
            print("6. 🔍 分析生成的图片")
            print("7. 🎭 获取风格建议")
            print("8. 💡 使用技巧")
            print("0. 🚪 退出")
            
            choice = input("\n请输入选项 (0-8): ").strip()
            
            if choice == "0":
                print("👋 感谢使用 Gemini AI 图片生成助手！")
                break
                
            elif choice == "1":
                print("\n🎨 生成图片提示词")
                description = input("请描述您想要的图片：")
                style = input("艺术风格 (默认：现实主义)：") or "现实主义"
                quality = input("质量要求 (默认：高质量)：") or "高质量"
                language = input("提示词语言 (默认：英文)：") or "英文"
                
                print("🔄 正在生成提示词...")
                prompt = generator.generate_image_prompt(description, style, quality, language)
                print(f"\n✨ 生成的提示词：\n{prompt}")
                
            elif choice == "2":
                print("\n✨ 优化现有提示词")
                basic_prompt = input("请输入要优化的提示词：")
                
                print("🔄 正在优化提示词...")
                enhanced = generator.enhance_prompt(basic_prompt)
                print(f"\n🚀 优化后的提示词：\n{enhanced}")
                
            elif choice == "3":
                print("\n🚫 生成负面提示词")
                positive_prompt = input("请输入正面提示词：")
                
                print("🔄 正在生成负面提示词...")
                negative = generator.generate_negative_prompt(positive_prompt)
                print(f"\n⛔ 负面提示词：\n{negative}")
                
            elif choice == "4":
                print("\n🖼️ 生成图片 (需要 Hugging Face Token)")
                hf_token = os.getenv("HUGGINGFACE_TOKEN")
                if not hf_token:
                    print("❌ 请先设置 HUGGINGFACE_TOKEN 环境变量")
                    print("   1. 访问 https://huggingface.co/settings/tokens")
                    print("   2. 创建新的 token")
                    print("   3. 设置环境变量：export HUGGINGFACE_TOKEN='your_token'")
                    continue
                
                prompt = input("请输入图片提示词：")
                model = input("模型 (默认：runwayml/stable-diffusion-v1-5)：") or "runwayml/stable-diffusion-v1-5"
                
                print("🎨 正在生成图片，请稍候...")
                result = generator.generate_with_huggingface(prompt, model)
                
                if result.get("success"):
                    print(f"✅ 图片生成成功！")
                    print(f"📁 文件：{result['filename']}")
                    print(f"🎯 提示词：{result['prompt']}")
                else:
                    print(f"❌ 生成失败：{result.get('error')}")
                    
            elif choice == "5":
                print("\n📚 创建图片故事")
                theme = input("请输入故事主题：")
                num_images = input("图片数量 (默认：4)：")
                try:
                    num_images = int(num_images) if num_images else 4
                except ValueError:
                    num_images = 4
                
                print("📝 正在创建图片故事...")
                story = generator.create_image_story(theme, num_images)
                
                if story.get("success"):
                    print(f"\n📖 故事创建成功：\n{story['story']}")
                else:
                    print(f"❌ 故事创建失败：{story.get('error')}")
                    
            elif choice == "6":
                print("\n🔍 分析生成的图片")
                image_path = input("请输入图片路径：")
                
                if not os.path.exists(image_path):
                    print(f"❌ 文件不存在：{image_path}")
                    continue
                
                print("🔍 正在分析图片...")
                analysis = generator.analyze_generated_image(image_path)
                print(f"\n📊 分析结果：\n{analysis}")
                
            elif choice == "7":
                print("\n🎭 获取风格建议")
                content_type = input("请输入内容类型（如：人物肖像、风景、建筑等）：")
                
                print("💡 正在生成风格建议...")
                suggestions = generator.get_style_suggestions(content_type)
                print(f"\n🎨 风格建议：\n{suggestions}")
                
            elif choice == "8":
                print("\n💡 使用技巧")
                print("🎯 提示词技巧：")
                print("   • 使用具体的描述词而非抽象概念")
                print("   • 添加艺术家名字或艺术风格")
                print("   • 包含质量修饰词（如 'highly detailed', 'masterpiece'）")
                print("   • 指定分辨率和纵横比")
                print("   • 使用负面提示词排除不需要的元素")
                print("\n🔧 技术参数：")
                print("   • steps: 20-50 (质量与速度平衡)")
                print("   • guidance_scale: 7-15 (提示词遵循程度)")
                print("   • 分辨率: 512x512, 768x768, 1024x1024")
                print("\n🎨 常用风格：")
                print("   • 现实主义: photorealistic, hyperrealistic")
                print("   • 艺术风格: oil painting, watercolor, digital art")
                print("   • 动漫风格: anime, manga, studio ghibli style")
                print("   • 概念艺术: concept art, matte painting")
                
            else:
                print("❌ 无效选项，请重新选择")
                
    except Exception as e:
        print(f"❌ 初始化失败：{e}")
        print("请确保已设置 GOOGLE_API_KEY 环境变量")

# 辅助函数
def setup_environment():
    """环境设置指南"""
    print("🔧 环境设置指南")
    print("="*40)
    print("1. Gemini API:")
    print("   export GOOGLE_API_KEY='your_gemini_key'")
    print("\n2. Hugging Face (可选):")
    print("   export HUGGINGFACE_TOKEN='your_hf_token'")
    print("\n3. 安装依赖:")
    print("   pip install requests pillow")
    print("\n4. 获取 API 密钥:")
    print("   • Gemini: https://makersuite.google.com/app/apikey")
    print("   • Hugging Face: https://huggingface.co/settings/tokens")

if __name__ == "__main__":
    # 检查环境
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ 请先设置 GOOGLE_API_KEY 环境变量")
        setup_environment()
    else:
        interactive_image_generator()
