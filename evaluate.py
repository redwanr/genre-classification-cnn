from keras.models import load_model
import numpy as np
import os

import measures

# evaluate a given model on test data
# model_path: path to keras model
def evaluate(model_path=os.path.join('/home/ubuntu/checkpoints', 'xception05-0.236.mod')):

    # load test data
    test_X = np.load(os.path.join('/home/ubuntu/training_data', 'test_X.npy'))
    test_Y = np.load(os.path.join('/home/ubuntu/training_data', 'test_Y.npy'))

    # load model
    model = model = load_model(model_path)
    
    # get predictions
    test_predictions = model.predict(test_X, batch_size=16)

    # get measures
    test_measures = measures.get_measures(test_predictions, test_Y, .5)
       
    # read genres
    genre_file_path = os.path.join('/home/ubuntu/training_data', 'genres.txt')
    with open(genre_file_path, 'r') as handler:
        genres = handler.readlines()
    genres = [genre[:-1] for genre in genres]
    
    # print measures 
    print("Statistics on test data:")
    measures.print_measures(test_measures, genres)    

evaluate()
