"""Extract signatures from an image."""
# ----------------------------------------------
# --- Author         : Ahmet Ozlu
# --- Mail           : ahmetozlu93@gmail.com
# --- Date           : 17th September 2018
# ----------------------------------------------

import cv2
# import matplotlib.pyplot as plt


import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt



from skimage import measure, morphology
from skimage.color import label2rgb
from skimage.measure import regionprops, label
import matplotlib.patches as mpatches
from copy import copy


def extract_signature(source_image):
    """Extract signature from an input image.

    Parameters
    ----------
    source_image : numpy ndarray
        The pinut image.

    Returns
    -------
    numpy ndarray
        An image with the extracted signatures.

    """

    # read the input image
    img = source_image
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # bel asfer
    plt.imshow(img)
    plt.show()
    # connected component analysis by scikit-learn framework
    blobs = img > img.mean()
    print("blobs are: " + str(blobs))
    blobs_labels = measure.label(blobs, background=1)
    print("blobs labeled are: " + str(blobs_labels))
    image_label_overlay = label2rgb(blobs_labels, image=img)

    fig, ax = plt.subplots(figsize=(10, 6))

    # plot the connected components (for debugging)
    ax.imshow(image_label_overlay)
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()

    fig, ahedi = plt.subplots(figsize=(10, 6))
    ahedi.imshow(image_label_overlay)

    the_biggest_component = 0
    total_area = 0
    counter = 0
    average = 0.0
    rects = []
    for region in regionprops(blobs_labels):
        if (region.area > 10):
            total_area = total_area + region.area
            counter = counter + 1
        # print (region.area)
        # take regions with large enough areas
        if (region.area >= 250):
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr, fill=False, edgecolor='red', linewidth=2)
            ahedi.add_patch(rect)
            rects.append([minc, maxc, minr, maxr])
            if (region.area > the_biggest_component):
                the_biggest_component = region.area

    ahedi.set_axis_off()
    plt.tight_layout()
    plt.show()

    average = (total_area / counter)
    print("the_biggest_component: " + str(the_biggest_component))
    print("average: " + str(average))

    # experimental-based ratio calculation, modify it for your cases
    # a4_constant is used as a threshold value to remove connected pixels
    # are smaller than a4_constant for A4 size scanned documents
    a4_constant = ((average / 84.0) * 250.0) + 100
    print("a4_constant: " + str(a4_constant))

    # remove the connected pixels are smaller than a4_constant
    b = morphology.remove_small_objects(blobs_labels, a4_constant)
    # save the the pre-version which is the image is labelled with colors
    # as considering connected components

    plt.imsave('pre_version.jpg', b)
    plt.imshow(b)
    plt.show()

    # read the pre-version
    img = cv2.imread('pre_version.jpg', 0)
    # ensure binary
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    clone = img.copy()

    # Display the image

    counter1 = 0

    for r in rects:
        counter1 = counter1 + 1
        print("x0: " + str(r[0]) + " y0: " + str(r[2]) + " x1: " + str(r[1]) + " y1: " + str(r[3]))
        crop_img = clone[r[2]:r[3], r[0]:r[1]]
        # cv2.imshow("crop_img", crop_img)
        cv2.imwrite("static/pictures/output/extracted_signatures/" + str(counter1) + ".jpg", crop_img)
    # save the the result
    # cv2.imwrite("output.png", img)
    return img
