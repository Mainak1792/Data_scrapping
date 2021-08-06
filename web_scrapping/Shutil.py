import time
from selenium import webdriver
import requests
from PIL import Image
import os
import io
from tqdm import tqdm
import cv2

def scroll_to_end(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(6)


def extract_img(wd, page_num, save_path):
    page_results = wd.find_elements_by_css_selector('img.z_h_9d80b.z_h_2f2f0')
    number_results = len(page_results)

    print(f"\nFOUND- {number_results} images in Page {page_num}")

    image_urls = []
    for img in page_results:
        image_urls.append(img.get_attribute('src'))

    for img_url in tqdm(image_urls):
        image_content = requests.get(img_url).content
        image_file = io.BytesIO(image_content)

        image = Image.open(image_file).convert('RGB')
        # image = cv2.resize(image, (360, 360), interpolation=cv2.INTER_AREA)
        w, h = image.size[0:2]
        crop_img = image.crop((0, 0, w, h - 20))
        file_path = os.path.join(save_path, img_url.split('/')[-1])
        with open(file_path, 'wb') as f:
            crop_img.save(f, "JPEG", quality=100, subsampling=0)

    print("SUCCESS - saved images from this page")


search_term = input("Keyword to Search: ")
req_imgs = int(input("Number Of Images Required : "))
save_path = r'C:\Users\Administrator\Desktop\New folder'  # change path if required
save = os.path.join(save_path, search_term)
if not os.path.exists(save):
    os.makedirs(save)

# Put the path for your ChromeDriver here
DRIVER_PATH = r"C:\Users\Administrator\Desktop\chromedriver.exe"  # change path
wd = webdriver.Chrome(executable_path=DRIVER_PATH)

URL = 'https://www.shutterstock.com/search/' + search_term.replace(' ',
                                                                   '+') + '?kw=shutterstock&c3apidt=p30791382916&msclkid=038b1d6f0433154f952a7dfbd713ed84&utm_source=bing&utm_medium=cpc&utm_campaign=IN_en_image_brand&utm_term=shutterstock&utm_content=brand_brand_exact&gclid=038b1d6f0433154f952a7dfbd713ed84&gclsrc=3p.ds&image_type=photo&mreleased=true'

wd.get(URL)

scroll_to_end(wd)

tot_pg = wd.find_elements_by_css_selector('div.b_aI_c6506.z_b_510de')
total_pg = int(tot_pg[0].text.split(" ")[-1].replace(',', ''))

for pg in range(0, total_pg + 1):
    if pg < total_pg + 1 and len(os.listdir(save)) < req_imgs:
        scroll_to_end(wd)
        extract_img(wd, pg, save)
        wd.execute_script(
            "document.querySelector('a.z_b_6e283.oc_v_453f4.b_h_9156a.b_h_f4d86.b_h_1a7bb.b_h_97f8c.b_h_ce5e9.b_h_31b1c.b_h_276d2.oc_v_d7a53.b_h_aaea6.b_h_695d2').click();")
        time.sleep(2)
    else:
        wd.quit()
        print("Saved in " + save_path)
        print("\n------------DOWNLOAD COMPLETED------------")
        break
