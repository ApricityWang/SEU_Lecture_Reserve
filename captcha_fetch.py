
import os
import ddddocr

# 初始化 OCR 模型
ocr = ddddocr.DdddOcr()

# 设置验证码图片文件夹路径
folder_path = "./image/"

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 初始化变量来存储正确识别的数量和总图片数量
correct_count = 0
total_count = len(file_names)

# 遍历文件夹中的每张图片
for file_name in file_names:
    # 提取验证码真实值
    true_value = os.path.splitext(file_name)[0]

    # 读取图片文件
    with open(os.path.join(folder_path, file_name), 'rb') as f:
        img_bytes = f.read()

    # 使用 OCR 模型识别图片
    recognized_value = ocr.classification(img_bytes)

    print(f"原始值：{true_value}，识别结果：{recognized_value}")

    # 判断识别结果是否正确
    if recognized_value.upper() == true_value.upper():
        # 打印原始值和识别结果
        correct_count += 1

# 计算整体准确率
accuracy = correct_count / total_count * 100

# 打印整体准确率
print(f"整体准确率：{accuracy:.2f}%")