import torchvision.models as models
import torch.nn as nn

def load_model_vgg16():
    model = models.vgg16(pretrained=True)
    model.classifier = model.classifier[:-1]
    model = model.eval()
    model = model.cuda()
    return model

def load_model_resnet():
    model = models.resnet101(pretrained=True)
    modules = list(model.children())[:-1]
    model = nn.Sequential(*modules)
    model = model.cuda()
    mdoel = model.eval()
    return model