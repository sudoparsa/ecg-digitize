from controllers.MainController import MainController
import sys
import os
from tqdm import tqdm
from fbs_runtime.application_context.PyQt5 import ApplicationContext


RECORDS_PATH = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\ECG_Record\\'
OUT_PATH = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\csv\\'
context = ApplicationContext()
controller = MainController()


def preprocess(image_path, csv_path):
    controller.setImageFile(image_path)
    controller.digitization(csv_path, 'Comma')
    controller.closeImageFile()


def preprocess_files(records_path=RECORDS_PATH, out_path=OUT_PATH):
    images = os.listdir(records_path)
    images.remove('.paperecg')
    for image in tqdm(images, colour='blue'):
        if os.path.isfile(records_path + image):
            out_folder = out_path + '\\' + image.split('.')[0] + '\\'
            if not os.path.exists(out_folder) :
                os.makedirs(out_folder)
            preprocess(records_path + image, out_folder + image.split('.')[0] + '.csv')


if __name__=="__main__":
    preprocess_files()
    sys.exit(0)
#exit_code = context.app.exec_()
