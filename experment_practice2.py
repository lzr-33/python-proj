# ==============================
# 1. 导入库
# ==============================
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ==============================
# 2. 读取数据（你指定的路径）
# ==============================
file_path = r"E:\林zr\dataset.xls"

data = pd.read_excel(file_path)
print("✅ 数据读取成功")
print("原始列名：", data.columns.tolist())

# ==============================
# 3. 数据预处理
# ==============================

# 3-1 处理“开始从事工作年份” → “参加工作时间”
data['参加工作时间'] = data['开始从事工作年份'].astype(str).str.extract(r'(\d{4})')
data['参加工作时间'] = pd.to_numeric(data['参加工作时间'], errors='coerce')
data.drop(columns=['开始从事工作年份'], inplace=True)

# 3-2 强制把“体检年份”转成数值（⭐关键修复）
data['体检年份'] = pd.to_numeric(data['体检年份'], errors='coerce')

# 3-3 删除缺失值
data.dropna(subset=['体检年份', '参加工作时间'], inplace=True)

# 3-4 计算工龄
data['工龄'] = data['体检年份'] - data['参加工作时间']
print("\n已成功计算工龄")
print(data[['性别', '体检年份', '参加工作时间', '工龄']].head())

# ==============================
# 4. 不同性别白细胞计数均值
# ==============================
gender_wbc_mean = data.groupby('性别')['白细胞计数'].mean()
print("\n--- 不同性别白细胞均值 ---")
print(gender_wbc_mean)

plt.figure(figsize=(6, 4))
gender_wbc_mean.plot(kind='bar', color=['steelblue', 'salmon'])
plt.xlabel('性别')
plt.ylabel('白细胞均值')
plt.title('不同性别白细胞计数平均值')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# ==============================
# 5. 工龄段分析（替代年龄段）
# ==============================
bins = [0, 5, 10, 15, float('inf')]
labels = ['≤5年', '6~10年', '11~15年', '>15年']

data['工龄段'] = pd.cut(data['工龄'], bins=bins, labels=labels)
workyear_wbc_mean = data.groupby('工龄段')['白细胞计数'].mean()

print("\n--- 不同工龄段白细胞均值 ---")
print(workyear_wbc_mean)

plt.figure(figsize=(8, 4))
workyear_wbc_mean.plot(kind='bar', color='green')
plt.xlabel('工龄段')
plt.ylabel('白细胞计数均值')
plt.title('不同工龄段白细胞计数平均值')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()