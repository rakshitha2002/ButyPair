from sklearn.cluster import KMeans
from collections import Counter
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def showImage(image):
    plt.axis("off")
    plt.imshow(image)
    plt.show()

def loadImage(image_path):
    print("Loading images....")
    img = cv.imread(image_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    dim = (500, 300)
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    print("Image Loading Completed :-)")
    return img

def trainKMeanClusterWithImage(image_obj):
    k_mean_cluster = KMeans(n_clusters=6)
    k_mean_cluster.fit(image_obj.reshape(-1, 3))

    print("Traning KMean Cluster....")
    labels = k_mean_cluster.labels_
    centers = k_mean_cluster.cluster_centers_
    print("KMean cluster training Completed :-)")
    return labels, centers

def pepareProportionofLables(labels):
    print("Peparing Proportion....")
    n_pixels = len(labels)
    counter = Counter(labels)  # count how many pixels per cluster
    proportion = {}
    for i in counter:
        proportion[i] = np.round(counter[i] / n_pixels, 2)
    proportion = dict(sorted(proportion.items()))
    print("Proportion Peparetion Completed :-)")
    return proportion

def prepareDominanteColor(centers, proportion):
    print("Sorting Domination Color....")
    dominating_color_list = [[center, proportion[idx]]
                            for idx, center in enumerate(centers)]
    dominating_color_list.sort(key=lambda x: x[1], reverse=True)
    print("Domination Color Sorting Completed :-)")
    return dominating_color_list

def convertTORGBList(colors):
    print("Converting to RGB List....")
    rgb_list = []
    for i in colors:
        r, g, b = i[0]
        rgb_list.append((int(r), int(g), int(b)))
    print("Converting to RGB List Completed :-)")
    return rgb_list

def maxColorInImage(image_path):
    loaded_img = loadImage(image_path)
    labels, centers = trainKMeanClusterWithImage(loaded_img)
    proportion_of_lables = pepareProportionofLables(labels)
    colors = prepareDominanteColor(centers, proportion_of_lables)
    rgb_colors = convertTORGBList(colors)
    return rgb_colors


# print(maxColorInImage("/static/images/image_5667d234-4ff4-4d80-8557-c175e5796648.jpg"))
'''
# def showImage(image):
#     plt.axis("off")
#     plt.imshow(image)
#     plt.show()


# starting time
start = time.time()

print("Loading images....")
img = cv.imread(r"E:\PROJECT\PythonFlask\butypair\application\static\images\image_d9bfae58-5ce2-460d-93e0-d0908cae426b.jpg")
# showImage(img)
img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# showImage(img)
dim = (500, 300)
img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
# showImage(img)
print("Image Loading Completed :-)")

k_mean_cluster = KMeans(n_clusters=4)
k_mean_cluster.fit(img.reshape(-1, 3))

print("Traning KMean Cluster....")
labels = k_mean_cluster.labels_
centers = k_mean_cluster.cluster_centers_
print("KMean cluster training Completed :-)")


print("Peparing Proportion....")
n_pixels = len(labels)
counter = Counter(labels)  # count how many pixels per cluster
perc = {}
for i in counter:
    perc[i] = np.round(counter[i] / n_pixels, 2)
perc = dict(sorted(perc.items()))
print("Proportion Peparetion Completed :-)")

print("Sorting Domination Color....")
dominating_color_list = [[center, perc[idx]]
                         for idx, center in enumerate(centers)]
dominating_color_list.sort(key=lambda x: x[1], reverse=True)
print("Domination Color Sorting Completed :-)")

for i in dominating_color_list:
    r, g, b = i[0]
    print(f"rgb({int(r)}, {int(g)}, {int(b)})")

# end time
end = time.time()

# total time taken
print(f"Runtime of the program is {end - start}")

# showImage(
#     [
#         [(int(i[0][0]), int(i[0][1]), int(i[0][2]),)]  # red  # green  # blue
#         for i in dominating_color_list
#     ]
# )
'''