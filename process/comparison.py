# import the necessary packages
import cv2
import numpy as np


def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err


def compare_images(imageA, imageB, title):
    '''
    # compute the mean squared error and structural similarity
    # index for the images
    m = mse(imageA, imageB)
    s = measure.compare_ssim(imageA, imageB)

    # setup the figure
    fig = plt.figure(title)
    plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

    # show first image
    ax = fig.add_subplot(1, 2, 1)
    plt.imshow(imageA, cmap=plt.cm.gray)
    plt.axis("off")

    # show the second image
    ax = fig.add_subplot(1, 2, 2)
    plt.imshow(imageB, cmap=plt.cm.gray)
    plt.axis("off")

    # show the images
    plt.show()
    plt.savefig(title+".jpg")
    '''
    # original = Image.open("hedisig.jpg")

    original = imageA
    # inverted_image = PIL.ImageOps.invert(original )
    # original = np.asarray(original, dtype="int32")
    # inverted_image = np.asarray(inverted_image, dtype="int32")

    original = cv2.resize(original, (500, 500))
    # inverted_image = cv2.resize(inverted_image, (500, 500))

    duplicate = imageB
    duplicate = cv2.resize(duplicate, (500, 500))
    # 1) Check if 2 images are equals
    if original.shape == duplicate.shape:
        print("The images have same size and channels")
    difference = cv2.subtract(duplicate, original)
    inverted_image = 255 - original

    gray_image = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    gray_image1 = cv2.cvtColor(duplicate, cv2.COLOR_BGR2GRAY)
    if (cv2.countNonZero(gray_image) != 0):
        result2 = (cv2.countNonZero(gray_image1) / cv2.countNonZero(gray_image)) * 100
    else:
        result2=0
    print(str(result2))

    bo, go, ro = cv2.split(inverted_image)
    b, g, r = cv2.split(difference)
    if cv2.countNonZero(bo) == 0 and cv2.countNonZero(go) == 0 and cv2.countNonZero(ro) == 0:
        result1=0
    else:
       result1 = (((1 - cv2.countNonZero(b) / cv2.countNonZero(bo)) + (1 - cv2.countNonZero(r) / cv2.countNonZero(ro)) + (
                1 - cv2.countNonZero(g) / cv2.countNonZero(go))) / 3) * 100

    result = (result1 + result2) / 2

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
        print("100%")
    else:

        print(str(result))

    # cv2.imshow("Original", original)
    # cv2.imshow("Duplicate", duplicate)
    # cv2.imshow("difference", difference)
    # cv2.imshow("inverted", inverted_image)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return result
