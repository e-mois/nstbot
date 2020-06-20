import sys
from PIL import Image
import numpy as np

def image_concat(img_1, img_2, user_id):
    list_im = [img_1, img_2]
    imgs = [Image.open(i) for i in list_im]
    min_shape = sorted([(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack((np.asarray( i.resize(min_shape)) for i in imgs ))

    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save(f'img/result_{user_id}.jpg')
    return f'img/result_{user_id}.jpg'    




    