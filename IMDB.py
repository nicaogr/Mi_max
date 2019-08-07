#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 14:54:36 2019

@author: gonthier
"""

import pandas as pd
import os
from urllib.request import urlretrieve
from zipfile import ZipFile
from tqdm import tqdm

def download_url(url, destination=None, progress_bar=True):
	def my_hook(t):
		last_b = [0]

		def inner(b=1, bsize=1, tsize=None):
			if tsize is not None:
				t.total = tsize
			if b > 0:
				t.update((b - last_b[0]) * bsize)
			last_b[0] = b

		return inner

	if progress_bar:
		with tqdm(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
			filename, _ = urlretrieve(url, filename=destination, reporthook=my_hook(t))
	else:
		filename, _ = urlretrieve(url, filename=destination)

def get_database(database,default_path_imdb = 'data'):

    if database=='watercolor':
        ext = '.csv'
        item_name = 'name_img'
        path_tmp = os.path.join(default_path_imdb,'watercolor')
        path_to_img = os.path.join(path_tmp,'JPEGImages')
        classes =  ["bicycle", "bird","car", "cat", "dog", "person"]
        url_dataset = 'http://www.hal.t.u-tokyo.ac.jp/~inoue/projects/cross_domain_detection/datasets/watercolor.zip'
        url_file = 'https://wsoda.telecom-paristech.fr/downloads/dataset/watercolor.csv'
    elif database=='PeopleArt':
        ext = '.csv'
        item_name = 'name_img'
        path_tmp = os.path.join(default_path_imdb,'PeopleArt')
        path_to_img =os.path.join(path_tmp,'JPEGImages')
        classes =  ["person"]
        url_dataset = 'https://codeload.github.com/BathVisArtData/PeopleArt/zip/master'
        url_file = 'https://wsoda.telecom-paristech.fr/downloads/dataset/PeopleArt.csv'
    elif 'IconArt_v1' in database:
        ext='.csv'
        item_name='item'
        classes =  ['angel','Child_Jesus', 'crucifixion_of_Jesus',
        'Mary','nudity', 'ruins','Saint_Sebastien']
        path_tmp = os.path.join(default_path_imdb,'IconArt_v1')
        path_to_img =os.path.join(path_tmp,'JPEGImages')
        url_dataset = 'https://wsoda.telecom-paristech.fr/downloads/dataset/IconArt_v1.zip'
    elif database=='clipart':
        raise(NotImplementedError)
        ext = '.csv'
        item_name = 'name_img'
        path_tmp = os.path.join(default_path_imdb,'clipart')
        path_to_img = os.path.join(path_tmp,'JPEGImages')
        classes =  ['aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor']
        url_dataset = 'http://www.hal.t.u-tokyo.ac.jp/~inoue/projects/cross_domain_detection/datasets/clipart.zip'
    else:
        print('This database don t exist :',database)
        raise NotImplementedError
    num_classes = len(classes)
    
    path_data_csvfile = os.path.join(path_tmp,'ImageSets','Main')
    databasetxt = path_data_csvfile + database + ext
    
    if not(os.path.exists(path_to_img)):
        tmp_zip = 'sampleDir.zip'
        print('Downloading: "{}" to {}\n'.format(url_dataset, tmp_zip))
        download_url(url_dataset, tmp_zip)
        with ZipFile(tmp_zip, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall(default_path_imdb)
        os.remove(tmp_zip)
        if database in ['PeopleArt','watercolor']:
            # We also need to download the image level annotations file at the right format
            download_url(url_file, databasetxt)
    
    databasetxt = os.path.join(path_data_csvfile,database + ext)

    if 'IconArt_v1' in database or 'IconArt_v1'==database or database=='RMN':
        dtypes = {0:str,'item':str,'angel':int,\
                      'Child_Jesus':int,'crucifixion_of_Jesus':int,'Mary':int,'nudity':int,\
                      'ruins':int,'Saint_Sebastien':int,\
                      'set':str,'Anno':int}
    else:
        dtypes = {}
        dtypes[item_name] =  str
        for c in classes:
            dtypes[c] = int
    df_label = pd.read_csv(databasetxt,sep=",",dtype=dtypes)
    str_val = 'val'
    if database in ['watercolor','clipart','PeopleArt']:
        str_val = 'val'
        df_label[classes] = df_label[classes].apply(lambda x:(x + 1.0)/2.0)
    
    return(item_name,path_to_img,classes,ext,num_classes,str_val,df_label)