import os
from torch.utils.data import DataLoader
from torch.utils.data.dataset import Dataset
from PIL import Image
import torchvision.transforms as transforms
import cv2
class Collection(Dataset):
    def __init__(self, image_path, transform=None):
        super().__init__()
        self.image_path = image_path
        self.transform = transform
    def __getitem__(self, index):
        image_path = self.image_path[index]
        image = Image.open(image_path).convert('RGB')
        if self.transform is not None:
            image = self.transform(image)
        return image, image_path
    def __len__(self):
        return len(self.image_path)

def get_file_list(file_path = "./image_data/"):
    import random
    file_list = []
    assert os.path.isdir(file_path)
    for file in os.listdir(file_path):
        file_list.append(file_path+file)
    return file_list

def load_data(data_path, batch_size = 4, shuffle=False, transform='default'):
    default_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.225, 0.225, 0.225))
    ]) if transform == 'default' else transform

    image_path_list = get_file_list(file_path=data_path)
    
    collection = Collection(image_path=image_path_list, transform = default_transform)

    dataloader = DataLoader(dataset=collection, batch_size=batch_size, shuffle=shuffle, num_workers=0)
    return dataloader

def load_query(img_path, batch_size = 1, shuffle=False, transform='default'):
    default_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.225, 0.225, 0.225))
    ]) if transform == 'default' else transform
    
    collection = Collection(image_path=[img_path], transform = default_transform)

    dataloader = DataLoader(dataset=collection, batch_size=batch_size, shuffle=shuffle, num_workers=0)
    return dataloader


def img_crop(img_info):
    path, x, y, w, h = img_info

    print(path, x, y, w, h)

    img = Image.open(path).convert('RGB')
    crop_img = img.crop((x, y, x+w, y+h))

    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.225, 0.225, 0.225))
    ])
    img = transform(crop_img)

    
    return img