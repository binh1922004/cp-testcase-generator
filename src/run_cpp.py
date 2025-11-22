import subprocess
import os
import shutil

def run_file(file_name):
  
  dir = f"generators/{file_name}/"
  file_path = os.path.join(dir, f"{file_name}_gen.cpp")
  output_binary = file_name  # tên file sau khi compile

  # Compile: output binary nằm trong đúng thư mục dir
  subprocess.run(["c++", file_path, "-std=c++17", "-o", os.path.join(dir, output_binary)])

  # Run binary trong thư mục đó
  result = subprocess.run([f"./{output_binary}"], cwd=dir, capture_output=True, text=True)
  
  print(result.stdout)
  
  # Zip all child folders in the root folder
  root_folder = dir  # or specify your root folder path
  for item in os.listdir(root_folder):
    item_path = os.path.join(root_folder, item)
    if os.path.isdir(item_path):
      # Create zip file for each child folder
      shutil.make_archive(
        os.path.join(root_folder, item),  # output zip path (without .zip)
        'zip',  # archive format
        item_path  # folder to zip
      )