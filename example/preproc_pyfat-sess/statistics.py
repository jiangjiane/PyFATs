# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import os
import nibabel as nib

from tools import permutation_diff
from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_qyk'
tck_name_lr = [['lvis1.tck', 'rvis1.tck'], ['lvis2.tck', 'rvis2.tck'],
               ['lvis3.tck', 'rvis3.tck'], ['lvis4.tck', 'rvis4.tck']]


results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

length_mean_lr = []
for tck_name in tck_name_lr:
    length_mean = []
    for tck in tck_name:
        length_mean_sub = []
        for subject in sessid:
            print subject

            fib_path = os.path.join(subjects_dir, subject, 'new_results', tck)
            if not os.path.exists(fib_path):
                continue
            fas = Fasciculus(fib_path)
            length_mean_sub.append(np.mean(fas.get_lengths()))
            # length_mean_sub.append(np.mean(fas.get_mean_curvature()))
        length_mean += length_mean_sub
    length_mean_lr.append(length_mean)

for i in range(len(length_mean_lr)):
    for j in range(i+1, len(length_mean_lr)):
        sts = permutation_diff(length_mean_lr[i], length_mean_lr[j], n_permutation=1000)
        print tck_name_lr[i], tck_name_lr[j]
        print sts[-1]
