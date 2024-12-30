import os
import json
import shutil
from scipy.spatial import ConvexHull
import logging
import numpy as np

# 初始化日志记录器
logging.basicConfig(filename='file_processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义源文件夹和目标文件夹
folder_a = r'D:\Deeplearning\Data\XM_TWF\jier\data\0514-焊接机-TWF极耳分割_cn\json_mask'
folder_b = r'D:\Deeplearning\Data\XM_TWF\jier\data\0514-焊接机-TWF极耳分割_cn\json'

# 定义阈值
threshold_m = 650  # 假设阈值是100

# 确保目标文件夹存在
if not os.path.exists(folder_b):
    os.makedirs(folder_b)

# 遍历源文件夹中的所有文件
for filename in os.listdir(folder_a):
    # 检查文件是否为JSON文件
    if filename.endswith('.json'):
        file_path = os.path.join(folder_a, filename)

        try:
            # 读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                # 遍历shapes中的所有标签，寻找'suixie'
                for shape in data['shapes']:
                    if shape['label'] == 'sealant':
                        # 获取点集
                        points = np.array(shape['points'])
                        # 抖动数据以避免精度问题
                        perturbation = 1e-8 * np.random.randn(*points.shape)
                        points_jiggled = points + perturbation
                        # 计算多边形的大小
                        hull = ConvexHull(points_jiggled)
                        area = hull.area

                        # 检查多边形的大小是否超过阈值
                        if area < threshold_m:
                            # 如果超过阈值，将文件复制到文件夹B
                            shutil.copy2(file_path, folder_b)
                            logging.info(f'Moved file {filename} to folderB due to its large size.')
                            print(f'File {filename} has been moved to folderB due to its large size.')
                            break  # 如果文件已经复制，就不需要再处理其他标签

        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f'Error processing file {filename}: {str(e)}')

logging.info('All JSON files have been processed.')
