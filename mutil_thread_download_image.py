import os
import pandas as pd
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# Hàm tải ảnh
def download_image(index, folder, filename, url, base_dir, max_retries=3, timeout=30):
    for attempt in range(max_retries):
        try:
            # Create directory
            folder_path = os.path.join(base_dir, folder)
            os.makedirs(folder_path, exist_ok=True)
            filename = re.sub(r'\([^)]*\)', '', filename).strip()
            file_path = os.path.join(folder_path, filename)

            # Download with increased timeout
            session = requests.Session()
            response = session.get(url, timeout=timeout)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                f.write(response.content)
                return f'Downloaded: {url} to {file_path}'

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:  # Last attempt
                return f'Error {url}: {str(e)}'
            print(f'Attempt {attempt + 1} failed, retrying...')
            time.sleep(2)  # Wait 2 seconds between retries

# Dùng multithreading
def download(filename_input, BASE_DIR = 'dataset'):
    # Đọc dữ liệu từ CSV
    df = pd.read_csv(filename_input, names=['class', 'filename', 'url'])

    # Thư mục lưu ảnh
    
    os.makedirs(BASE_DIR, exist_ok=True)
    with ThreadPoolExecutor(max_workers=300) as executor:
        futures = []
        for idx, row in df.iterrows():
            futures.append(executor.submit(download_image, idx, str(row['class']), row['filename'], row['url'], BASE_DIR))

        for future in futures:
            print(future.result())

