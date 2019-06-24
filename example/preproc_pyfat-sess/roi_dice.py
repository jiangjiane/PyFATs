# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import nibabel as nib
import numpy as np

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

rois_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/standard/'
terminal_rois_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/results/'
results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/results/'

l_rois = ['l_MNI152_cytoMPM_thr25_1mm_hOc1.nii.gz', 'l_MNI152_cytoMPM_thr25_1mm_hOc2.nii.gz',
          'l_MNI152_cytoMPM_thr25_1mm_hOc3d.nii.gz', 'l_MNI152_cytoMPM_thr25_1mm_hOc3v.nii.gz']

l_terminal_rois = ['l_vis1_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'l_vis2_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'l_vis3_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'l_vis4_terminalpoint_posterior_vol_merge_prob24.nii.gz']

r_rois = ['r_MNI152_cytoMPM_thr25_1mm_hOc1.nii.gz', 'r_MNI152_cytoMPM_thr25_1mm_hOc2.nii.gz',
          'r_MNI152_cytoMPM_thr25_1mm_hOc3d.nii.gz', 'r_MNI152_cytoMPM_thr25_1mm_hOc3v.nii.gz']

r_terminal_rois = ['r_vis1_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'r_vis2_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'r_vis3_terminalpoint_posterior_vol_merge_prob24.nii.gz',
                   'r_vis4_terminalpoint_posterior_vol_merge_prob24.nii.gz']


def _overlap(c1, c2, index='dice'):
    """
    Calculate overlap between two collections
    Parameters
    ----------
    c1, c2 : collection (list | tuple | set | 1-D array etc.)
    index : string ('dice' | 'percent')
        This parameter is used to specify index which is used to measure overlap.
    Return
    ------
    overlap : float
        The overlap between c1 and c2
    """
    set1 = set(c1)
    set2 = set(c2)
    intersection_num = float(len(set1 & set2))
    try:
        if index == 'dice':
            total_num = len(set1 | set2) + intersection_num
            overlap = 2.0 * intersection_num / total_num
        elif index == 'percent':
            overlap = 1.0 * intersection_num / len(set2)
        else:
            raise Exception("Only support 'dice' and 'percent' as overlap indices at present.")
    except ZeroDivisionError as e:
        overlap = np.nan

    return overlap

l_result = []
for i in range(len(l_rois)):
    data1 = nib.load(os.path.join(rois_dir, l_rois[i])).get_data()
    pos1 = np.where(data1 > 0)
    data1_1 = zip(*pos1)
    roi_result = []
    for j in range(len(l_terminal_rois)):
        data2 = nib.load(os.path.join(terminal_rois_dir, l_terminal_rois[j])).get_data()
        pos2 = np.where(data2 > 0)
        data2_2 = zip(*pos2)
        roi_result.append(_overlap(data1_1, data2_2, 'percent'))
    l_result.append(roi_result)

print l_result

r_result = []
for m in range(len(r_rois)):
    data1 = nib.load(os.path.join(rois_dir, r_rois[m])).get_data()
    pos1 = np.where(data1 > 0)
    data1_1 = zip(*pos1)
    roi_result = []
    for n in range(len(r_terminal_rois)):
        data2 = nib.load(os.path.join(terminal_rois_dir, r_terminal_rois[n])).get_data()
        pos2 = np.where(data2 > 0)
        data2_2 = zip(*pos2)
        roi_result.append(_overlap(data1_1, data2_2, 'percent'))
    r_result.append(roi_result)

print r_result

class_id = ['fib_1', 'fib_2', 'fib_3', 'fib_4']

l_dice = pd.concat([pd.DataFrame(class_id, columns=['class_id']),
                    pd.DataFrame(l_result[3], columns=['hOc3v']),
                    pd.DataFrame(l_result[1], columns=['hOc2']),
                    pd.DataFrame(l_result[0], columns=['hOc1']),
                    pd.DataFrame(l_result[2], columns=['hOc3d'])], axis=1)
r_dice = pd.concat([pd.DataFrame(class_id, columns=['class_id']),
                    pd.DataFrame(r_result[3], columns=['hOc3v']),
                    pd.DataFrame(r_result[1], columns=['hOc2']),
                    pd.DataFrame(r_result[0], columns=['hOc1']),
                    pd.DataFrame(r_result[2], columns=['hOc3d'])], axis=1)

l_dice.to_csv(os.path.join(results_dir, 'l_dice.csv'), index=False)
r_dice.to_csv(os.path.join(results_dir, 'r_dice.csv'), index=False)


