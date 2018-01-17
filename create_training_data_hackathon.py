import numpy as np
import json
import os
import random

from keras.applications import imagenet_utils
from keras.applications.inception_v3 import preprocess_input as preprocess_xception
from keras.preprocessing.image import load_img, img_to_array

# dimension: (height, width) of image
# train_split: fraction of data to use for training
# target: what to classify. Currently the only supported option is 'genre'

def create_training_data(dimension, train_split=0.8) 


    product_cat_map = {}
    categories = set()
    category_target = {}
    with open('product_cat_map') as f:
        products = f.readlines()

    # build product_cat_map, product_id -> category_name
    for p in products:
        columns = p.split('\t')
        product_cat_map[columns[0]] =  columns[1]
        categories.add(columns[1])

    # create index for each category
    for i, cat in enumerate(categories):
        category_target[cat] = i


    # scraped images placed here
    data_dir = '../../hackathon_data'

    # output going here:
    output_dir = 'training_data'

    preprocess = preprocess_xception

    # training and test data
    train_X = []
    train_Y = []
    test_X = []
    test_Y = []

    counter = 0
    total_count = len(os.listdir(data_dir))
    collect_training = True

    # iterate over game folders, randomly permuted
    print('Processing raw data')
    folders = os.listdir(data_dir)
    random.shuffle(folders)
    for folder in folders:
        counter += 1
        if counter % 100 == 0:
            print(counter)
        if counter > train_split * total_count:
            collect_training = False
        screen_dir = os.path.join(data_dir, folder)
        if not os.path.isdir(screen_dir):
            continue
        target_file = os.path.join(screen_dir, 'attributes')
        screen_files = []
        suffix = '.jpg'
        for filename in os.listdir(screen_dir):
            if filename.endswith(suffix):
                screen_files.append(os.path.join(screen_dir, filename))
        # sanity check: if we found no screen, let's skip
        if screen_files == []:
            continue
        # read meta data from attribute file
        target_id = -1
        with open(target_file, 'r') as game_info_file:
            game_info = game_info_file.read()
            colunns = game_info.split('\t')
            product_id = columns[0]
            genre = []
            genre.append(product_cat_map[product_id])
            if not genre:
                continue
            target_id = category_target[genre] 

        # add to training/test data
        for screen_file in screen_files:
            screenshot = process_screen(screen_file, dimension, preprocess)
            train_X.append(screenshot)
            train_Y.append(target_id)

    print('Transforming test data')
    # transform genre lists to 1/-1 vector
    number_of_genres = len(category_target)
    train_Y = transform_to_binary_matrix(train_Y, number_of_genres)
    test_Y = transform_to_binary_matrix(test_Y, number_of_genres)

    print('Creating arrays')
    # turn everything into proper numpy arrays
    train_X = np.asarray(train_X, dtype='float32')
    test_X = np.asarray(test_X, dtype='float32')
    train_Y = np.asarray(train_Y, dtype='int8')
    test_Y = np.asarray(test_Y, dtype='int8')

    # dump everything into files
    print('Writing data')

    # genres
    genre_file_path = os.path.join(output_dir, 'genres.txt')
    with open(genre_file_path, 'w') as genre_file:
        [genre_file.write(genre + os.linesep) for genre in category_target]

    # preprocess type
    preprocess_path = os.path.join(output_dir, 'preprocess.txt')
    with open(preprocess_path, 'w') as preprocess_file:
        data = dict()
        data['preprocess'] = preprocess_method
        preprocess_file.write(str(data))

    # training/test data
    train_X_path = os.path.join(output_dir, 'train_X.npy')
    train_Y_path = os.path.join(output_dir, 'train_Y.npy')
    test_X_path = os.path.join(output_dir, 'test_X.npy')
    test_Y_path = os.path.join(output_dir, 'test_Y.npy')
    np.save(train_X_path, train_X)
    np.save(train_Y_path, train_Y)
    np.save(test_X_path, test_X)
    np.save(test_Y_path, test_Y)

    # print some info
    print(str(number_of_genres) + ' genres found.')
    for genre, index in category_target:
        train_count = len([i for i in train_Y if i[index] == 1])
        test_count = len([i for i in test_Y if i[index] == 1])
        print(genre + ' ' + str(train_count) + ' ' + str(test_count))

# transform genre id list to binary matrix
def transform_to_binary_matrix(data, count):
    for row in range(0, len(data)):
        ids = data[row]
        data[row] = np.asarray([1 if i in ids else 0 for i in range(0, count)], dtype='bool')
    return data

# preprocess a single screens using keras image processing lib
def process_screen(screen_file, dimension, preprocess):
    screenshot = load_img(screen_file, target_size=dimension)
    screenshot = img_to_array(screenshot)
    screenshot = np.expand_dims(screenshot, axis=0)
    screenshot = preprocess(screenshot)
    screenshot = screenshot[0]
    return screenshot

create_training_data(dimension=(299, 299))
