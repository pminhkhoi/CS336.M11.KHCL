import pickle
import model
import dataset
from feature_extract import feature_extract, feature_extract_crop
import evaluation


def retrieval(img_path, crop):
    collection_feature = None
    collection_path = None
    
    m = model.load_model_vgg16()
    dataloader = dataset.load_query(img_path)
    query_feature, query_path = feature_extract(m, dataloader)
 
    with open('./vgg16_extractor_result/collection_features.pkl', 'rb') as pickle_file:
        collection_feature = pickle.load(pickle_file)
    
    with open('./vgg16_extractor_result/collection_paths.txt', 'rb') as pickle_file:
        collection_path = pickle.load(pickle_file)
    # collection_feature, collection_path = pickle.load('vgg16_extractor_result/collection_features.pkl'), pickle.load('vgg16_extractor_result/collection_paths.txt')
    similarity, index = evaluation.compute_score(query_feature, collection_feature)
    sorted_paths = [collection_path[i] for i in index]
    return sorted_paths, similarity


def retrieval_crop(img_info):
    collection_feature = None
    collection_path = None

    m = model.load_model_vgg16()

    query = dataset.img_crop(img_info)
    query_feature = feature_extract_crop(query, m)
    with open('./vgg16_extractor_result/collection_features.pkl', 'rb') as pickle_file:
        collection_feature = pickle.load(pickle_file)
    
    with open('./vgg16_extractor_result/collection_paths.txt', 'rb') as pickle_file:
        collection_path = pickle.load(pickle_file)
    similarity, index = evaluation.compute_score(query_feature, collection_feature)
    sorted_paths = [collection_path[i] for i in index]
    return sorted_paths, similarity

