# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import seaborn as sns
import matplotlib.pyplot as plt

import nibabel.streamlines.array_sequence as nibas
from pyfat.core.dataobject import Fasciculus
from dipy.tracking.streamline import bundles_distances_mdf

subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest'
subjects_id = '101309'
tck_name = ['lvis1_template_centroids.tck', 'lvis2_template_centroids.tck',
            'lvis3_template_centroids.tck', 'lvis4_template_centroids.tck']


results_dir = 'Diffusion/tractography/Det/new_results'

path = os.path.join(subjects_dir, subjects_id, 'new_results')

fib = nibas.ArraySequence()
for tck in tck_name:
    fas = Fasciculus(os.path.join(path, tck))
    f = fas.get_data()
    fib.extend(f)

dist = bundles_distances_mdf(fib, fib)
print dist.shape

sns.set()
ax = sns.heatmap(dist)
plt.savefig(os.path.join(subjects_dir, 'new_results', 'left_distance.tif'), dpi=300)
plt.show()

