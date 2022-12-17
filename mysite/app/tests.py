from django.test import TestCase

img_endding  = {'jpg', 'png', 'img', 'mp4'}

file_name = 'myfile.ssla.jpg.mp4'

check_img = {file_name.split(".")[-1]}

if check_img.intersection(img_endding):
    print('yes')
else:
    print('no')
