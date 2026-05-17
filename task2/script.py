# -*- coding: utf-8 -*-
from io import BytesIO
import cv2 as cv
import numpy
import urllib3
from PIL import Image
from matplotlib import pyplot

#Zadanie drugie histogram
urladdress = 'https://wallup.net/wp-content/uploads/2015/06/Romantic-boy.jpg'
fileAddress = '/Users/ignas/PyCharmMiscProject/file.png'
print('First assignment - process image')
print('Downloading image from URL: ' + urladdress)
request = urllib3.request(method='GET', url=urladdress, headers={'User-Agent': 'Mozilla/5.0'})
#print(request.status)
if request.status == 200:
    print("Download OK, Image has been downloaded correctly")
    #Image.open(BytesIO(request.data)).show()
    image_data = numpy.frombuffer(BytesIO(request.data).getvalue(), dtype=numpy.uint8)
    decoded = cv.imdecode(image_data,cv.IMREAD_COLOR)
    if decoded is None:
        raise ValueError("Cannot decode image")
    overallhist = cv.calcHist([decoded],[0],None,[256],[0,256])
    #print(overallhist)
    pyplot.plot(overallhist)
    pyplot.title('Image Histogram')
    pyplot.xlabel('Pixel Intensity')
    pyplot.ylabel('Frequency')
    pyplot.show()
    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv.calcHist([decoded],[i],None,[256],[0,256])
        pyplot.plot(histr,color = col)
    pyplot.title('Image Histogram - RGB channels')
    pyplot.xlabel('Pixel Intensity')
    pyplot.ylabel('Frequency')
    pyplot.xlim([0,256])
    pyplot.show()
else:
    print("Download not OK - http code {code}".format(code=request.status))

