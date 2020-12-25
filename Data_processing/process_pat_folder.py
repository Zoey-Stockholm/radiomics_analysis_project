#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
import shutil


pat_file = pd.read_excel('output_T2_info.xlsx',sheet_name='final_outcome')

id_list = list(pat_file['id'])


images_path = '/Volumes/Samsung_T5/cleanedData/cleanedData'

for dir in os.listdir(images_path):
    id = int(dir[3:])
    if id not in id_list:
        pat = os.path.join(images_path,dir)
        shutil.rmtree(pat)  # delete nonempty dirs but not listed in DICOM files




