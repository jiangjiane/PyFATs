# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import nibabel as nib
import numpy as np


terminal_rois_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/results/'
results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/results/'

l_terminal_rois = ['l_vis1_fa_merge_mean24.nii.gz',
                   'l_vis2_fa_merge_mean24.nii.gz',
                   'l_vis3_fa_merge_mean24.nii.gz',
                   'l_vis4_fa_merge_mean24.nii.gz']

r_terminal_rois = ['r_vis1_fa_merge_mean24.nii.gz',
                   'r_vis2_fa_merge_mean24.nii.gz',
                   'r_vis3_fa_merge_mean24.nii.gz',
                   'r_vis4_fa_merge_mean24.nii.gz']


l_max = []
l_mean = []
for i in range(len(l_terminal_rois)):
    data1 = nib.load(os.path.join(terminal_rois_dir, l_terminal_rois[i])).get_data()
    pos1 = np.where(data1 > 0)
    data1_1 = zip(*pos1)
    l_max.append(data1.max())
    l_mean.append(data1.sum()/len(data1_1))


r_max = []
r_mean = []
for m in range(len(r_terminal_rois)):
    data1 = nib.load(os.path.join(terminal_rois_dir, r_terminal_rois[m])).get_data()
    pos1 = np.where(data1 > 0)
    data1_1 = zip(*pos1)
    r_max.append(data1.max())
    r_mean.append(data1.sum()/len(data1_1))


fa_id = ['fib1_fa', 'fib2_fa', 'fib3_fa', 'fib4_fa']

l_dice = pd.concat([pd.DataFrame(fa_id, columns=['fa_id']),
                    pd.DataFrame(l_max, columns=['fa_max']),
                    pd.DataFrame(l_mean, columns=['fa_mean'])], axis=1)

r_dice = pd.concat([pd.DataFrame(fa_id, columns=['fa_id']),
                    pd.DataFrame(r_max, columns=['fa_max']),
                    pd.DataFrame(r_mean, columns=['fa_mean'])], axis=1)

l_dice.to_csv(os.path.join(results_dir, 'l_fa.csv'), index=False)
r_dice.to_csv(os.path.join(results_dir, 'r_fa.csv'), index=False)


