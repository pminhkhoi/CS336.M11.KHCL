import numpy as np
import torch
from torch.autograd import Variable
import matplotlib.pyplot as plt

def feature_extract(model, dataloader):
    features = torch.FloatTensor()
    path_list = []
    for img, path in dataloader:
        img = img.cuda()
        input = Variable(img)
        output = model(input)
        feature = output.data.cpu()
        feature_norm = torch.norm(feature, p=2, dim=1, keepdim=True)
        feature = feature.div(feature_norm.expand_as(feature))
        features = torch.cat((features, feature), 0)
        path_list += list(path)
    return features, path_list


def feature_extract_crop(img, model):
    img = img.cuda()
    img = img.unsqueeze(0)
    input = Variable(img)
    output = model(input)
    feature = output.data.cpu()
    feature_norm = torch.norm(feature, p=2, dim=1, keepdim=True)
    feature = feature.div(feature_norm.expand_as(feature))
    return feature