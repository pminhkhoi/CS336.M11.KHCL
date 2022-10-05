import os
import cv2

def create_query_folder(path = "./image_annotation/"):
    query_list = []
    file_name = []
    for query in os.listdir(path):
        if query.split('.')[0].split('_')[-1] == "query":
            file_name.append(query.split('.')[0] + '.jpg')
            file = open(path+query, 'r')
            content = file.readline().split()
            crop_img, x, y, w, h = content
            file.close()
            crop_img = crop_img.split('_')[1::]
            crop_img = '_'.join(crop_img)
            query_list.append((crop_img + '.jpg', x, y, w, h))
    query_dir = "./image_data/"
    query_des = "./image_query/"
    for item in range(len(query_list)):
        img = cv2.imread(query_dir+query_list[item][0])
        x, y, w, h = float(query_list[item][1]), float(query_list[item][2]), float(query_list[item][3]), float(query_list[item][4])
        img = img[int(x):int(x+w), int(y):int(y+h)]
        cv2.imwrite(query_des+file_name[item], img)

if __name__ == "__main__":
    create_query_folder()