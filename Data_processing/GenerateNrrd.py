#!/usr/bin/env python
# coding: utf-8

import os
from skimage.io import ImageCollection
import nrrd
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd


def convert_to_gray(f, **args):
        image = cv.imread(f)
        image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        return image


T2_info = pd.read_excel('output_T2_info.xlsx',sheet_name = 'final_outcome')
T2_info.head()


def get_image_info(patient_id):
    r = T2_info.loc[T2_info['id']==patient_id,'pixel_spacing_0':'slice_thickness']
    if len(r.index)>0:
        r =  r.values.tolist()[0]
        spacings = r[0:3]
        thickness = r[3]
        return spacings,thickness
    return None
    



def generate_nrrd(file):
    """
    ## This function is for generating NRRD for patient T2M images.
    Args:
        filer(str):Orginal or Mask images folder path. The files are saved in format: Data/Patn/PatnT2M/images or masks

    Yields:
        nrrd of all patinets T2M saved in another folder named "{file}_nrrd"
    
    """
    for root, dirs, files in os.walk(file):
        path = root.split(file)
        if path[1] != "":
            patient_id = int(path[1].split('/')[1][3:])
            path = file + "_nrrd" + path[1]
            #             if path.find("frisk")==-1 & path.find("M+")==-1 & path.find('T2M')==-1:
            if (path.find('T2M') != -1 & path.find('frisk') ==
                    -1 & path.find('+') == -1
                ) or path.find('masks') != -1:  # Only T2M or mask can be found
                os.makedirs(path, exist_ok=True)
                print(path)
                Nrrd = ImageCollection(os.path.join(root, "*.tiff"),
                                       plugin='tifffile',
                                       load_func=convert_to_gray)
                Nrrd = np.asarray(Nrrd)

                if get_image_info(patient_id):
                    print(patient_id)
                    (spacings, thickness) = get_image_info(patient_id)
                    thicknesses = [float('nan'), float('nan'), thickness]
                    spacing_direction = np.eye(3)
                    # Note: All header fields are specified in Fortran order,
                    # per the NRRD specification, regardless of the index order. For example,
                    # a C-ordered array with shape (60, 800, 600) would have a sizes field of (600, 800, 60).
                    if len(Nrrd) > 0:
                        header = {
                            'spacings': spacings,
                            'thicknesses': thicknesses
                            
                        }
                        nrrd.write(os.path.join(path,
                                                str(patient_id) + '.nrrd'),
                                   Nrrd,
                                   header,
                                   index_order='C')


generate_nrrd('/Volumes/Samsung_T5/cleanedData/Data')






















