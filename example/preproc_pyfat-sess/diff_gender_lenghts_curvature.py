# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import os
import nibabel as nib

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_gender'
tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

sessid = [strs.split(' ') for strs in sessid]

sessid_f = []
sessid_m = []
for sub_g in sessid:
    if sub_g[1] is 'f':
        sessid_f.append(sub_g[0])
    elif sub_g[1] is 'm':
        sessid_m.append(sub_g[0])
    else:
        ValueError("There is no such gender.")

sessid = [sessid_m, sessid_f]

length_mean_lr = []
length_std_lr = []
for tck in tck_name:
    length_mean = []
    length_std = []
    for sub in sessid:
        length_mean_sub = []
        for subject in sub:
            print subject

            fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
            if not os.path.exists(fib_path):
                continue
            fas = Fasciculus(fib_path)
            # length_mean_sub.append(np.mean(fas.get_lengths()))
            # length_mean_sub.append(len(fas.get_data()))
            length_mean_sub.append(np.mean(fas.get_mean_curvature()))
        length_mean.append(np.mean(length_mean_sub))
        length_std.append(np.std(length_mean_sub)/np.sqrt(len(length_mean_sub)))
    length_mean_lr.append(length_mean)
    length_std_lr.append(length_std)


n_groups = 8

means_men = np.array(length_mean_lr)[:, 0]
std_men = np.array(length_std_lr)[:, 0]

means_women = np.array(length_mean_lr)[:, 1]
std_women = np.array(length_std_lr)[:, 1]

fig, ax = plt.subplots()

index = np.arange(n_groups)
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = ax.bar(index, means_men, bar_width,
                alpha=opacity, color='b',
                yerr=std_men, error_kw=error_config,
                label='M')

rects2 = ax.bar(index + bar_width, means_women, bar_width,
                alpha=opacity, color='r',
                yerr=std_women, error_kw=error_config,
                label='F')

ax.set_xlabel('Group')
ax.set_ylabel('Curvatures')
ax.set_title('Curvatures by group and gender')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(('lfib1', 'lfib2', 'lfib3', 'lfib4', 'rfib1', 'rfib2', 'rfib3', 'rfib4'))
ax.legend()

fig.tight_layout()
out_results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'
plt.savefig(os.path.join(out_results_dir, 'giff_gender_curvatures.tif'), dpi=300)

plt.show()
