import json
from nltk_utils import tokenize , stem , bag_of_words
import numpy as np
import torch 
import torch.nn as nn
from torch.utils.data import Dataset , DataLoader

from model import NeuralNet

with open('intents.json' ,'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

for intent in intents['intents'] :
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w,tag))


ignore_words = ['?' , '!' , '.' , ',' , '@' ]
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))



x_train = []
y_train = []

for patter , tag in xy:
    bag = bag_of_words(patter , all_words)
    x_train.append(bag)
    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(x_train)
y_train = np.array(y_train)




class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    
    def __len__(self):
        return self.n_samples



#hyperparameters
batch_size = 8
input_size = len(x_train[0])
hidden_size = 8
output_size = len(tags)
learning_rate = 0.001
num_epochs = 256


print(input_size , len(all_words))
print(output_size , tags)

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset , batch_size=batch_size , shuffle=True , num_workers=2)


device = torch.device()
model = NeuralNet(input_size , hidden_size , output_size )