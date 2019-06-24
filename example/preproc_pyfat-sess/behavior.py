# !/usr/bin/python
# -*- conding: utf-8 -*-


import re
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt

from pyfat.core.dataobject import Fasciculus


behavior_file = '/home/brain/workingdir/pyfat/bin/pipeline_file/BehavioralData.csv'
subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'

results_dir = 'Diffusion/tractography/Det/new_results'

# tck_name = ['lvis1_fa.txt', 'lvis2_fa.txt', 'lvis3_fa.txt', 'lvis4_fa.txt',
#             'rvis1_fa.txt', 'rvis2_fa.txt', 'rvis3_fa.txt', 'rvis4_fa.txt']
tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
            'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']


behavior_data = pd.read_csv(behavior_file)

sessid = list(behavior_data['Subject'])
behavior = list(behavior_data['Mars_Final'])

print sessid
print behavior

def is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(num)

    return True if result else False


for f in tck_name:
    print f
    fa_data = []
    behavior_final = []
    for i in range(len(sessid)):
        fib_path = os.path.join(subjects_dir, str(sessid[i]), results_dir, f)
        if not os.path.exists(fib_path):
            continue

        # with open(fib_path, 'r') as fa:
        #     fa_val = fa.readlines()
        #     fa_list = [strs.strip().split(' ') for strs in fa_val]
        #     fa_lists = [[float(val) for val in strs if is_number(val)] for strs in fa_list]

        fas = Fasciculus(fib_path)

        # sub_fa = [fa_lines[0] if fa_lines[0] > fa_lines[-1] else fa_lines[-1] for fa_lines in fa_lists]
        # fa_data.append(np.mean(sub_fa))
        fa_data.append(fas.get_counts())
        # fa_data.append(np.mean(fa_lists))
        # fa_data.append(np.mean(fas.get_lengths()))
        # fa_data.append(np.mean(fas.get_mean_curvature()))
        behavior_final.append(behavior[i])

    sns.set(style='ticks', color_codes=True)
    # tips = sns.load_dataset("tips")
    # print tips
    fa_data = np.array(fa_data) / float(np.array(fa_data).max())
    g = sns.JointGrid(x=fa_data, y=behavior_final)
    g = g.plot(sns.regplot, sns.distplot)
    g = g.annotate(stats.pearsonr)
    # plt.title("Correlation Between Contrast Sensitivity and FA - {}".format(f[:5]))
    plt.xlabel("FiberDensity - {}".format(f[:5]))
    plt.ylabel("Contrast Sensitivity")
    out_results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'
    plt.savefig(os.path.join(out_results_dir, 'CS_{}_FiberDensity.tif'.format(f.split('.')[0])), dpi=300)
    # plt.show()

