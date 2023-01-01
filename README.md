# AI_PhotoApp_with_Tensorflow
*A.I. Photo App with Tensorflow and More*

# Run app:
- server (built with Flask): run ./server/_\_init__.py
- frontend (built with React): run __npm start__ under ./react-front-end

## Features
The Photo app supports:
- Image categorization with neural nets
- Object detection and search by keyword
- Smart Albums (automatically assign photos to album)
  - Albums include: Nature, Urban, Portrait, Pet, Interior, Night
- upload image and save to backend
    
## Image Categorization & Object Detection
*all models saved as .h5 files in ./Detectors/models*

#### Models

- sky-recognition: categorize between [day_time_sky, sunset, other]
- night-recognition: categorize between [night, day]
- building-recognition: categorize between [buildings, other]
- forest-recognition: categorize between [forest, other]
- mountain-recognition: categorize between [mountain, other]


### Built & Trained Convolutional Neural Nets

-- models includes: forest, sky, mountain, night recognition --

- build with Tensorflow.keras.layers
- General architecture: (varies for different models)
  - conv layer: (64 node to 256 node) x2 ~ x4
  - L2 regularization
  - batch normalization (for some)
  - linear activation relu
  - max pooling layer
  - Global pooling / flatten
  - fully connected layers x1 ~ x3
  - dropout (for some)
- trained on small dataset of 500 to 1000 images per model
- data argumentation for training (ex. random horizontal flip, random crop / shift ..)

### Transfer Learning

-- model includes: Building recondition --

- using pre-trained model MobileNetV2 from Keras
- added fully connected layers

### Pre-trained Model

-- for Object Detection --

- Tensorflow Model Zoo Mask RNN model
- trained on COCO categories

## Backend & Image Processing

- server built with flask: ./server
- api build with Flask.Blueprint: ./server/views.py
- image processing: ./server/image_filter.py
- synonym enabled image search with nltk.corpus WordNet: ./server/vocab_dictionary.py
- auto assigned albums: ./server/albums.py

## React Frontend

- styled with Bootstrap & react-bootstrap
- Navigation enabled with react-router-dom

### UI demo

Upload Immge:
![upload img](./demo%20photos/upload_image_with_images_list.png)

Homepage:
![homepage img](./demo%20photos/homepage.png)

Select & Delete Photo(s)
![select img](./demo%20photos/home_select.png)

Search Image by Keyword
![search img](./demo%20photos/word_search.png)

Albums:
![albums img](./demo%20photos/albums.png)

Example, Album: Urban
![urban album img](./demo%20photos/urban_album.png)

Example, Album: Nature
![nature album img](./demo%20photos/nature_album.png)

Search Image in a Album
![album search](./demo%20photos/nature_search_cars.png)


