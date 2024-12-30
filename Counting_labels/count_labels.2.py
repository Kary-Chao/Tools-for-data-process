import os
import json

def count_labels(json_file, target_label):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return sum(1 for item in data['shapes'] if item['label'] == target_label)

def move_files(src_folder, dst_folder, threshold):
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)

    for file in os.listdir(src_folder):
        if file.endswith('.json'):
            src_file = os.path.join(src_folder, file)
            dst_file = os.path.join(dst_folder, file)
            count = count_labels(src_file, target_label)
            if count > threshold:
                os.rename(src_file, dst_file)
                print(f"Moved {src_file} to {dst_file}")

if __name__ == "__main__":
    src_folder = r"D:\Deeplearning\Data\XNA-Gaimao\3\智能标注\3\json-ok"
    dst_folder = r"D:\Deeplearning\Data\XNA-Gaimao\3\智能标注\3\json-待修改"
    target_label = 'gaimao'
    threshold = 1  # 设置数量阈值，可以根据需要调整
    move_files(src_folder, dst_folder, threshold)
