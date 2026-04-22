# -*- coding: utf-8 -*-
import urllib3
from io import BytesIO
from PIL import Image
from numpy import asarray

def print_image(image):
    print("Show Image")
    processedImage = Image.open(image)
    processedImage.show(title="Before processing")
def grayscale_image(image):
    print('Show grayscale image')
    processimage = Image.open(image)
    processimage.convert('L').show()
def change_resolution(image):
    print('Change image resolution')
    processimage = Image.open(image)
    image_h = processimage.size[1] /2
    image_w = processimage.size[0] /2
    newsize = (int(image_w), int(image_h))
    processimage.resize(newsize).show()
def rotate_image(image):
    print('Rotate image')
    processimage = Image.open(image)
    processimage.rotate(90).show()
def all_in_one_changes(image):
    print('Process image')
    processimage = Image.open(image)
    imagearray = asarray(processimage)
    print(imagearray)
    image_h = processimage.size[1] /2
    image_w = processimage.size[0] /2
    newsize = (int(image_w), int(image_h))
    newimage = processimage.resize(newsize).convert('L').rotate(90)
    newimage.show(title="After Processing")
    newimagearray = asarray(newimage)
    print(newimagearray)

#Zadanie Pierwsze procesowanie obrazu
urladdress = 'https://wallup.net/wp-content/uploads/2015/06/Romantic-boy.jpg'
fileAddress = '/Users/ignas/PyCharmMiscProject/file.png'
print('First assignment - process image')
print('Downloading image from URL: ' + urladdress)
request = urllib3.request(method='GET', url=urladdress, headers={'User-Agent': 'Mozilla/5.0'})
#print(request.status)
if request.status == 200:
    print("Download OK")
    #with open(fileAddress, 'w') as file:
    #    file.write(request.data)
    print_image(BytesIO(request.data))
    #grayscale_image(BytesIO(request.data))
    #change_resolution(BytesIO(request.data))
    #rotate_image(BytesIO(request.data))
    all_in_one_changes(BytesIO(request.data))
else:
    print("Download not OK - http code {code}".format(code=request.status))

