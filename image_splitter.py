'''
This file contains an image converter which formats an image to be 
recognised by the number_splitter functin and 
'''
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def image_converter(img, threshold = 0.7):
    '''
    Takes in image file name. 
    Converts image to greyscale, normalizes it by dividing by 255
    and then inverts it.
    Threshold is the number of which any pixel (normalized) 
    below which the pixel will be set to 0
    '''
    
    image = cv.imread(img, cv.IMREAD_GRAYSCALE)
    image_arr = np.array(image)
    full_image = image_arr / 255
    full_image = full_image - 1
    full_image = full_image * -1
    full_image = np.where(full_image > 0.7, full_image, 0)
    
    return full_image

    
def number_splitter(image, n, expand_height = 0, size = (28,28)):
    """
    This function takes in an image, which must be in inverse greyscale 
    format and have no background noise (i.e, pixels that are 
    not numbers are 0).
    This image must also have only one row of numbers
    n -> the expected gap (measured in pixels) between numbers to split by
    expand_height -> number of pixels by which the images will be centred
    by, for example 0, means that the final image will have no "empty"
    pixels above the number
    size -> tuple, the size of which returning images are reformatted to.
    Returns a numpy array of images.
    """

    #This part identifies all co-ordiantes that are non-zero
    t = np.unique(np.where(image != 0)[0])
    t1 = np.unique(np.where(image != 0)[1])
    
    coordinate_list = []
    cycle = -1
    count = 0
    for i in t1:
    
        count += 1
        # Just to assign a dummy prev_i variable for the very 
        # first iteration of the loop
        if cycle == -1:
            prev_i = i
            cycle = 0
            coordinate_list.append(i)

        #If the gap between two non-zero pixels is greater than 
        # n pixels, record co-ordinates
        if (i - prev_i) > n:
            cycle = 0
            coordinate_list.append(prev_i)
            coordinate_list.append(i)
        prev_i = i
    
        #This catches the last co-ordinate
        if count == len(t1):
            coordinate_list.append(i)

    coords = coordinate_list[:] # just shorter to write with

    # - Now this section deals with formatiing the image and resizing it -
    final_list = []
    expand_height = expand_height // 2

    #This loop grabs each pair of co-ordinates generated earlier.
    for i in range(0,len(coords),2):
    
        # Here we retrieve the non-zero pixels in the ranges we got earlier.
        # We use this to find the highet and lowest pixel of the number (by y axis)
        nonz = np.unique(np.where(image[:,coords[i]:coords[i+1]] != 0)[0]) 
        
        highest = np.max(nonz) + expand_height # new highest point of image
        lowest = np.min(nonz) - expand_height # new lowest point of image
        distance = highest - lowest # Basically height of number with expansion
        middle = (coords[i] + coords[i+1]) // 2 # find middle of number
        first = middle - (distance // 2) # Expanding start of image for number
        last = middle + (distance // 2) # Expanding end of image for number
        
        final_list.append((first,last, highest, lowest))

    #This uses the co-ordinates to grab the images,
    # resize them and append to a list.
    image_list = []
    for c in final_list:
        z = image[c[3]:c[2],c[0]:c[1]]
        z = cv.resize(z, dsize = (28,28))
        image_list.append(z)
    
    image_list_array = np.asarray(image_list)

    return(image_list_array)