import cv2
import numpy as np
import os
from scipy import ndimage
from matplotlib import pyplot as plt
import pytesseract
from tqdm import tqdm

PATH = 'ECG_Record/' # Data folder
images = os.listdir(PATH)
log_file = open('log.txt', 'w')
BUFF = ''


# Helper function to Save 2d-array to txt file
def save2txt(data, name):
    f = open(name, 'w')
    f.write(str(data.shape) + '\n')
    for line in data:
        for x in line:
            f.write(str(x) + ' ')
        f.write('\n')
    f.close()


# Helper function to display segmented ECG picture
def display_segments(path, item, axis='off'):
    plt.figure(figsize=(12, 9))
    plt.imshow(item)
    plt.title('Labeled Image')
    plt.axis(axis)
    plt.subplots_adjust(wspace=.05, left=.01, bottom=.01, right=.99, top=.9)
    plt.savefig(path)


def remove_grid(img):
    # Mask red pixels to remove grid
    lower_red = np.array([0, 0, 0])
    upper_red = np.array([50, 255, 255])
    mask = cv2.inRange(img, lower_red, upper_red)
    # Change color
    img[np.where(mask)] = 0
    img[np.where(mask == 0)] = 255
    return img


def get_grid(img):
    # Mask red pixels
    lower_red = np.array([150, 80, 80])
    upper_red = np.array([255, 240, 240])
    mask = cv2.inRange(img, lower_red, upper_red)
    # Change color
    grid = img.copy()
    grid[np.where(mask)] = [0, 0, 0]
    grid[np.where(mask == 0)] = [255, 255, 255]
    return grid


# Separate signals (leads)
def separate(img):
    mask = cv2.inRange(img, np.array([0, 0, 0]), np.array([0, 0, 0]))
    structure = np.array([[1, 1, 1],
                          [1, 1, 1],
                          [1, 1, 1]], np.uint8)
    labeled_image, nb = ndimage.label(mask, structure=structure)

    segments = []
    for i in range(1, nb + 1):
        # Extract component
        component = img.copy()
        mask = labeled_image == i
        component[np.where(mask)] = [0, 0, 0]
        component[np.where(mask == 0)] = [255, 255, 255]
        # Crop component
        sl = ndimage.find_objects(component == [0, 0, 0])
        component = component[sl[0]]
        if component.shape[1] >= 2000:
            segments.append(component)

    if len(segments) != 7:
        return False

    leads = {}
    order = ['I', 'V1', 'II', 'V2', 'III', 'V3',
             'aVR', 'V4', 'aVL', 'V5', 'aVF', 'V6']  # Order with respect to image
    for i in range(6):
        # Find line separator index
        separator_index = np.argmax([np.count_nonzero(
            segments[i][:, x] == [0, 0, 0]) for x in range(img.shape[0])]) + 1
        # Cut segment
        leads[order[2*i]] = segments[i][:, :separator_index]
        leads[order[2*i+1]] = segments[i][:, separator_index:]
    leads['I_complete'] = segments[6]

    return leads


def digitize(leads):
    # TODO
    return


def preprocess(path, out_name, folder='out/'):
    img = cv2.imread(path)
    height, width, depth = img.shape

    # Split grid
    grid = get_grid(img)
    img = remove_grid(img)

    # Crop image
    head = img[:222, :]
    ecg = img[222:1965, :]

    # Separation
    leads = separate(ecg)

    # Digitization
    if leads:  # Check segmentation error
        digitize(leads)

    # Save output
    directory = out_name.split('.')[0]
    out_path = os.path.join(folder, directory)
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    cv2.imwrite(out_path + '\img.jpg', ecg)
    cv2.imwrite(out_path + '\grid.jpg', grid)
    cv2.imwrite(out_path + '\head.jpg', head)
    if leads == False:
        print('Segmentation error in file ' + path + '\n')
        global BUFF
        BUFF = BUFF + 'Segmentation error in file ' + path + '\n'
    else:
        separated_path = out_path + '/separated/'
        if not os.path.isdir(separated_path):
            os.mkdir(separated_path)
        for lead, img in leads.items():
            cv2.imwrite(separated_path + lead + '.jpg', img)


for image in tqdm(images):
    print(image)
    preprocess(os.path.join(PATH, image), image)
    break

log_file.write(BUFF)
log_file.close()
