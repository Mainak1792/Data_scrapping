from selenium import webdriver
import requests
import os
import time
import io
from PIL import Image
from tqdm import tqdm
from selenium.webdriver.common.action_chains import ActionChains


def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(60) 


search_term=input("Keyword to Search: ")
req_imgs=int(input("Number Of Images Required : "))
save_path='C:/Users/Administrator/Documents/Data_Scraping'
save=os.path.join(save_path, search_term.replace(' ', '_'))

if not os.path.exists(save):
    os.makedirs(save)
    
# Put the path for your ChromeDriver here
DRIVER_PATH = "C:/Users/Administrator/Documents/scripts/chromedriver/chromedriver.exe"
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
a = ActionChains(wd)

URL="https://yandex.com/images/search?text="+search_term.replace(' ', '%20')+"&isize=large&type=photo"
wd.get(URL)
scroll_to_end(wd)

wd.execute_script("document.querySelector('a.serp-item__link').click();")
time.sleep(20) 

urls=[]
print("\nObtaining URLS...!")
for i in range(req_imgs):
    if i%100==0:
            print(i,end=(".."))
    try:
        actual = wd.find_element_by_class_name('MMImage-Origin')
        img_actual=actual.get_attribute('src')
        urls.append(img_actual)
        wd.find_elements_by_class_name('CircleButton-Icon')[-1].click()
        time.sleep(2)
    except:
        print("\nException")

textfile = open("C:/Users/Administrator/Documents/Data_Scraping/"+search_term.replace(' ', '_')+".txt", "w")
for element in urls:
    textfile.write(element + "\n")
textfile.close()

print("\nURLS Obtained Successfully..!\nDownloading all images...!")


# file = open('C:/Users/Pragadeesh/Documents/Wobot/Data_Scrapping/fire.txt', 'r')
# urls= file.readlines()

for index in range(len(urls)):
    print(index,end=("."))
    try:
        image_content = requests.get(urls[index].strip()).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(save,search_term.replace(' ', '_')+str(index)+".jpg")
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=100)
    except Exception as e:
        print("\nException:"+str(e))


print("\nDownloaded images successfully...!")