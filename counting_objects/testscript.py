# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 17:17:53 2017
@author: Aparna Pidaparthi

"""

from Annotation_script import AnnotationYOLO
import sys
import string

def main():
    annotation_file = sys.argv[1]
    list_of_classes_file = sys.argv[2]

    count_obj_dict = counting_module(annotation_file, list_of_classes_file)
    print(count_obj_dict)
    
main()