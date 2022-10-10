#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from collections import Counter
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# In[6]:


# Path to the data directory
data_dir = Path("./captcha_images_v2/")


# In[15]:


# Get list of all the images
images = sorted(list(map(str, list(data_dir.glob("*.png")))))
images


# In[14]:


labels = [img.split(os.path.sep)[-1].split(".png")[0] for img in images]
labels


# In[22]:


characters = set(char for label in labels for char in label)
characters


# In[23]:


characters = sorted(list(characters))


# In[24]:


characters


# In[25]:


print("Number of images found: ", len(images))
print("Number of labels found: ", len(labels))
print("Number of unique characters: ", len(characters))
print("Characters present: ", characters)


# In[26]:


# Batch size for training and validation
batch_size = 16


# In[27]:


# Desired image dimensions
img_width = 200
img_height = 50


# In[28]:


# Factor by which the image is going to be downsampled
# by the convolutional blocks. We will be using two
# convolution blocks and each block will have
# a pooling layer which downsample the features by a factor of 2.
# Hence total downsampling factor would be 4.
downsample_factor = 4


# In[29]:


# Maximum length of any captcha in the dataset
max_length = max([len(label) for label in labels])


# In[30]:


print(max_length)


# Preprocessing

# In[31]:


# Mapping characters to integers
char_to_num = layers.StringLookup(
    vocabulary=list(characters), mask_token=None
)


# In[43]:


print(characters)
print(len(characters))


# In[34]:


print(tf.__version__)


# In[47]:


char_to_num.get_vocabulary()


# In[39]:


len(char_to_num.get_vocabulary())


# In[46]:


# Mapping integers back to original characters
num_to_char = layers.StringLookup(
    vocabulary=char_to_num.get_vocabulary(), mask_token=None, invert=True
)


# In[48]:


print(num_to_char)


# In[50]:


num_to_char.get_vocabulary()


# In[51]:


def split_data(images, labels, train_size=0.9, shuffle=True):
    # 1. Get the total size of the dataset
    size = len(images)
    # 2. Make an indices array and shuffle it, if required
    indices = np.arange(size)
    if shuffle:
        np.random.shuffle(indices)
    # 3. Get the size of training samples
    train_samples = int(size * train_size)
    # 4. Split data into training and validation sets
    x_train, y_train = images[indices[:train_samples]], labels[indices[:train_samples]]
    x_valid, y_valid = images[indices[train_samples:]], labels[indices[train_samples:]]
    return x_train, x_valid, y_train, y_valid


# In[58]:


# Splitting data into training and validation sets
x_train, x_valid, y_train, y_valid = split_data(np.array(images), np.array(labels))


# In[59]:


def encode_single_sample(img_path, label):
    # 1. Read image
    img = tf.io.read_file(img_path)
    # 2. Decode and convert to grayscale
    img = tf.io.decode_png(img, channels=1)
    # 3. Convert to float32 in [0, 1] range
    img = tf.image.convert_image_dtype(img, tf.float32)
    # 4. Resize to the desired size
    img = tf.image.resize(img, [img_height, img_width])
    # 5. Transpose the image because we want the time
    # dimension to correspond to the width of the image.
    img = tf.transpose(img, perm=[1, 0, 2])
    # 6. Map the characters in label to numbers
    label = char_to_num(tf.strings.unicode_split(label, input_encoding="UTF-8"))
    # 7. Return a dict as our model is expecting two inputs
    return {"image": img, "label": label}


# In[57]:


a


# In[ ]:




