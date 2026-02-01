from PIL import Image

def resize_pil(input_path, output_path, size=None, scale_factor=None, method=Image.Resampling.LANCZOS):
    """
    使用 Pillow 缩放 PNG 图像
    
    :param input_path: 输入文件路径
    :param output_path: 输出文件路径
    :param size: 目标尺寸 (width, height)，例如 (800, 600)
    :param scale_factor: 缩放比例 (0.5 表示缩小一半, 2.0 表示放大一倍)
    :param method: 重采样方法，控制缩放质量
    """
    try:
        with Image.open(input_path) as img:
            # 确保图像是 RGBA 模式以保留透明度
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            original_width, original_height = img.size
            
            # 计算新的尺寸
            if size:
                new_size = size
            elif scale_factor:
                new_size = (int(original_width * scale_factor), int(original_height * scale_factor))
            else:
                raise ValueError("必须提供 size 或 scale_factor")
            
            print(f"原始尺寸: {original_width}x{original_height}")
            print(f"目标尺寸: {new_size[0]}x{new_size[1]}")
            
            # 执行缩放
            # Image.Resampling.LANCZOS: 高质量缩小
            # Image.Resampling.BICUBIC: 平衡质量和速度
            # Image.Resampling.BILINEAR: 快速，质量较低
            resized_img = img.resize(new_size, resample=method)
            
            # 保存图像，优化PNG压缩
            resized_img.save(output_path, 'PNG', optimize=True)
            print(f"图像已成功保存至: {output_path}")
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 {input_path}")
    except Exception as e:
        print(f"发生错误: {e}")

# --- 使用示例 ---
if __name__ == "__main__":
    input_file = "input.png"
    output_file_resize = "output_resize.png"
    output_file_scale = "output_scale.png"

    # 示例 1: 缩放到指定尺寸 (保持宽高比需自行计算或使用 thumbnail)
    # 注意：直接resize不会保持宽高比，可能导致拉伸
    resize_pil(input_file, output_file_resize, size=(400, 300), method=Image.Resampling.LANCZOS)
    
    # 示例 2: 按比例缩放 (推荐此方法以避免变形)
    resize_pil(input_file, output_file_scale, scale_factor=0.5, method=Image.Resampling.LANCZOS)
    
    # 示例 3: 保持宽高比缩放 (使用 thumbnail 方法)
    def resize_keep_aspect_ratio(input_path, output_path, base_width):
        with Image.open(input_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                
            w_percent = (base_width / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img.thumbnail((base_width, h_size), Image.Resampling.LANCZOS)
            img.save(output_path, 'PNG', optimize=True)
            print(f"保持宽高比缩放完成，新尺寸: {img.size}")

    resize_keep_aspect_ratio(input_file, "output_thumbnail.png", 400)