#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单图片提示词生成器
专注于使用 Gemini 生成高质量的图片提示词
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

class SimpleImagePromptGenerator:
    def __init__(self):
        """初始化提示词生成器"""
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ 请设置 GOOGLE_API_KEY 环境变量")
        
        genai.configure(api_key=self.api_key)
        
        # 从 .env 文件读取模型配置
        model_name = os.getenv("DEFAULT_MODEL", "gemini-1.5-flash")
        self.model = genai.GenerativeModel(model_name)
    
    def generate_prompt(self, description: str, style: str = "photorealistic") -> str:
        """生成图片提示词"""
        prompt_template = f"""
        请根据以下描述生成一个专业的AI图片生成提示词（英文）：
        
        描述：{description}
        风格：{style}
        
        要求：
        1. 使用专业的艺术和摄影术语
        2. 包含详细的视觉描述
        3. 添加质量修饰词
        4. 确保提示词适合 AI 图片生成
        5. 直接输出英文提示词，不要解释
        
        格式：主要内容, 详细描述, 艺术风格, 质量词汇, 技术参数
        """
        
        try:
            response = self.model.generate_content(prompt_template)
            return response.text.strip()
        except Exception as e:
            return f"Error generating prompt: {e}"
    
    def create_variations(self, base_prompt: str, count: int = 3) -> list:
        """创建提示词变体"""
        variations = []
        for i in range(count):
            variation_prompt = f"""
            基于以下提示词创建一个变体版本：
            
            原始提示词：{base_prompt}
            
            变体要求：
            - 保持核心内容不变
            - 调整艺术风格或视角
            - 添加不同的细节描述
            - 直接输出英文提示词
            
            变体 {i+1}：
            """
            
            try:
                response = self.model.generate_content(variation_prompt)
                variations.append(response.text.strip())
            except Exception as e:
                variations.append(f"Error creating variation {i+1}: {e}")
        
        return variations
    
    def save_prompts(self, prompts: dict, filename: str = None):
        """保存提示词到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_prompts_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("AI 图片生成提示词\n")
            f.write("="*50 + "\n")
            f.write(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for key, value in prompts.items():
                f.write(f"{key}：\n{value}\n\n")
        
        print(f"💾 提示词已保存到：{filename}")

def main():
    """主程序"""
    print("🎨 Gemini AI 图片提示词生成器")
    print("="*50)
    print("💡 帮助您生成专业的 AI 图片生成提示词")
    print("="*50)
    
    try:
        generator = SimpleImagePromptGenerator()
        
        while True:
            print("\n🎯 请选择功能：")
            print("1. 📝 生成图片提示词")
            print("2. 🔄 创建提示词变体")
            print("3. 💡 获取提示词建议")
            print("4. 📋 常用风格参考")
            print("0. 🚪 退出")
            
            choice = input("\n请输入选项 (0-4): ").strip()
            
            if choice == "0":
                print("👋 再见！")
                break
                
            elif choice == "1":
                print("\n📝 生成图片提示词")
                description = input("请详细描述您想要的图片：")
                if not description.strip():
                    print("❌ 请输入有效的描述")
                    continue
                
                print("\n🎨 选择风格：")
                print("1. photorealistic (照片现实)")
                print("2. digital art (数字艺术)")
                print("3. oil painting (油画)")
                print("4. anime style (动漫风格)")
                print("5. concept art (概念艺术)")
                print("6. watercolor (水彩)")
                print("7. 自定义")
                
                style_choice = input("请选择风格 (1-7): ").strip()
                style_map = {
                    "1": "photorealistic",
                    "2": "digital art",
                    "3": "oil painting",
                    "4": "anime style",
                    "5": "concept art",
                    "6": "watercolor"
                }
                
                if style_choice in style_map:
                    style = style_map[style_choice]
                elif style_choice == "7":
                    style = input("请输入自定义风格：")
                else:
                    style = "photorealistic"
                
                print(f"🔄 正在生成提示词... (风格: {style})")
                prompt = generator.generate_prompt(description, style)
                
                print(f"\n✨ 生成的提示词：")
                print("-" * 50)
                print(prompt)
                print("-" * 50)
                
                # 询问是否保存
                save = input("\n💾 是否保存提示词？(y/N): ").lower().strip()
                if save == 'y':
                    prompts_data = {
                        "原始描述": description,
                        "选择风格": style,
                        "生成提示词": prompt
                    }
                    generator.save_prompts(prompts_data)
                
            elif choice == "2":
                print("\n🔄 创建提示词变体")
                base_prompt = input("请输入基础提示词：")
                if not base_prompt.strip():
                    print("❌ 请输入有效的提示词")
                    continue
                
                count = input("生成变体数量 (默认3个): ")
                try:
                    count = int(count) if count else 3
                    count = min(max(count, 1), 5)  # 限制在1-5之间
                except ValueError:
                    count = 3
                
                print(f"🔄 正在生成 {count} 个变体...")
                variations = generator.create_variations(base_prompt, count)
                
                print(f"\n✨ 生成的变体：")
                print("=" * 50)
                for i, variation in enumerate(variations, 1):
                    print(f"\n变体 {i}：")
                    print("-" * 30)
                    print(variation)
                print("=" * 50)
                
                # 询问是否保存
                save = input("\n💾 是否保存所有变体？(y/N): ").lower().strip()
                if save == 'y':
                    prompts_data = {"基础提示词": base_prompt}
                    for i, variation in enumerate(variations, 1):
                        prompts_data[f"变体 {i}"] = variation
                    generator.save_prompts(prompts_data)
                
            elif choice == "3":
                print("\n💡 提示词建议")
                print("🎯 优质提示词的要素：")
                print("   • 主体描述：具体说明要画什么")
                print("   • 细节描述：服装、表情、姿态等")
                print("   • 环境设定：背景、场景、氛围")
                print("   • 艺术风格：写实、卡通、油画等")
                print("   • 质量词汇：high quality, detailed, masterpiece")
                print("   • 技术参数：8k, HDR, professional lighting")
                
                print("\n🚫 负面提示词常用：")
                print("   • low quality, blurry, distorted")
                print("   • bad anatomy, deformed, ugly")
                print("   • watermark, signature, text")
                
                print("\n📝 示例结构：")
                print('   "主体, 细节描述, 环境, 风格, 质量词"')
                print('   例：beautiful woman, long hair, sunset beach,')
                print('       photorealistic, high quality, 8k resolution')
                
            elif choice == "4":
                print("\n📋 常用风格参考")
                print("🖼️  艺术风格：")
                print("   • 现实主义：photorealistic, hyperrealistic, lifelike")
                print("   • 数字艺术：digital art, CGI, 3D render")
                print("   • 传统绘画：oil painting, watercolor, acrylic painting")
                print("   • 插画风格：illustration, cartoon, comic book style")
                print("   • 动漫风格：anime, manga, studio ghibli style")
                
                print("\n📷 摄影风格：")
                print("   • 人像摄影：portrait photography, headshot")
                print("   • 风景摄影：landscape photography, nature")
                print("   • 街头摄影：street photography, urban")
                print("   • 时尚摄影：fashion photography, editorial")
                
                print("\n🎨 特殊效果：")
                print("   • 光线效果：dramatic lighting, golden hour, neon lights")
                print("   • 色彩风格：monochrome, vibrant colors, pastel colors")
                print("   • 视角效果：close-up, wide angle, bird's eye view")
                
            else:
                print("❌ 无效选项，请重新选择")
                
    except Exception as e:
        print(f"❌ 程序初始化失败：{e}")
        print("请确保已设置 GOOGLE_API_KEY 环境变量")

if __name__ == "__main__":
    main()
