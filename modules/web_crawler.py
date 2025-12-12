import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin ##to make links join

def crawler(target_url, file_extension):

    download_folder = "web_crawler_downloads";

    if not os.path.exists(download_folder):
        os.makedirs(download_folder);
        print(f"{download_folder} has been created");

    try:
        #to pose as a web browser
        headers = {"User-Agent": "Mozilla/5.0"};
        response = requests.get(target_url, headers=headers);

        if response.status_code != 200:
            print(f"ERROR: Could not access website. Status: {response.status.code}");
            return;

        soup = BeautifulSoup(response.text, "html.parser");

        tags = soup.find_all(["a","img"]);
    
        count = 0;

        for tag in tags:
            link = tag.get("href") or tag.get("src");

            if link and link.endswith(file_extension):
                
                full_url = urljoin(target_url, link);
                filename = os.path.basename(link);

                save_path = os.path.join(download_folder, filename);

                try:
                    print(f"Downloadin: {filename}");
                    file_data = requests.get(full_url,headers=headers).content;
                    
                    with open(save_path, "wb") as f:
                        f.write(file_data);

                    count += 1;
                    print(f"Saved: {save_path}");

                except Exception as e:
                    print(f"Download FAILED: {e}");
        
    
    except Exception as e:
        print(f"ERROR: {e}");

if __name__ == "__main__":

    target_url = input("Enter Target URL: ") or "https://en.wikipedia.org/wiki/Never_Gonna_Give_You_Up";
    file_extension = input("Enter desired file extension to download: ").strip() or "png";
    
    ##add dot if not exists
    if not file_extension.startswith("."):
        file_extension = "." + file_extension;

    crawler(target_url, file_extension);