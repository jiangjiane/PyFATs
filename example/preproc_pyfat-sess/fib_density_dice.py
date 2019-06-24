# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import seaborn as sns
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt


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


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
file_dir = 'Diffusion/tractography/Det/new_results'

# tck_name = ['lvis1_density_map_MNI152.nii.gz',
#             'lvis2_density_map_MNI152.nii.gz',
#             'lvis3_density_map_MNI152.nii.gz',
#             'lvis4_density_map_MNI152.nii.gz']
# tck_name = ['rvis1_density_map_MNI152.nii.gz',
#             'rvis2_density_map_MNI152.nii.gz',
#             'rvis3_density_map_MNI152.nii.gz',
#             'rvis4_density_map_MNI152.nii.gz']

tck_name = ['rvis1_template_centroids_terminus_MNI152.nii.gz',
            'rvis2_template_centroids_terminus_MNI152.nii.gz',
            'rvis3_template_centroids_terminus_MNI152.nii.gz',
            'rvis4_template_centroids_terminus_MNI152.nii.gz']
#
# tck_name = ['lvis1_template_centroids_terminus_MNI152.nii.gz',
#             'lvis2_template_centroids_terminus_MNI152.nii.gz',
#             'lvis3_template_centroids_terminus_MNI152.nii.gz',
#             'lvis4_template_centroids_terminus_MNI152.nii.gz']

std_name = ['standard/r_MNI152_cytoMPM_thr25_1mm_hOc1.nii.gz',
            'standard/r_MNI152_cytoMPM_thr25_1mm_hOc2.nii.gz',
            'standard/r_MNI152_cytoMPM_thr25_1mm_hOc3d.nii.gz',
            'standard/r_MNI152_cytoMPM_thr25_1mm_hOc3v.nii.gz']
#
# std_name = ['standard/l_MNI152_cytoMPM_thr25_1mm_hOc1.nii.gz',
#             'standard/l_MNI152_cytoMPM_thr25_1mm_hOc2.nii.gz',
#             'standard/l_MNI152_cytoMPM_thr25_1mm_hOc3d.nii.gz',
#             'standard/l_MNI152_cytoMPM_thr25_1mm_hOc3v.nii.gz']

results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

sessid = ['101915']
# sessid = ['101309']

tck_file = []
for tck in tck_name:
    for sub in sessid:
        tck_path = os.path.join(subjects_dir, sub, file_dir, tck)
        if os.path.exists(tck_path):
            tck_file.append(tck_path)
            print tck_path
for tck in std_name:
    for sub in sessid:
        tck_path = os.path.join(subjects_dir, tck)
        if os.path.exists(tck_path):
            tck_file.append(tck_path)
            print tck_path

print len(tck_file)
print tck_file

dices = []
c = 0
for fib_file in tck_file:
    c += 1
    print c
    dice = []
    data1 = nib.load(fib_file).get_data()
    pos1 = np.where(data1 > 0)
    data1_1 = zip(*pos1)

    for fib_file2 in tck_file:
        data2 = nib.load(fib_file2).get_data()
        pos2 = np.where(data2 > 0)
        data2_2 = zip(*pos2)
        if fib_file == fib_file2:
            dice.append(0)
        else:
            dice.append(_overlap(data1_1, data2_2, index='percent'))
    dices.append(dice)

sns.set()
ax = sns.heatmap(dices)
plt.savefig(os.path.join(results_dir, 'rvis_template_centroids_terminus_MNI152_percent.tif'), dpi=300)
plt.show()
