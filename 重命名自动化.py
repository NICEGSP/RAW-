import os
import datetime
import exifread
import shutil
import sys


print("本软件完全免费，作者：NICE蛋蛋")
print("支持的格式(大小写通用)：.dng.jpg.jpeg.tiff.cr2.nef.orf.arw.sr2.rw2")
print("默认是复制[导入原图]中的文件粘贴到[导出图片]文件夹，会保留原文件，请确保有原文件两倍的存储空间！")
n=input("按回车键继续：")
# 获取程序所在文件夹路径
program_path = os.path.abspath(sys.argv[0])
program_dir = os.path.dirname(program_path)

# 定义要导入和导出的文件夹路径
import_folder = os.path.join(program_dir, "导入原图")
export_folder = os.path.join(program_dir, "导出图片")

# 如果导出文件夹不存在，创建文件夹
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

# 获取导入文件夹中的所有文件
for filename in os.listdir(import_folder):
    # 获取文件路径
    filepath = os.path.join(import_folder, filename)

    # 判断文件是否为DNG、JPG、JPEG、TIFF、CR2、NEF、ORF、ARW、SR2、RW2格式
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".dng", ".jpg", ".jpeg", ".tiff", ".cr2", ".nef", ".orf", ".arw", ".sr2", ".rw2"]:
        continue

    # 读取文件的EXIF信息
    with open(filepath, "rb") as f:
        tags = exifread.process_file(f)

    # 获取照片的拍摄日期和时间
    try:
        date_str = str(tags["EXIF DateTimeOriginal"])
        date_obj = datetime.datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    except Exception as e:

        print(f"读取照片{filename}的拍摄日期和时间失败：{str(e)}")
        continue

    # 获取照片的拍摄机型和镜头型号
    camera_model = str(tags.get("Image Model", "")).replace(" ", "_")
    lens_model = str(tags.get("EXIF LensModel", "")).replace(" ", "_")

    # 根据拍摄日期和时间和文件格式重命名文件
    new_filename = f"{camera_model}_{lens_model}_{date_obj.strftime('%Y%m%d_%H%M%S')}{ext.upper()}"

    # 如果该文件名已经存在，添加后缀
    i = 1
    while os.path.exists(os.path.join(export_folder, new_filename)):
        new_filename = f"{camera_model}_{lens_model}_{date_obj.strftime('%Y%m%d_%H%M%S')}_{i}{ext.upper()}"
        i += 1

    # 保存文件到导出文件夹中
    new_filepath = os.path.join(export_folder, new_filename)
    shutil.copyfile(filepath, new_filepath)

    # 打印重命名的过程
    print(f"重命名文件{filename}为{new_filename}")

n=input("处理完毕，按回车键结束：")
