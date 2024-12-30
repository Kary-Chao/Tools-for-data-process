import os
import json
import shutil
from scipy.spatial import ConvexHull

# 定义源文件夹和目标文件夹
folder_a = r'D:\Deeplearning\Data\XM_TWF\jier\data\sealant-seg-0514_zc\智能标注\json_mask'
folder_b = r'D:\Deeplearning\Data\XM_TWF\jier\data\sealant-seg-0514_zc\智能标注\pro'

# 定义阈值
threshold_m = 2000  # 假设阈值是100

#定义目标缺陷
target_label = input('')

# 确保目标文件夹存在
if not os.path.exists(folder_b):
    os.makedirs(folder_b)
# 遍历源文件夹中的所有文件
for filename in os.listdir(folder_a):
    # 检查文件是否为JSON文件
    if filename.endswith('.json'):
        file_path = os.path.join(folder_a, filename)
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # 遍历shapes中的所有标签，寻找'suixie'
            for shape in data['shapes']:
                if shape['label'] == target_label:
                    # 获取点集
                    points = shape['points']
                    # 计算多边形的大小
                    hull = ConvexHull(points)
                    area = hull.area
                    # 检查多边形的大小是否超过阈值
                    if area < threshold_m:
                        # 如果超过阈值，将文件复制到文件夹B
                        shutil.move(file_path, folder_b)
                        print(f'File {filename} has been moved to folderB due to its large size.')
                        break  # 如果文件已经复制，就不需要再处理其他标签
print('All JSON files have been processed.')