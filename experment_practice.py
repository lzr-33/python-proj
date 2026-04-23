import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 测试 NumPy
data1 = [1, 3, 5, 7]
w1 = np.array(data1)
print("NumPy 测试结果：")
print("w1:", w1)

# 测试 Pandas
data = {
    'name': ['张三', '李四', '王五', '小明'],
    'sex': ['female', 'female', 'male', 'male'],
    'year': [2001, 2001, 2003, 2002],
    'city': ['北京', '上海', '广州', '北京']
}
df_test = pd.DataFrame(data)
print("\nPandas 测试结果：")
print(df_test)

# 解决中文显示问题（实验要求）
plt.rcParams['font.sans-serif'] = ['SimHei']   # 正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False     # 正常显示负号

# 1-5 / 1-6 测试 Matplotlib
plt.figure()
plt.plot(np.arange(10))
plt.title("Matplotlib 测试图像")
plt.show()


file_path = r'E:\林zr\dataset.xls'

# 读取 Excel 文件
df = pd.read_excel(file_path)

# 显示前 5 行数据
print("\n数据集前 5 行预览：")
print(df.head())

# 3-1 查看数据类型及缺失值统计
print("\n各字段数据类型：")
print(df.dtypes)

print("\n各字段缺失值统计：")
print(df.isnull().sum())

# 3-2 删除全为空的列
df.dropna(axis=1, how='all', inplace=True)

# 3-3 删除“身份证号”为空的数据
df.dropna(subset=['身份证号'], inplace=True)

# 再次查看缺失值统计结果
print("\n删除缺失值后的统计结果：")
print(df.isnull().sum())

