# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 16:20:56 2017

@author: aparn
"""

import string
import sys

class AnnotationYOLO:
        
    def read_datafile(file_name):
		"""
		description: accepts a file, reads it and splits and extracts the first number in each line, which corresponds to the class label
		"""
        f = open(file_name, "r")
        extracted_list = []
        
        for line in f:
            extracted_list.append(line.split(' ')[0])
            
        return extracted_list
    
    def create_detected_class_list(annotation_file):
		"""
		description: parses the YOLO annotation_file and makes a list of the returned class labels 
		"""
        detected_class_list = []
        detected_class_list = read_datafile(annotation_file)
        
        return detected_class_list
        
    def create_dict_for_class_index(list_of_classes_file):
        """
        description: this function assigns a key to every class, creates
        a dictionary that gives an index for the class and its encoding in YOLO.
        param arg1: list_of_classes_file is a list of classes
        (like human, car etc)
        return: returns a dictionary with the key value pair
        """
        list_of_classes = []
        label_index = dict()
        
        list_of_classes = read_datafile(list_of_classes_file)
    
        #create a dictionary with all the classes and label pairs    
        for i in range(len(list_of_classes)):
            label_index[str(i+1)] = list_of_classes[i].strip()
            
        return label_index
            
    def count_objects(label_index, detected_class_list):
        """
        description: this func accepts YOLO's output and the index for objects 
        and their labels, counts and returns the frequency of occurance of each
        object type as a dictionary object.
        param arg1: label_index is the dictionary that has class labels and their
        corresponding object names
        param arg2: detected_class_list has class labels that YOLO outputs, 
        for all objects that it detects
        return: detected_object_count_dict is a dictionary where the key is 
        object type and value is the number of such objects that have been 
        observed in a particular image
        """
        detected_object_count_dict = dict()
    
        for key in label_index:
            num_of_type_i_objects = detected_class_list.count(str(key))
            detected_object_count_dict[label_index.get(key)] = num_of_type_i_objects                
        return detected_object_count_dict
    
    def counting_module(annotation_file, list_of_classes_file):
		"""
		description: This function is the one that needs to be called from our program
		"""
        detected_object_count_dict = dict()
        
        detected_class_list = create_detected_class_list(annotation_file)
        label_index = create_dict_for_class_index(list_of_classes_file)
        detected_object_count_dict = count_objects(label_index, detected_class_list)
        
        return detected_object_count_dict
        
    def something():
		"""
		function to test the rest of the program; reads from the command line
		"""
        annotation_file = sys.argv[1]
        list_of_classes_file = sys.argv[2]
        
        count_obj_dict = counting_module(annotation_file, list_of_classes_file)
        print(count_obj_dict )
        