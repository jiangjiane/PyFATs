# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import nibabel as nib

from pyfat.core.dataobject import Fasciculus
from pyfat.io.save import save_nifti
from pyfat.algorithm.fasc_mapping import fib_density_map

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'
tck_name_lr = [['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck'],
               ['rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']]


results_dir = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

length_mean_lr = []
length_std_lr = []
for tck_name in tck_name_lr:
    length_mean = []
    length_std = []
    for tck in tck_name:
        length_mean_sub = []
        for subject in sessid:
            print subject

            fib_path = os.path.join(subjects_dir, subject, results_dir, tck)
            if not os.path.exists(fib_path):
                continue
            fas = Fasciculus(fib_path)
            # length_mean_sub.append(np.mean(fas.get_lengths()))
            # length_mean_sub.append(len(fas.get_data()))
            orientation = np.array(fas.get_mean_orientation()).sum(axis=0)
            soa = np.array([[0, 0, 0, orientation[0], orientation[1], orientation[2]]])

            X, Y, Z, U, V, W = zip(*soa)

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.quiver(X, Y, Z, U, V, W)

            ax.set_xlim([-1, 0.5])
            ax.set_ylim([-1, 1.5])
            ax.set_zlim([-1, 8])
            plt.show()
            length_mean_sub.append(np.mean(fas.get_mean_curvature()))
        length_mean.append(np.mean(length_mean_sub))
        length_std.append(np.std(length_mean_sub)/np.sqrt(len(length_mean_sub)))
    length_mean_lr.append(length_mean)
    length_std_lr.append(length_std)


# n_groups = 4
#
# means_men = length_mean_lr[0]
# std_men = length_std_lr[0]
#
# means_women = length_mean_lr[1]
# std_women = length_std_lr[1]
#
# fig, ax = plt.subplots()
#
# index = np.arange(n_groups)
# bar_width = 0.35
#
# opacity = 0.4
# error_config = {'ecolor': '0.3'}
#
# rects1 = ax.bar(index, means_men, bar_width,
#                 alpha=opacity, color='b',
#                 yerr=std_men, error_kw=error_config,
#                 label='Left')
#
# rects2 = ax.bar(index + bar_width, means_women, bar_width,
#                 alpha=opacity, color='r',
#                 yerr=std_women, error_kw=error_config,
#                 label='Right')
#
# ax.set_xlabel('Group')
# ax.set_ylabel('Curvature')
# ax.set_title('Curvature by group and hemisphere')
# ax.set_xticks(index + bar_width / 2)
# ax.set_xticklabels(('fib1', 'fib2', 'fib3', 'fib4'))
# ax.legend()
#
# fig.tight_layout()
# out_results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/new_results/'
# plt.savefig(os.path.join(out_results_dir, 'curvature.tif'), dpi=300)
#
# plt.show()




