# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import re
import os
import nibabel as nib

from pyfat.core.dataobject import Fasciculus

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_gender'
file_dir = 'Diffusion/tractography/Det/new_results'
# results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'

tck_fa_name = ['lvis1_fa.txt', 'lvis2_fa.txt', 'lvis3_fa.txt', 'lvis4_fa.txt',
               'rvis1_fa.txt', 'rvis2_fa.txt', 'rvis3_fa.txt', 'rvis4_fa.txt']

tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

# tck_fa_name = ['lvis1_fa.txt']

# results_dir = 'Diffusion/tractography/Det/new_results'

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


def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)

    return True if result else False


fa_result = []
lengths_result = []
for k in range(len(tck_fa_name)):
    fa_mean_subs = []
    lengths = float('-inf')
    for subject in sessid:
        fa_mean_sub = []
        for sub in subject:
            fib_path = os.path.join(subjects_dir, sub, file_dir, tck_fa_name[k])
            if not os.path.exists(fib_path):
                continue

            with open(fib_path, 'r') as fa:
                fa_val = fa.readlines()
                fa_list = [strs.strip().split(' ') for strs in fa_val]
                fa_lists = [[float(val) for val in strs if is_number(val)] for strs in fa_list]

            sub_fa = [fa_lines if fa_lines[0] > fa_lines[-1] else fa_lines[::-1] for fa_lines in fa_lists]
            fa_mean_sub.append(np.array(sub_fa).mean(axis=0))
            fas = Fasciculus(os.path.join(subjects_dir, sub, file_dir, tck_name[k]))
            sub_length = fas.get_lengths().max()
            if sub_length > lengths:
                lengths = sub_length
        fa_mean_subs.append(np.array(fa_mean_sub).mean(axis=0))
    lengths_result.append(lengths)
    fa_result.append(fa_mean_subs)

for i in range(len(fa_result)):
    plt.subplots()
    plt.title(tck_fa_name[i].split('.')[0])
    plt.plot(np.linspace(0, lengths_result[i], 200), fa_result[i][0], color='green', label='Male')
    plt.plot(np.linspace(0, lengths_result[i], 200), fa_result[i][1], color='blue', label='Female')

    # plt.title('Right FA')
    #
    # plt.plot(np.linspace(0, lengths_result[i+4], 200), np.array(fa_result[i+4]).mean(axis=0), color='purple', label='R-fib1')
    # plt.plot(np.linspace(0, lengths_result[i+5], 200), np.array(fa_result[i+5]).mean(axis=0), color='yellowgreen', label='R-fib2')
    # plt.plot(np.linspace(0, lengths_result[i+6], 200), np.array(fa_result[i+6]).mean(axis=0), color='violet', label='R-fib3')
    # plt.plot(np.linspace(0, lengths_result[i+7], 200), np.array(fa_result[i+7]).mean(axis=0), color='green', label='R-fib4')

    plt.xlabel('Location')
    plt.ylabel('Fractional Anisotropy')

    plt.legend()
    plt.tight_layout()
    out_results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'
    # plt.savefig(os.path.join(out_results_dir, 'merge_{}.tif'.format(tck_fa_name[i].split('.')[0][1:])), dpi=300)

    plt.savefig(os.path.join(out_results_dir, 'm_f_{}.tif'.format(tck_fa_name[i].split('.')[0])), dpi=300)

    plt.show()
    plt.close()
