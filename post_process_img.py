import os
import numpy as np
import cv2
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import argparse
from tqdm import tqdm
import timeit
import time
import shutil
import logging 

####################################################################################################
# This function modifies the input image by applying blur and posterize filters and changing certain values.
#
# Input:
# - inputPath:          (string) path to the folder where the depthmap images are located
# - outputPath:         (string) path to the folder where the images will be saved
# - img_name:           (string) image name with extension (example: DSC_6564.png)
# - blur_radius:        (float) value to be applied to the blur radius parameter
# - contrast_factor:    (float) value to be applied to the contrast factor parameter
# - brightness_factor:  (float) value to be applied to the brightness factor parameter
#
####################################################################################################
def image_processing(inputPath, outputPath, img_name, blur_radius, contrast_factor, brightness_factor):
    """
    Read Image
    """
    img = Image.open(os.path.join(inputPath, img_name))

    """
    Convert Image Mode To 'L' (This is a string specifying the pixel format used by the image). Typical values are:

        - 1 (1-bit pixels, black and white, stored with one pixel per byte)
        - L (8-bit pixels, black and white)
        - P (8-bit pixels, mapped to any other mode using a colour palette)
        - RGB (3x8-bit pixels, true colour)
        - RGBA (4x8-bit pixels, true colour with transparency mask)
        - CMYK (4x8-bit pixels, colour separation)
        - YCbCr (3x8-bit pixels, colour video format)
        - I (32-bit signed integer pixels)
        - F (32-bit floating point pixels)

    """
    convert_img = img.convert('L')

    """
    Change Image Contrast
    """
    enhancer_contrast = ImageEnhance.Contrast(convert_img)
    factor = contrast_factor 
    convert_img = enhancer_contrast.enhance(factor)

    """
    Change Image Brightness
    """
    enhancer_brightness = ImageEnhance.Brightness(convert_img)
    factor = brightness_factor 
    convert_img = enhancer_brightness.enhance(factor)

    """
    Applying The Gaussian Blur Filter
    """ 
    convert_img = convert_img.filter(ImageFilter.GaussianBlur(radius = blur_radius))
  
    """
    Applying Posterize Method
    """
    convert_img = ImageOps.posterize(convert_img, 1)

    """
    Change All Positive Value To 255
    """
    np_img = np.array(convert_img, dtype=np.uint8)
    np_img[np_img > 0] = 255
    
    """
    Save Image
    """
    cv2.imwrite(os.path.join(outputPath, img_name), np_img.astype(np.uint8))


####################################################################################################
# Main function
#
####################################################################################################
if __name__ == "__main__":
    """
    Get Start Time
    """
    start_time_main = timeit.default_timer()

    """
    Add Command Line Parameters
    """
    parser = argparse.ArgumentParser(description="mask from depthMap parameters")

    parser.add_argument("-i", "--inputPath", help="Input Folder", required=True)
    parser.add_argument("-o", "--outputPath", help="Output Folder", required=True)
    parser.add_argument("--blur_radius", help="Blur Radius [ Recommended value = 50 ]")
    parser.add_argument("--contrast_factor", help="Contrast Factor [ Recommended value = 10 ]")
    parser.add_argument("--brightness_factor", help="Brightness Factor [ Recommended value = 2 ]")

    args = parser.parse_args()

    inputPath = args.inputPath
    outputPath = args.outputPath
    blur_radius = 50.0
    contrast_factor = 10.0
    brightness_factor = 2.0

    if (args.blur_radius != None):
        blur_radius = float(args.blur_radius)
    if (args.contrast_factor != None):
        contrast_factor = float(args.contrast_factor)
    if (args.brightness_factor != None):
        brightness_factor = float(args.brightness_factor)

    """
    Process Images
    """
    for f in tqdm(os.listdir(inputPath)):
        image_processing(inputPath, outputPath, f, blur_radius, contrast_factor, brightness_factor)
    
    """
    Get Elapsed Time
    """
    elapsed_time = timeit.default_timer() - start_time_main

    """
    Now we will Create and configure logger
    """
    logging.basicConfig(filename=os.path.join(outputPath, "process_info.log"),
                        format='%(asctime)s %(message)s', 
                        filemode='w') 

    """
    Let us Create an object
    """ 
    logger=logging.getLogger() 

    """
    Now we are going to Set the threshold of logger to DEBUG
    """
    logger.setLevel(logging.DEBUG)

    """
    Write Log Message
    """
    logger.info("Input folder: " + inputPath)
    logger.info("Output folder: " + outputPath)
    logger.info("Filter parameter: ")
    logger.info("   - Contrast factor: " + str(contrast_factor))
    logger.info("   - Brightness factor: " + str(brightness_factor))
    logger.info("   - Gaussian Blur radius: " + str(blur_radius))
    logger.info("---> Time elapsed: " + time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    logger.info("--------------------------------------------------------")