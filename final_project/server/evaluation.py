import numpy as np
import os
from scipy import spatial
import matplotlib.pyplot as plt
import pandas as pd

def compute_score(query_feature, collection_feature):
    score = [spatial.distance.cosine(query_feature, feature) for feature in collection_feature]
    idx = np.argsort(score, axis=0)
    score = sorted(score)
    return score, idx

def calculate_AP_mAP_at_k(sorted_path_list, k, label_dir = "./image_annotation/", index = np.arange(0, 55)):
    query = []
    for file in os.listdir(label_dir):
        if file.split('.')[0].split('_')[-1] == "query":
            query.append(file.split('.')[0])
    labels = []
    for i in index:
        temp = []
        for file in os.listdir(label_dir):
            if file.split('.')[0] == query[i].replace("query", "good"):
                temp.append(file)
            elif file.split('.')[0] == query[i].replace("query", "junk"):
                temp.append(file)
            elif file.split('.')[0] == query[i].replace("query", "ok"):
                temp.append(file)
            if len(temp) == 3:
                labels.append(temp)
                break
    labels_content = []
    for q in labels:
        tmp = []
        for file in q:
            f = open(label_dir+file, 'r')
            content = f.read().split()
            tmp.extend(content)
            f.close()
        labels_content.append(tmp)
    ap = []
    for i in range(len(index)):
        precision = []
        relevant_doc = 0
        retrieved_doc = 0
        for path in sorted_path_list[index[i]][:k-1]:
            retrieved_doc += 1
            if path.split('/')[-1].split('.')[0] in labels_content[i]:
                relevant_doc += 1
                precision.append(relevant_doc/retrieved_doc)
        ap.append(np.mean(precision) if precision else 0)
    return ap, np.mean(ap)
            
def ploting_precision_recall( sorted_path_list, label_dir = "./image_annotation/", index = np.arange(0, 55)):
    query = []
    for file in os.listdir(label_dir):
        if file.split('.')[0].split('_')[-1] == "query":
            query.append(file.split('.')[0])
    labels = []
    for i in index:
        temp = []
        for file in os.listdir(label_dir):
            if file.split('.')[0] == query[i].replace("query", "good"):
                temp.append(file)
            elif file.split('.')[0] == query[i].replace("query", "junk"):
                temp.append(file)
            elif file.split('.')[0] == query[i].replace("query", "ok"):
                temp.append(file)
            if len(temp) == 3:
                labels.append(temp)
                break
    labels_content = []
    for q in labels:
        tmp = []
        for file in q:
            f = open(label_dir+file, 'r')
            content = f.read().split()
            tmp.extend(content)
            f.close()
        labels_content.append(tmp)
    for i in range(len(index)):
        precision = []
        recall = []
        relevant_doc = 0
        retrieved_doc = 0
        length = len(labels_content[i])
        for path in sorted_path_list[index[i]]:
            retrieved_doc += 1
            if path.split('/')[-1].split('.')[0] in labels_content[i]:
                relevant_doc += 1
                precision.append(relevant_doc/retrieved_doc)
                recall.append(relevant_doc/length)
            if relevant_doc == length:
                break
        plt.figure()
        plt.title(f"Precision-Recall curve of {query[i]}")
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.plot(recall, precision)
        #plt.savefig(f"image_retrieval/resnet101_plot/Precision_recall_curve_{query[i]}.jpg")
        plt.show()    
