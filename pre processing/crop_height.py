from PIL import Image
import cv2
import os
i=0
try:
    for root, dirs, files in os.walk(r"C:\Users\Administrator\Desktop\Python\safety Jacket\safety_Jacket", topdown=False):
        for name in files:  # read_single_pic
            x = os.path.join(root, name)
            # combine_dir_and_name
            original = cv2.imread(x, cv2.IMREAD_UNCHANGED)
            width, height = original.size   # Get dimensions
            left = 0
            top = height/4
            right = 0
            bottom = 0
            cropped_example = original.crop((left, top, right, bottom))
            i += 1
            cv2.imwrite(r"CC:\Users\Administrator\Desktop\Python\cropped_image" % i, cropped_example)
except Exception as e:
    print(str(e))
