#!/usr/bin/python
"""Python main file."""
# -*- coding: utf-8 -*-
# -----------------------------------------
# author      : Ahmet Ozlu
# mail        : ahmetozlu93@gmail.com
# date        : 05.05.2019
# -----------------------------------------

from os import listdir
from os.path import isfile, join

import cv2
import numpy

from process import color_correlation, signature_extractor
from process import comparison
from process import unsharpen
from process.comparison import compare_images


def process(test_signature, real_signature):
    source_image = cv2.imread(test_signature)
    img = 0
    try:
        # read the source input image and call the dewarp_book function
        # to perform cropping with the margin and book dewarping
        img = source_image
        cv2.imwrite("static/pictures/output/dewarped.jpg", img)
        print("- step1 (cropping with the argins + book dewarpping): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN CROPPING & BOOK DEWARPING! PLEASE CHECK LIGTHNING,"
              " SHADOW, ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:
        # call the unsharpen_mask method to perform signature extraction
        img = signature_extractor.extract_signature(cv2.cvtColor(img,
                                                                 cv2.COLOR_BGR2GRAY))

        print("- step2 (signature extractor): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN SIGNATURE EXTRACTION! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:
        image_list = []

        mypath = 'static/pictures/output/extracted_signatures'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = numpy.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
            im = cv2.imread(join(mypath, onlyfiles[n]))
            # call the unsharpen_mask method to perform unsharpening mask
            im = unsharpen.unsharpen_mask(im)
            cv2.imwrite("static/pictures/output/unsharpening/" + onlyfiles[n], im)
        print("- step3 (unsharpening mask): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN BOOK UNSHARPING MASK! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:

        mypath = 'static/pictures/output/unsharpening'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = numpy.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
            im = cv2.imread(join(mypath, onlyfiles[n]))
            # call the unsharpen_mask method to perform unsharpening mask
            im = color_correlation.funcBrightContrast(im)
            cv2.imwrite("static/pictures/output/correlation/" + onlyfiles[n], im)

        print("- step4 (color correlation): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN BOOK COLOR CORRELATION! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")

    realsignature = cv2.imread(real_signature)
    mypath = 'static/pictures/output/correlation'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = numpy.empty(len(onlyfiles), dtype=object)

    # realsignature = cv2.resize(realsignature, (1000, 1000))
    # realsignature = cv2.cvtColor(realsignature, cv2.COLOR_BGR2GRAY)
    max = 0
    acc = 0
    for n in range(0, len(onlyfiles)):
        im = cv2.imread(join(mypath, onlyfiles[n]))
        # call the unsharpen_mask method to perform unsharpening mask
        im = color_correlation.funcBrightContrast(im)
        cv2.imwrite("./output/final/" + onlyfiles[n], im)

    for n in range(0, len(onlyfiles)):
        im = cv2.imread(join(mypath, onlyfiles[n]))
        # im = cv2.resize(im, (1000, 1000))
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        print("- comparing picture " + str(n) + " to  real signature: OK")
        acc = compare_images(im, realsignature, "comparing_" + str(onlyfiles[n]) + "_to_ hedi_signature")
        if acc > max:
            max = acc

    print("- final step : OK")

    return max


def process1(test_signature, namepic):
    source_image = cv2.imread(test_signature)
    # img = 0
    # try:
    #     # read the source input image and call the dewarp_book function
    #     # to perform cropping with the margin and book dewarping
    #     img = source_image
    #     cv2.imwrite("static/pictures/output/dewarped.jpg", img)
    #     print("- step1 (cropping with the argins + book dewarpping): OK")
    # except Exception as e:
    #     print("type error: " + str(e))
    #     print("ERROR IN CROPPING & BOOK DEWARPING! PLEASE CHECK LIGTHNING,"
    #           " SHADOW, ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:
        # call the unsharpen_mask method to perform signature extraction
        signature_extractor.extract_signature(cv2.cvtColor(source_image,
                                                                 cv2.COLOR_BGR2GRAY))

        print("- step2 (signature extractor): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN SIGNATURE EXTRACTION! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:
        image_list = []

        mypath = 'static/pictures/output/extracted_signatures'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = numpy.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
            im = cv2.imread(join(mypath, onlyfiles[n]))
            # call the unsharpen_mask method to perform unsharpening mask
            im = unsharpen.unsharpen_mask(im)
            cv2.imwrite("static/pictures/output/unsharpening/" + onlyfiles[n], im)
        print("- step3 (unsharpening mask): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN BOOK UNSHARPING MASK! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")
    try:

        mypath = 'static/pictures/output/unsharpening'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        images = numpy.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
            im = cv2.imread(join(mypath, onlyfiles[n]))
            # call the unsharpen_mask method to perform unsharpening mask
            im = color_correlation.funcBrightContrast(im)
            cv2.imwrite("static/pictures/output/correlation/" + onlyfiles[n], im)

        print("- step4 (color correlation): OK")
    except Exception as e:
        print("type error: " + str(e))
        print("ERROR IN BOOK COLOR CORRELATION! PLEASE CHECK LIGTHNING, SHADOW,"
              " ZOOM LEVEL AND ETC. OF YOUR INPUT BOOK IMAGE!")

    mypath = 'static/pictures/output/correlation'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    images = numpy.empty(len(onlyfiles), dtype=object)

    # realsignature = cv2.resize(realsignature, (1000, 1000))
    # realsignature = cv2.cvtColor(realsignature, cv2.COLOR_BGR2GRAY)
    max = 0
    acc = 0
    for n in range(0, len(onlyfiles)):
        im = cv2.imread(join(mypath, onlyfiles[n]))
        # call the unsharpen_mask method to perform unsharpening mask
        im = color_correlation.funcBrightContrast(im)
        cv2.imwrite("static/pictures/" + namepic + ".jpg", im)

    return 0
