import os
from tqdm import tqdm
import shutil
from random import randint

Img_dir=r"C:\Users\Administrator\Desktop\ola"
all_imgs=[]
for folder in tqdm(os.listdir(Img_dir)):
    for img in  os.listdir(os.path.join(Img_dir,folder)):
        all_imgs.append(os.path.join(Img_dir,folder,img))
len(all_imgs)

# systematic Random Sampling

sample_rate=20  # In a Range of 6 pick one image in random

sampled=[]
temp=[]
for count,img in enumerate(all_imgs):
    temp.append(img)
    if count!=0 and count%sample_rate==0 :
        rand = randint(0,sample_rate-1)
        sampled.append(temp[rand])
        temp=[]
len(sampled)

sampled[10000].split("/")[-1].split("\\")[1]

for c,img in enumerate(tqdm(sampled)):
    new_folder=os.path.join(os.path.dirname(Img_dir),"Sampled","10",sampled[c].split("/")[-1].split("\\")[1])
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    shutil.copy(img,new_folder)
