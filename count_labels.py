import os.path as osp
import os
import cv2
import json
import numpy as np
import glob

label_count = {}
image_count = {}

dataset_dir = r'E:\Deeplearning\Data\ASC1-TWF\模型数据集-241212\ASC1-头部碎屑-Tab断裂-数据集-20241212095944\json_mark'
label_files = glob.glob(osp.join(dataset_dir, "*.json"))

for i in label_files:
    data = json.load(open(i),encoding='utf-8')
    labels = [shape['label'] for shape in data['shapes']]
    for label in labels:
        if label not in label_count:
            label_count[label] = 0
        label_count[label] += 1

    labelnames = list(set(labels))
    for name in labelnames:
        if name not in image_count:
            image_count[name] = 0
        image_count[name] += 1


print("==============="*3)
print("标签数统计结果：")
for label, count in label_count.items():
    print(f"{label} 实例个数为: {count}")

print("==============="*3)
print("图片数量统计结果：")
for label, count in image_count.items():
    print(f"{label} 图片数量为: {count}")
