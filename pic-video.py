# Modifying the code to handle multiple subfolders in a parent directory, processing images in each subfolder separately

modified_code_for_subfolders = '''
import os
import sys
import logging
import re
from PIL import Image, ImageFile
from moviepy.editor import ImageSequenceClip
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 移除图像大小的限制
Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

def numerical_sort_key(filename):
    """Generates a key for sorting filenames numerically."""
    parts = re.split(r'(\\d+)', filename)
    parts[1::2] = map(int, parts[1::2])
    return parts

def resize_image(image_path, target_height, target_width):
    """调整图片大小以适应目标尺寸，同时保持宽高比"""
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            if width / height > target_width / target_height:
                new_width = target_width
                new_height = int(target_width * height / width)
            else:
                new_height = target_height
                new_width = int(target_height * width / height)

            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            new_img = Image.new("RGB", (target_width, target_height))
            new_img.paste(resized_img, ((target_width - new_width) // 2, (target_height - new_height) // 2))
            
        return new_img
    except Exception as e:
        logging.error(f"Error resizing image {image_path}: {e}")
        return None

def find_images_in_subfolder(subfolder, extensions=('.png', '.jpg', '.jpeg', 'bmp', 'PNG', 'JPG', 'JPEG')):
    """在子文件夹中查找图片并按数字顺序排序"""
    images = []
    for file in os.listdir(subfolder):
        if file.lower().endswith(extensions) and not file.startswith('._'):
            images.append(os.path.join(subfolder, file))
    images.sort(key=numerical_sort_key)
    return images

def process_images_in_subfolder(subfolder, target_size):
    """处理子文件夹中的图片"""
    image_paths = find_images_in_subfolder(subfolder)
    processed_images = []
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda path: process_image(path, target_size), image_paths))
    processed_images.extend(res for res in results if res)
    return processed_images

def process_image(image_path, target_size):
    """调整单个图片大小并保存为临时文件"""
    logging.info(f"Resizing image: {image_path}")
    resized_image = resize_image(image_path, target_size[1], target_size[0])
    if resized_image:
        temp_path = f"{image_path}_temp.jpg"
        resized_image.save(temp_path)
        return temp_path
    return None

def create_video(image_files, output_file='output_video.mp4'):
    """从图片文件创建视频"""
    try:
        clip = ImageSequenceClip(image_files, fps=1)
        clip.write_videofile(output_file, fps=1, logger='bar')
    except Exception as e:
        logging.error(f"Error creating video: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <parent_folder_path>")
        sys.exit(1)

    parent_folder = sys.argv[1]
    subfolders = [os.path.join(parent_folder, d) for d in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, d))]
    subfolders.sort()  # Sort the subfolders if needed

    all_images = []
    for subfolder in subfolders:
        all_images.extend(process_images_in_subfolder(subfolder, (1080, 1920)))

    create_video(all_images)

    # 清理临时文件
    for image_file in all_images:
        os.remove(image_file)
'''

# Writing the modified code to handle multiple subfolders to a file
modified_code_path = '/mnt/data/modified_code_for_subfolders.py'
with open(modified_code_path, 'w') as file:
    file.write(modified_code_for_subfolders)

modified_code_path
