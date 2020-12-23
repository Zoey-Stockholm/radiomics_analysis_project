#!/usr/bin/env python
# coding: utf-8


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


def getMask(img_path):
    """
    # This function generate a mask of the given image based on the segmentation outlined in green color.
    Args:
         img_path(str): image file path
    Return:
         1.the mask in which segmentated area is filled with label 255 (Note: exclude the outline), TRUE = successfully get mask
         2.black image, False = failed to get mask  
    
    """
    imgCV = cv2.imread(img_path)
    img = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGB)

    # the outline is True ;other is False
    mask = (img[:, :, 0] != img[:, :, 1]) & (img[:, :, 0] < 240)
    bound_image = np.where(mask, 255, 0).astype(np.uint8)
    bound = bound_image.copy()
    contours, hierarchy = cv2.findContours(bound_image, cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    # if a tumor exists
    if len(contours) > 0:
        for contour in contours:
            mask_with_bound = cv2.fillPoly(bound_image, [contour], 255)
        # remove the outline part
        mask_without_bound = mask_with_bound - bound
        return mask_without_bound, True
    else:
        return bound, False


def generateMasks(data_path,mask_path):
    """
    This function generates masks for all T2M images in Data dir.
    args: 
        data_path(str):dir path of original segmented images
        mask_path: give a path where the masks would be
    Yield:
        masks of all T2 images in data_path
    Return:
        is_seg_pat(list): list of patients whose masks are successfully generated
    """


    patients_path = os.listdir(data_path)
    
    is_seg_pat = []


    for pat in patients_path:
        # Create direcctory path = "Mask/Pat_n/masks"
        path = os.path.join(mask_path,pat,'masks')
        if not os.path.exists(path):
            # os.makedirs()
            os.makedirs(path)
        # Create masks of 'Data/Pat?/Pat?T2M'
        pat_data_path = os.path.join(data_path,pat,pat+'T2M')
        # Delete Thumbs.db
        if os.path.exists(os.path.join(pat_data_path,'Thumbs.db')):
            os.remove(os.path.join(pat_data_path,'Thumbs.db'))
        # For images in 'Data/Pat?/Pat?T2M',create masks

        # check if masks has been created
        if not os.listdir(path):
            for img in os.listdir(pat_data_path):
                img_path = os.path.join(pat_data_path,img)
                mask,is_seg = getMask(img_path)
                cv2.imwrite(os.path.join(path,img),mask)
                if is_seg and (pat not in is_seg_pat):
                    is_seg_pat.append(pat)
    return is_seg_pat

            
            
        


data_path = '/Volumes/Samsung_T5/cleanedData/Data/'
mask_path = '/Volumes/Samsung_T5/cleanedData/Mask/'





