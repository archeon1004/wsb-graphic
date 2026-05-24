# -*- coding: utf-8 -*-
from io import BytesIO
import cv2 as cv
import numpy
import urllib3
from PIL import Image
from matplotlib import pyplot
from scipy.stats import entropy
from numpy import ndarray


def analyze_image(img: numpy.ndarray) -> dict:
    if img is None:
        raise ValueError("Ima attribute is empty")
    print("Analyzing Image function")
    #print(type(img))
    #print(img.shape)
    #print(img.ndim)
    assert len(img.shape) > 1
    if len(img.shape) == 2:
        print("Image is already a grayscale image")
        img_gray = img
    else:
        print("image is not a grayscale")
        channels = img.shape[2]
        if channels==3:
            print("3 color channels (rgb)")
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        elif channels==4:
            print("4 color channels (rgba)")
            img_gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
    assert img_gray is not None
    total_size_pixels = img_gray.size
    print("Total image pixels: " + str(total_size_pixels))
    hist = cv.calcHist([img_gray],[0],None,[256],[0,256])
    hist_norm = hist / hist.sum()
    pyplot.plot(hist_norm, color="black", alpha=0.5)
    pyplot.title('Image Histogram - Grayscale')
    pyplot.xlabel('Pixel Intensity')
    pyplot.ylabel('Frequency')
    pyplot.xlim([0,256])
    pyplot.show()
    mean                    = numpy.mean(img_gray)
    standard_deviation      = numpy.std(img_gray)
    black_clip_percentage   = numpy.sum(img_gray == 0) / total_size_pixels * 100
    white_clip_percentage   = numpy.sum(img_gray == 255) / total_size_pixels * 100
    shadows_percentage      = numpy.sum(img_gray < 50) / total_size_pixels * 100
    highlights_percentage   = numpy.sum(img_gray > 200) / total_size_pixels * 100
    image_entropy           = entropy(hist_norm, base = 2)
    issues = []
    if mean < 80:                   issues.append("Underexposed")
    if mean > 200:                  issues.append("Overexposed")
    if standard_deviation < 40:     issues.append("Low contrast")
    if black_clip_percentage > 2:   issues.append("Shadow clipping")
    if white_clip_percentage > 2:   issues.append("Highlight clipping")
    if image_entropy < 6.0:         issues.append("Low detail / flat image")

    return {
        "mean_brightness":  round(mean, 2),
        "contrast_std":     round(standard_deviation, 2),
        "entropy_bits":     image_entropy,
        "black_clip_pct":   round(black_clip_percentage, 3),
        "white_clip_pct":   round(white_clip_percentage, 3),
        "shadows_pct":      round(shadows_percentage, 2),
        "highlights_pct":   round(highlights_percentage, 2),
        "issues":           issues or ["No major issues detected"],
    }

#Zadanie drugie histogram
urladdress = 'https://wallup.net/wp-content/uploads/2015/06/Romantic-boy.jpg'
urladdress = 'https://photographylife.com/cdn-cgi/imagedelivery/GrQZt6ZFhE4jsKqjDEtqRA/photographylife.com/2013/02/Underexposure.jpg/w=1024'
urladdress = 'https://photographylife.com/cdn-cgi/imagedelivery/GrQZt6ZFhE4jsKqjDEtqRA/photographylife.com/2013/02/Overexposure.jpg/w=1024'
urladdress = 'https://photographylife.com/cdn-cgi/imagedelivery/GrQZt6ZFhE4jsKqjDEtqRA/photographylife.com/2013/02/Correct-Exposure.jpg/w=1024'
print('Second assignment - histogram and check of the image')
print('Downloading image from URL: ' + urladdress)
request = urllib3.request(method='GET', url=urladdress, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0'})
#print(request.status)
if request.status == 200:
    print("Download OK, Image has been downloaded correctly")
    #Image.open(BytesIO(request.data)).show()
    image_data = numpy.frombuffer(BytesIO(request.data).getvalue(), dtype=numpy.uint8)
    print("Show Image")
    Image.open(BytesIO(request.data)).show()
    decoded = cv.imdecode(image_data,cv.IMREAD_COLOR)
    if decoded is None:
        raise ValueError("Cannot decode image")
    color = ('b','g','r')
    b, g, r = cv.split(decoded)
    luminosity = (0.2126 *r + 0.7152 * g + 0.0722 * b).astype(numpy.uint8)
    histr_l = cv.calcHist(luminosity,[0],None,[256],[0,256])
    pyplot.plot(histr_l, color="black", alpha=0.5)
    pyplot.title('Image Histogram - Luminosity')
    pyplot.show()
    for i,col in enumerate(color):
        histr = cv.calcHist([decoded],[i],None,[256],[0,256])
        pyplot.plot(histr,color = col,alpha = 0.5)
    pyplot.title('Image Histogram - RGB channels')
    pyplot.xlabel('Pixel Intensity')
    pyplot.ylabel('Frequency')
    pyplot.xlim([0,256])
    pyplot.show()
    print("Checking Image Quality")
    image_stats = analyze_image(decoded)
    for key, value in image_stats.items():
        print (f"{key}: {value}")
else:
    print("Download not OK - http code {code}".format(code=request.status))

