from keras.models import load_model
from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input as preprocess_xception
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import ast
import sys

# classify some images
# image_paths: lists of paths to jpg images
# model_path: path to keras model
# cutoff_file: path to threshold file

def classify_image(image_paths=['img.jpg'],
    model_path=os.path.join('/home/ubuntu/checkpoints','xception05-0.236.mod')):

    # load model
    image_paths = ['/home/ubuntu/PREVIEW_SCREENSHOT1_103681.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT1_159208.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT2_159208.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT3_159208.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT4_159208.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT5_159208.jpg',
    #'/home/ubuntu/hackathon_data/AAERO/PREVIEW_SCREENSHOT6_159208.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT1_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT2_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT3_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT4_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT7_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT8_146691.jpg',
    '/home/ubuntu/hackathon_data/STAR WARS BATTLEFRONT 2/PREVIEW_SCREENSHOT9_146691.jpg']
    #'/home/ubuntu/hackathon_data/88 HEROS/PREVIEW_SCREENSHOT10_119883.jpg']
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT1_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT2_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT3_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT4_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT5_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT6_136917.jpg',
    #'/home/ubuntu/hackathon_data/88 HEROES/PREVIEW_SCREENSHOT7_136917.jpg']
    image_paths = []
    image_paths.append(sys.argv[1])

    model = load_model(model_path)

    # read genre file 
    genre_file_path = os.path.join('/home/ubuntu/training_data', 'genres.txt')
    with open(genre_file_path, 'r') as handler:
        genres = handler.readlines()

    # determine preprocess method
    preprocess_path = os.path.join('/home/ubuntu/training_data', 'preprocess.txt')
    with open(preprocess_path, 'r') as preprocess_file:
        dictionary = ast.literal_eval(preprocess_file.read())
        preprocess_method = dictionary['preprocess']
    preprocess = preprocess_xception

    # preprocess images
    input_shape = model.layers[0].input_shape
    dimension = (input_shape[1], input_shape[2])
    screenshots = [process_screen(image_path, dimension, preprocess) for image_path in image_paths]


    # predict image genre
    predictions = model.predict(np.array(screenshots))
    for prediction in predictions:
        print(prediction)
        # cutoff threshold value equals .5
        classes = [i for i in range(0, len(prediction)) if prediction[i] >= .5] 
        print('Predicted genres:')
        for c in classes:
            print(genres[c][:-1])
        #sys.exit()
        print('True genres:')


# preprocess a single screen
def process_screen(screen_file, dimension, preprocess):
    screenshot = load_img(screen_file, target_size=dimension)
    screenshot = img_to_array(screenshot)
    screenshot = np.expand_dims(screenshot, axis=0)
    screenshot = preprocess(screenshot)
    screenshot = screenshot[0]
    return screenshot

classify_image()
