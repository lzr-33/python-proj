import numpy as np
from PIL import Image, ImageDraw
import os
import urllib.request
from io import BytesIO

def create_test_image():
    """创建一个彩色的测试图像"""
    # 创建一个400x300的白色背景图像
    img = Image.new('RGB', (400, 300), color='white')
    draw = ImageDraw.Draw(img)
    
    # 绘制一些彩色图形来测试亮度效果
    # 红色正方形（较暗）
    draw.rectangle([50, 50, 150, 150], fill='red')
    # 绿色圆形（中等亮度）  
    draw.ellipse([180, 50, 280, 150], fill='green')
    # 蓝色矩形（较暗）
    draw.rectangle([50, 180, 350, 220], fill='blue')
    # 黄色区域（较亮）
    draw.rectangle([50, 240, 350, 280], fill='yellow')
    # 白色文字区域（最亮）
    draw.rectangle([300, 50, 380, 130], fill='white')
    # 灰色区域（中等暗度）
    draw.rectangle([320, 180, 380, 240], fill='gray')
    
    # 添加一些文字说明
    try:
        # 尝试使用默认字体写文字
        draw.text((60, 65), "Red", fill='white')
        draw.text((195, 65), "Green", fill='black') 
        draw.text((60, 195), "Blue", fill='white')
        draw.text((60, 250), "Yellow", fill='black')
    except:
        pass  # 如果字体不可用就跳过
    
    return img

def download_sample_image():
    """尝试从网络下载示例图像（使用urllib，无需requests库）"""
    # 使用urllib下载示例图像
    sample_urls = [
        "https://picsum.photos/400/300",  # Lorem Picsum随机图片
    ]
    
    for i, url in enumerate(sample_urls):
        try:
            print(f"尝试从 {url} 下载示例图像 ({i+1}/{len(sample_urls)})...")
            
            # 设置超时和请求头
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            # 下载图像
            with urllib.request.urlopen(req, timeout=10) as response:
                data = response.read()
                
            # 打开图像
            img = Image.open(BytesIO(data)).convert("RGB")
            print("✓ 成功下载示例图像！")
            return img
            
        except Exception as e:
            print(f"× 从 {url} 下载失败: {str(e)}")
            continue
    
    print("所有下载尝试都失败了，将使用内置测试图像")
    return None

def extract_luminance(image, method="weighted"):
    """
    从图像中抽取亮度图
    :param image: PIL Image对象
    :param method: 亮度计算方法，"weighted"（加权平均，默认）或 "average"（简单平均）
    :return: 亮度图（PIL Image对象）
    """
    # 确保图像是RGB模式
    if image.mode != 'RGB':
        image = image.convert("RGB")
    
    rgb_array = np.array(image)
    
    # 分离R、G、B通道
    r = rgb_array[:, :, 0]
    g = rgb_array[:, :, 1] 
    b = rgb_array[:, :, 2]
    
    # 计算亮度图
    if method == "weighted":
        # 加权平均：符合人眼感知的亮度公式（BT.601标准）
        luminance = 0.299 * r + 0.587 * g + 0.114 * b
    elif method == "average":
        # 简单平均：三通道直接平均
        luminance = (r + g + b) / 3
    else:
        raise ValueError("method must be 'weighted' or 'average'")
    
    # 亮度值取整并确保在[0,255]范围内，转为uint8类型
    luminance = np.clip(luminance, 0, 255).astype(np.uint8)
    # 转为PIL灰度图（单通道）
    luminance_img = Image.fromarray(luminance, mode="L")
    
    return luminance_img

def main():
    print("=== PNG亮度图抽取工具 (无额外依赖版) ===")
    print("正在检查环境和准备图像...")
    
    # 检查必要库
    try:
        import PIL
        import numpy as np
        print("✓ 必要库检查通过 (PIL, numpy)")
    except ImportError as e:
        print("× 缺少必要的库!")
        print("请安装: pip install pillow numpy")
        return
    
    image_path = "example.png"
    original_img = None
    
    # 方法1：检查是否已有本地图像
    if os.path.exists(image_path):
        try:
            original_img = Image.open(image_path)
            print(f"✓ 找到本地图像: {image_path}")
        except Exception as e:
            print(f"× 本地图像损坏: {e}")
            original_img = None
    
    # 方法2：如果没有本地图像，尝试下载
    if original_img is None:
        print("\n尝试下载网络示例图像...")
        downloaded_img = download_sample_image()
        if downloaded_img is not None:
            original_img = downloaded_img
            try:
                original_img.save(image_path)
                print(f"✓ 下载的示例图像已保存为: {image_path}")
            except Exception as e:
                print(f"× 保存下载的图像失败: {e}")
                # 继续使用内存中的图像，不保存到文件
    
    # 方法3：如果下载失败，创建测试图像
    if original_img is None:
        print("\n创建内置测试图像...")
        original_img = create_test_image()
        try:
            original_img.save(image_path)
            print(f"✓ 测试图像已创建并保存为: {image_path}")
        except Exception as e:
            print(f"× 保存测试图像失败: {e}")
            print("将继续使用内存中的测试图像")
    
    print(f"\n图像信息: 尺寸={original_img.size}, 模式={original_img.mode}")
    
    # 抽取两种亮度图
    print("\n正在计算亮度图...")
    try:
        print("1. 计算加权平均亮度图...")
        weighted_lum = extract_luminance(original_img, method="weighted")
        
        print("2. 计算简单平均亮度图...")  
        average_lum = extract_luminance(original_img, method="average")
        
        print("✓ 亮度图计算完成")
    except Exception as e:
        print(f"× 计算亮度图时出错: {e}")
        return
    
    # 显示图像信息
    print(f"\n结果图像信息:")
    print(f"- 原图: {original_img.size}, {original_img.mode}")
    print(f"- 加权平均亮度图: {weighted_lum.size}, {weighted_lum.mode}")  
    print(f"- 简单平均亮度图: {average_lum.size}, {average_lum.mode}")
    
    # 保存结果
    output_files = []
    
    try:
        # 保存加权平均亮度图
        weighted_file = "luminance_weighted.png"
        weighted_lum.save(weighted_file)
        output_files.append(weighted_file)
        print(f"✓ 已保存: {weighted_file}")
    except Exception as e:
        print(f"× 保存加权平均亮度图失败: {e}")
    
    try:
        # 保存简单平均亮度图
        average_file = "luminance_average.png" 
        average_lum.save(average_file)
        output_files.append(average_file)
        print(f"✓ 已保存: {average_file}")
    except Exception as e:
        print(f"× 保存简单平均亮度图失败: {e}")
    
    # 创建对比图
    try:
        print("正在创建对比图...")
        width, height = original_img.size
        comparison_img = Image.new('RGB', (width * 3, height))
        
        # 将原图和亮度图粘贴到对比图上
        comparison_img.paste(original_img, (0, 0))
        
        # 将灰度图转换为RGB以便拼接
        weighted_rgb = Image.merge('RGB', [weighted_lum, weighted_lum, weighted_lum])
        average_rgb = Image.merge('RGB', [average_lum, average_lum, average_lum])
        
        comparison_img.paste(weighted_rgb, (width, 0))
        comparison_img.paste(average_rgb, (width * 2, 0))
        
        comparison_file = "comparison_result.png"
        comparison_img.save(comparison_file)
        output_files.append(comparison_file)
        print(f"✓ 已保存: {comparison_file}")
    except Exception as e:
        print(f"× 创建对比图时出错: {e}")
    
    # 尝试显示图像
    print("\n尝试显示图像...")
    display_success = False
    try:
        original_img.show(title="1. 原始彩色图像")
        print("✓ 已显示原始图像")
        display_success = True
        
        weighted_lum.show(title="2. 加权平均亮度图")
        print("✓ 已显示加权平均亮度图")
        
        average_lum.show(title="3. 简单平均亮度图") 
        print("✓ 已显示简单平均亮度图")
        
        if any("comparison_result.png" in f for f in output_files):
            Image.open("comparison_result.png").show(title="4. 对比图")
            print("✓ 已显示对比图")
            
    except Exception as e:
        print(f"× 自动显示图像失败: {e}")
        print("请手动打开生成的PNG文件查看结果")
    
    print(f"\n🎉 程序执行完成！")
    if output_files:
        print("生成的文件:")
        for file in output_files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"  - {file} ({size} bytes)")
            else:
                print(f"  - {file} (保存失败)")
    
    print(f"\n📁 当前工作目录: {os.getcwd()}")
    print("\n💡 提示:")
    print("- 所有生成的文件都在上面的目录中")
    print("- 如果看不到图像，请检查系统的图片查看器")
    print("- 要使用自己的图像，请将PNG文件重命名为 'example.png' 放在此目录")

if __name__ == "__main__":
    main()