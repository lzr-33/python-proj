from PIL import Image, ImageDraw
import os
import sys

def get_script_dir():
    """获取脚本所在目录的绝对路径"""
    return os.path.dirname(os.path.abspath(sys.argv[0]))

def create_test_image(output_name="test.png", width=640, height=480):
    """
    创建测试PNG图片
    
    参数:
        output_name: 输出文件名
        width: 图片宽度(像素)
        height: 图片高度(像素)
    """
    try:
        script_dir = get_script_dir()
        output_path = os.path.join(script_dir, output_name)
        
        # 创建新图像
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # 绘制测试图形
        draw.rectangle([50, 50, width-50, height-50], outline='red', width=5)
        draw.line([0, 0, width, height], fill='blue', width=3)
        draw.line([0, height, width, 0], fill='blue', width=3)
        draw.ellipse([width//4, height//4, 3*width//4, 3*height//4], 
                    outline='green', width=4)
        draw.text((width//2-100, height//2-20), "TEST IMAGE", fill='black')
        
        # 保存图片
        img.save(output_path, 'PNG')
        print(f"测试图片已创建: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"创建图片时出错: {e}")
        return None

def resize_image(input_path, output_path=None, width=None, height=None, 
                scale=None, keep_aspect=True, method=Image.Resampling.LANCZOS):
    """
    PNG图片缩放工具
    
    参数:
        input_path: 输入图片路径
        output_path: 输出图片路径(可选)
        width: 目标宽度(像素)
        height: 目标高度(像素)
        scale: 缩放比例
        keep_aspect: 是否保持宽高比
        method: 重采样方法
    """
    try:
        # 处理输入路径
        if not os.path.isabs(input_path):
            input_path = os.path.join(get_script_dir(), input_path)
            
        with Image.open(input_path) as img:
            # 确保处理RGBA模式以保留透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            original_width, original_height = img.size
            
            # 处理输出路径
            if output_path is None:
                output_path = os.path.join(
                    get_script_dir(), 
                    f"resized_{os.path.basename(input_path)}"
                )
            elif not os.path.isabs(output_path):
                output_path = os.path.join(get_script_dir(), output_path)
            
            # 计算目标尺寸
            if scale is not None:
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
            elif width is not None and height is not None:
                new_width = width
                new_height = height
            elif width is not None:
                if keep_aspect:
                    ratio = width / original_width
                    new_width = width
                    new_height = int(original_height * ratio)
                else:
                    new_width = width
                    new_height = original_height
            elif height is not None:
                if keep_aspect:
                    ratio = height / original_height
                    new_height = height
                    new_width = int(original_width * ratio)
                else:
                    new_height = height
                    new_width = original_width
            else:
                raise ValueError("必须提供width/height或scale参数")
            
            print(f"原始尺寸: {original_width}x{original_height}")
            print(f"新尺寸: {new_width}x{new_height}")
            
            # 执行缩放
            resized_img = img.resize((new_width, new_height), resample=method)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存图片
            resized_img.save(output_path, 'PNG', optimize=True)
            print(f"图片已保存至: {output_path}")
            return output_path
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_path}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None

if __name__ == "__main__":
    # 1. 首先创建测试图片
    test_image_path = create_test_image()
    
    if test_image_path:
        # 2. 测试各种缩放方式
        print("\n=== 测试1: 按比例缩放 ===")
        resize_image(test_image_path, scale=0.5)
        
        print("\n=== 测试2: 指定宽度并保持比例 ===")
        resize_image(test_image_path, width=300)
        
        print("\n=== 测试3: 指定高度并保持比例 ===")
        resize_image(test_image_path, height=200)
        
        print("\n=== 测试4: 指定宽高(可能变形) ===")
        resize_image(test_image_path, width=400, height=300, keep_aspect=False)
