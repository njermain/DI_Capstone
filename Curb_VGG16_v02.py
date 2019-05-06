# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 13:25:08 2019

Nate Jermain Gender Identification CNN
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('C:/Users/Nathaniel/Dropbox/DI Capstone/comp_cases_7.csv')
df9=pd.read_csv('C:/Users/Nathaniel/Dropbox/DI Capstone/comp_cases_9.csv')
df10=pd.read_csv('C:/Users/Nathaniel/Dropbox/DI Capstone/comp_cases_10.csv')
master = pd.concat([df,df9, df10], ignore_index=True)

master.head(5)
master.columns.values

# get strings to directory 
mypath = 'C:/Users/Nathaniel/Dropbox/DI Capstone/House_Images/'
master['img_path'] = [mypath + str(zpid)+'.jpg' for zpid in master['zpid']]
# calculate index for residuals
master['ind'] = master['Price'].replace({',':''},regex=True).apply(pd.to_numeric,1).sub(master['Zest'].replace({',':''},regex=True).apply(pd.to_numeric,1))

import os
os.chdir('C:/Users/Nathaniel/Dropbox/DI Capstone')
master.to_csv('master_dir.csv')

#some homes sold for way more than the zest
master['ind'].sort_values().head(10)
master['img'][333]
import scipy
master['zind'] = scipy.stats.zscore(master['ind'])

# some sold for way less 

plt.hist(master['ind'], 200)

sns.distplot(master['ind'], hist=True, kde=False, 
             bins=100, color = 'darkblue', 
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})

# convert index to binary string
master = pd.read_csv('master_dir.csv')
bin_label = []
for i in master['ind']:
    if i>0:
        bin_label.append(str(1))
    else:
        bin_label.append(str(0))
        
   
        
master['bin_label'] = bin_label

type(master['bin_label'][0])
master.to_csv('master_dir.csv')   

# split into training and test sets
from sklearn.model_selection import train_test_split
train_X, test_X, train_y, test_y = train_test_split(master['img_path'], master['bin_label'], random_state = 0, test_size=.2)

# join dataframes for flow.from.dataframe
type(train_y[2])
train_y = [str(x) for x in train_y]
test_y = [str(x) for x in test_y]
test_y[2]

train_df = pd.DataFrame(train_X)
train_df ['bin_label'] = train_y
train_df.columns.values

test_df = pd.DataFrame(test_X)
test_df ['bin_label'] = test_y
test_df.columns.values

######## Modeling ################################
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras import layers


vgg=VGG16(include_top=False, pooling='avg', weights='imagenet',input_shape=(250, 250, 3))
vgg.summary()

# Freeze the layers except the last 2 layers
for layer in vgg.layers[:-4]:
    layer.trainable = False

# Check the trainable status of the individual layers
for layer in vgg.layers:
    print(layer, layer.trainable)
    

# Create the model
model = Sequential()


# Add the vgg convolutional base model
model.add(vgg)
 
# Add new layers
model.add(layers.Dense(128, activation='relu'))
model.add(layers.BatchNormalization())
model.add(layers.Dense(2, activation='softmax'))

model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

### Data flow and fitting #######

from tensorflow.python.keras.applications.vgg16 import preprocess_input
from tensorflow.python.keras.preprocessing.image import ImageDataGenerator



data_generator = ImageDataGenerator(preprocessing_function=preprocess_input)

train_generator = data_generator.flow_from_dataframe(
        train_df, x_col = 'img_path', y_col = 'bin_label',
        target_size=(250, 250),
        batch_size=12,
        class_mode='categorical')



valid_generator = data_generator.flow_from_dataframe(
        test_df, x_col = 'img_path', y_col = 'bin_label',
        target_size=(250, 250),
        batch_size=12,
        class_mode='categorical')


history = model.fit_generator(
        train_generator,
        epochs=10,
        steps_per_epoch=66,
        validation_data=valid_generator,
        validation_steps=16)

# plot training and validation accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()







