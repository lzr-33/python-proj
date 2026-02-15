import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime

class BrightnessAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("PNG图片亮度像素分析器")
        self.root.geometry("800x600")
        
        self.image_path = None
        self.image_data = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = tk.Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文件选择区域
        file_frame = tk.LabelFrame(main_frame, text="文件选择", padx=5, pady=5)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Button(file_frame, text="选择PNG图片", command=self.select_image, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        
        self.file_label = tk.Label(file_frame, text="未选择文件", fg="gray")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # 参数设置区域
        param_frame = tk.LabelFrame(main_frame, text="参数设置", padx=5, pady=5)
        param_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(param_frame, text="亮度阈值:").pack(side=tk.LEFT)
        self.threshold_var = tk.StringVar(value="200")
        threshold_entry = tk.Entry(param_frame, textvariable=self.threshold_var, width=10)
        threshold_entry.pack(side=tk.LEFT, padx=(5, 20))
        
        tk.Button(param_frame, text="开始分析", command=self.analyze_brightness,
                 bg="#2196F3", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        
        # 结果显示区域
        result_frame = tk.LabelFrame(main_frame, text="分析结果", padx=5, pady=5)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建文本框显示结果
        self.result_text = tk.Text(result_frame, height=8, font=("Consolas", 10))
        scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 图表区域
        chart_frame = tk.LabelFrame(main_frame, text="亮度分布图表", padx=5, pady=5)
        chart_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # 保存数据按钮
        save_frame = tk.Frame(main_frame)
        save_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(save_frame, text="保存数据到CSV", command=self.save_to_csv,
                 bg="#FF9800", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
        
        tk.Button(save_frame, text="导出分析报告", command=self.export_report,
                 bg="#9C27B0", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=(10, 0))
    
    def select_image(self):
        """选择PNG图片文件"""
        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg;*.jpeg"),
            ("All image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff"),
            ("All files", "*.*")
        ]
        
        file_path = filedialog.askopenfilename(
            title="选择图片文件",
            filetypes=file_types
        )
        
        if file_path:
            self.image_path = file_path
            filename = file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1]
            self.file_label.config(text=f"已选择: {filename}", fg="green")
            self.load_image()
    
    def load_image(self):
        """加载图片"""
        try:
            self.image_data = Image.open(self.image_path).convert('L')  # 转换为灰度图
            self.result_text.insert(tk.END, f"✓ 成功加载图片: {self.image_path}\n")
            self.result_text.insert(tk.END, f"✓ 图片尺寸: {self.image_data.size}\n")
            self.result_text.insert(tk.END, "-" * 50 + "\n")
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")
    
    def analyze_brightness(self):
        """分析图片亮度"""
        if not self.image_path or not self.image_data:
            messagebox.showwarning("警告", "请先选择图片文件！")
            return
        
        try:
            # 获取阈值
            threshold = int(self.threshold_var.get())
            if not (0 <= threshold <= 255):
                raise ValueError("阈值必须在0-255之间")
            
            # 转换为numpy数组
            img_array = np.array(self.image_data)
            
            # 计算各种亮度统计
            total_pixels = img_array.size
            bright_pixels = np.sum(img_array > threshold)
            dark_pixels = np.sum(img_array <= threshold)
            bright_percentage = (bright_pixels / total_pixels) * 100
            
            # 更详细的亮度分级
            very_bright = np.sum(img_array > 220)
            bright = np.sum((img_array > threshold) & (img_array <= 220))
            medium = np.sum((img_array > 128) & (img_array <= threshold))
            dim = np.sum((img_array > 64) & (img_array <= 128))
            very_dark = np.sum(img_array <= 64)
            
            # 亮度统计
            mean_brightness = np.mean(img_array)
            max_brightness = np.max(img_array)
            min_brightness = np.min(img_array)
            std_brightness = np.std(img_array)
            
            # 清空之前的结果
            self.result_text.delete(1.0, tk.END)
            
            # 显示结果
            result_str = f"""
🎯 PNG图片亮度像素分析报告
{'='*60}
📁 文件路径: {self.image_path}
🖼️  图片尺寸: {self.image_data.size[0]} × {self.image_data.size[1]}
⚙️  分析阈值: > {threshold} (定义为亮像素)

📊 基本统计:
• 总像素数量: {total_pixels:,}
• 平均亮度: {mean_brightness:.2f}/255
• 最大亮度: {max_brightness}/255
• 最小亮度: {min_brightness}/255
• 亮度标准差: {std_brightness:.2f}

💡 亮度分类统计:
• 很亮像素 (>220): {very_bright:,} ({very_bright/total_pixels*100:.2f}%)
• 较亮像素 ({threshold}-220): {bright:,} ({bright/total_pixels*100:.2f}%)
• 中等亮度 (128-{threshold}): {medium:,} ({medium/total_pixels*100:.2f}%)
• 较暗像素 (64-128): {dim:,} ({dim/total_pixels*100:.2f}%)
• 很暗像素 (≤64): {very_dark:,} ({very_dark/total_pixels*100:.2f}%)

🎨 核心指标:
• 亮像素总数 (>{threshold}): {bright_pixels:,}
• 暗像素总数 (≤{threshold}): {dark_pixels:,}
• 亮像素占比: {bright_percentage:.2f}%
• 暗像素占比: {(100-bright_percentage):.2f}%

⏰ 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            self.result_text.insert(tk.END, result_str)
            
            # 生成图表
            self.plot_brightness_chart(img_array, threshold)
            
        except ValueError as e:
            messagebox.showerror("错误", f"参数错误: {str(e)}")
        except Exception as e:
            messagebox.showerror("错误", f"分析过程中出现错误: {str(e)}")
    
    def plot_brightness_chart(self, img_array, threshold):
        """绘制亮度分布图表"""
        # 清除之前的图表
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        
        # 创建新窗口显示图表
        chart_window = tk.Toplevel(self.root)
        chart_window.title("亮度分布图表")
        chart_window.geometry("900x700")
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('PNG图片亮度分析图表', fontsize=16, fontweight='bold')
        
        # 1. 亮度直方图
        ax1.hist(img_array.flatten(), bins=50, color='skyblue', alpha=0.7, edgecolor='black')
        ax1.axvline(x=threshold, color='red', linestyle='--', linewidth=2, label=f'阈值: {threshold}')
        ax1.set_title('亮度值分布直方图')
        ax1.set_xlabel('亮度值 (0-255)')
        ax1.set_ylabel('像素数量')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 亮度饼图
        labels = ['很亮\n(>220)', f'较亮\n({threshold}-220)', '中等\n(128-200)', '较暗\n(64-128)', '很暗\n(≤64)']
        sizes = [
            np.sum(img_array > 220),
            np.sum((img_array > threshold) & (img_array <= 220)),
            np.sum((img_array > 128) & (img_array <= threshold)),
            np.sum((img_array > 64) & (img_array <= 128)),
            np.sum(img_array <= 64)
        ]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'lightgray']
        
        # 过滤掉大小为0的项
        non_zero_labels = [labels[i] for i in range(len(sizes)) if sizes[i] > 0]
        non_zero_sizes = [sizes[i] for i in range(len(sizes)) if sizes[i] > 0]
        non_zero_colors = [colors[i] for i in range(len(colors)) if sizes[i] > 0]
        
        ax2.pie(non_zero_sizes, labels=non_zero_labels, colors=non_zero_colors, autopct='%1.1f%%', startangle=90)
        ax2.set_title('亮度等级分布')
        
        # 3. 累积分布函数
        sorted_pixels = np.sort(img_array.flatten())
        y_vals = np.arange(len(sorted_pixels)) / float(len(sorted_pixels))
        ax3.plot(sorted_pixels, y_vals, color='purple', linewidth=2)
        ax3.axvline(x=threshold, color='red', linestyle='--', linewidth=2, label=f'阈值: {threshold}')
        ax3.fill_between(sorted_pixels, y_vals, where=(sorted_pixels > threshold), 
                        alpha=0.3, color='red', label=f'> {threshold}')
        ax3.set_title('亮度累积分布函数')
        ax3.set_xlabel('亮度值')
        ax3.set_ylabel('累积概率')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. 亮度热力图预览
        preview_size = (200, 200)  # 缩小尺寸用于预览
        preview_img = img_array.copy()
        if preview_img.shape[0] > preview_size[1] or preview_img.shape[1] > preview_size[0]:
            preview_img = np.array(Image.fromarray(preview_img).resize(preview_size))
        
        im = ax4.imshow(preview_img, cmap='gray', aspect='auto')
        ax4.set_title('图片亮度预览')
        plt.colorbar(im, ax=ax4, shrink=0.8)
        
        plt.tight_layout()
        
        # 将图表嵌入到Tkinter窗口
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 添加关闭按钮
        close_btn = tk.Button(chart_window, text="关闭图表", command=chart_window.destroy,
                             bg="#f44336", fg="white", font=("Arial", 10))
        close_btn.pack(pady=10)
    
    def save_to_csv(self):
        """保存数据到CSV文件"""
        if not hasattr(self, 'result_text'):
            messagebox.showwarning("警告", "请先进行亮度分析！")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存CSV数据",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if file_path:
                # 从文本框中提取数据并保存到CSV
                content = self.result_text.get(1.0, tk.END)
                
                # 这里可以添加更复杂的数据提取逻辑
                data = {
                    '项目': ['总像素', '亮像素', '暗像素', '亮像素占比', '平均亮度'],
                    '数值': [content.count('总像素数量'), content.count('亮像素总数'), 
                           content.count('暗像素总数'), content.count('亮像素占比'),
                           content.count('平均亮度')]
                }
                
                df = pd.DataFrame(data)
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                
                messagebox.showinfo("成功", f"数据已保存到: {file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")
    
    def export_report(self):
        """导出详细分析报告"""
        if not hasattr(self, 'result_text'):
            messagebox.showwarning("警告", "请先进行亮度分析！")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="保存分析报告",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                content = self.result_text.get(1.0, tk.END)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("PNG图片亮度像素分析报告\n")
                    f.write("=" * 60 + "\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"源文件: {self.image_path}\n\n")
                    f.write(content)
                
                messagebox.showinfo("成功", f"报告已保存到: {file_path}")
                
        except Exception as e:
            messagebox.showerror("错误", f"导出失败: {str(e)}")

def main():
    root = tk.Tk()
    app = BrightnessAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()