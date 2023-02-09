import json
import os

def load_dict(filename):
    with open(filename, "r") as json_file:
        dic = json.load(json_file)
    return dic

def get_img_list(path):
    is_img = lambda x: any(x.endswith(extention)
                            for extention in ['jpg','png','gif','bmp'])
    return [os.path.join(r,i) for r, _, f in os.walk(path) for i in f if is_img(i)]


f = '150obj_onehotmatrix_places14.json'
ff = load_dict(f)
c = 0
for k,v in ff.items():
    c+=1
print(c)

'''
p = '/home/data/cenj/bomiao/camera_cls/data/datasets/places365_train_2/'
img = get_img_list(p)

print(len(set(img)))
'''
