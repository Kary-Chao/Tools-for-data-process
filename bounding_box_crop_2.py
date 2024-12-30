from PIL import Image
import numpy as np
import cv2
import os
import xml.etree.ElementTree as ET

# 定义图像和标注文件的路径
ori_img_path = r'C:\Users\Charl\Downloads\PKG-极片分割-2D_V5\智能标注\images'
anno_xml_path = r'C:\Users\Charl\Downloads\PKG-极片分割-2D_V5\智能标注\annotations'
dst_img_path = r'C:\Users\Charl\Downloads\PKG-极片分割-2D_V5\智能标注\crop'

# 创建输出目录，如果它不存在的话
if not os.path.exists(dst_img_path):
    os.makedirs(dst_img_path)

# 遍历标注文件夹中的所有XML文件
for anno_file in os.listdir(anno_xml_path):
    if anno_file.endswith('.xml'):
        try:
            # 解析XML文件
            tree = ET.parse(os.path.join(anno_xml_path, anno_file))
            root = tree.getroot()

            # 获取图像文件名
            img_filename = root.find('filename').text
            img_path = os.path.join(ori_img_path, img_filename)

            # 检查图像文件是否存在
            if not os.path.isfile(img_path):
                print(f"Warning: Image file does not exist for annotation {anno_file}.")
                continue

            # 使用Pillow读取图像
            img_pil = Image.open(img_path)

            # 将Pillow图像转换为NumPy数组
            img = np.array(img_pil)

            # 获取所有的object元素
            objects = root.findall('object')

            # 遍历每个object
            for idx, obj in enumerate(objects):
                # 获取类别名称
                name = obj.find('name').text

                # 获取边界框坐标
                bndbox = obj.find('bndbox')
                xmin = int(bndbox.find('xmin').text)
                ymin = int(bndbox.find('ymin').text)
                xmax = int(bndbox.find('xmax').text)
                ymax = int(bndbox.find('ymax').text)

                # 裁剪图像
                cropped_img = img[ymin:ymax, xmin:xmax]

                # 构建裁剪图像的保存路径
                # 使用类别名称和序号作为文件名的一部分
                cropped_img_path = os.path.join(dst_img_path, f"{name}_{idx}_{os.path.splitext(img_filename)[0]}_cropped.jpg")

                # 保存裁剪后的图像
                cropped_img_pil = Image.fromarray(cropped_img)
                cropped_img_pil.save(cropped_img_path)

        except Exception as e:
            print(f"Error processing file {anno_file}: {str(e)}")
