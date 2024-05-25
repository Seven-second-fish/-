import os
import sys

def replace_filenames(root_dir, old_prefix, new_prefix):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.startswith(old_prefix):
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(old_prefix, new_prefix, 1)
                new_path = os.path.join(dirpath, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <old_prefix> <new_prefix>")
        sys.exit(1)

    folder_path = os.getcwd()  # 获取当前脚本所在文件夹的路径
    old_prefix = sys.argv[1]
    new_prefix = sys.argv[2]

    replace_filenames(folder_path, old_prefix, new_prefix)

