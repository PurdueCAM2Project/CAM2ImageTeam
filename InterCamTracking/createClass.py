import cv2
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
import matplotlib.pyplot as plt

'''
create this class if object is car

class boundingbox

variables:
imagename
xmin
xmax
ymin
ymax
hash value -- to be added later --- Decided to not make it a class variable and
defined a separate method for this
'''

img = cv2.imread("NYCImages/144319_2017-07-06_17-22-45-520384.jpg")
#print(img[195][183])
#print(type(img))
#print(img.size)

class boundingBox(object):


    def __init__(self, imagename, xmin, ymin, xmax, ymax):
        self.imagename = imagename
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax


'''
Creates a car object if object in file is of type car.
Car class is 7
Creates car object is probability of object being car is higher than 10%
'''

def createClass(fileName):
    car = boundingBox("car", 1, 3 , 5 , 7)
    my_cars = []


    with open(fileName, "r") as f:
        for line in f:
            data = line
            data = data.split(" ")


            if(data[1] == str(7)):
                if(float(data[2]) > 0.1):
                    name = data[0].split("/")
                    my_cars.append(boundingBox(name[4] + '/' + name[5], int(data[3]), int(data[4]), int(data[5]), int(data[6])))



    #print(len((my_cars)))
    return my_cars

'''
Generates a hash function for all car objects
so that the given values could then be used for k-means clustering or other
methods for analysis.
In the curent version of the hash function, I have multiplied the red color by 1,
green by 2 and blue by 3. Or it might be the other way around. That doesn't really matter
'''



def hash_generator(my_images):

    hash_array = []

    for counter in my_images:
        img = cv2.imread(counter.imagename)
        j = counter.xmin
        i = counter.ymin
        x = 0
        #print(img.shape[1])
        #print(counter.imagename)
        #print(j)
        #print(i)
        while(i < counter.ymax and i < img.shape[0]):
            while(j < counter.xmax and j < img.shape[1]):
                x = x + img[i][j][0] * 5323 + img[i][j][1] * 1483 + img[i][j][2] * 7919
                #hash_array.append(img[i][j][0] * 1 + img[i][j][1] * 2 + img[i][j][2] * 3)
                j += 1
            i += 1
        #print(j)
        #print(i)
        #print(counter.imagename)
        hash_array.append(x)

    return hash_array

def hash_generator(my_images):

    hash_array = []
    counter1 = 0
    counter2 = 0

    while(counter1 < len(my_images)):
        counter2 = counter1 + 1
        img1 = cv2.imread(my_images[counter1].imagename)
        while(counter2 < len(my_images)):

            img2 = cv2.imread(my_images[counter2].imagename)

            '''
            j = counter.xmin
            i = counter.ymin
            x = 0

            while(i < counter1.ymax and i < img.shape[0]):
                while(j < counter.xmax and j < img.shape[1]):
                    x = x + img[i][j][0] * 5323 + img[i][j][1] * 1483 + img[i][j][2] * 7919
                    #hash_array.append(img[i][j][0] * 1 + img[i][j][1] * 2 + img[i][j][2] * 3)
                    j += 1
                i += 1
            '''



            counter2 += 1
        counter1 += 1
'''
    for counter in my_images:
        img = cv2.imread(counter.imagename)
        j = counter.xmin
        i = counter.ymin
        x = 0

        while(i < counter.ymax and i < img.shape[0]):
            while(j < counter.xmax and j < img.shape[1]):
                x = x + img[i][j][0] * 5323 + img[i][j][1] * 1483 + img[i][j][2] * 7919
                #hash_array.append(img[i][j][0] * 1 + img[i][j][1] * 2 + img[i][j][2] * 3)
                j += 1
            i += 1
        #print(j)
        #print(i)
        #print(counter.imagename)
        hash_array.append(x)

    return hash_array
'''
def hash_array_to_dict(my_hashed_array):

    count = 0
    my_hashed_dict = {}
    while(count < len(my_hashed_array)):
        my_hashed_dict[my_hashed_array[count]] = count
        #print(my_hashed_array[count])
        count += 1

    return my_hashed_dict

if __name__ == '__main__':
    #main()
    my_list = createClass("labels.txt")
    print(len(my_list))


    my_hash_array = hash_generator(my_list)
    print(len(my_hash_array))
    my_hash_dict = hash_array_to_dict(my_hash_array)
    print(len(my_hash_dict))


    X = np.array(list(zip(my_hash_array,np.zeros(len(my_hash_array)))), dtype=np.int)
    bandwidth = estimate_bandwidth(X, quantile=0.02)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_
    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    for k in range(n_clusters_):
        my_members = labels == k
        #print(X[my_members, 0])
        print("cluster {0} : {1}".format(k, X[my_members, 0]))
'''
TODO

1) Make a dictionary using list value as index. WON'T WORK. Cuz lack of uniqueness
2) Make as many lists of integer (maybe a list of lists) as the number of clusters
3) Iterate through all the hash-values in a given cluster, extract the dictionary index
using the hash-value and cluster all those indices together.

Thus, clustering task is completed. All that is left to now compare objects in these given
clusters against other objects in the same cluster O(n^2).

^^ This approach did not work. The roadblocks encountered were firstly that finding indices 
after the actual MeanShift task was completed was not possible. Secondly, in direct image
to image comparison, the main problem seems to be the differing sizes of images. That, combined
with the actual difficulty in identifying similarities using direct pixel by pixel comparison makes
it a bad approach.

'''
