# !/usr/bin/python
# -*- coding: utf-8 -*-

import random
import numpy as np
import nibabel as nib
from pyfat.algorithm.fiber_maths import create_registration_paths

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pospath = 'Structure/Native_cytoMPM_thr25.nii.gz'

pos_outpath = '/Structure/Native_cytoMPM_thr25_vis.nii.gz'

paths_file = create_registration_paths(prepath, pospath)

for pf in paths_file:
    img = nib.load(pf)
    data = img.get_data()
    data_temp = np.zeros(img.shape)
    index = range(85, 89)
    v = [0.1, 0.4, 0.65, 1]
    print index
    for i in xrange(len(index)):
        data_temp[data == index[i]] = v[i]  # random.randint(1, 255)
    print data_temp.max()
    print data_temp.min()
    dm_img = nib.Nifti1Image(data_temp.astype("float32"), img.affine)

    sb_id = int(pf.split('/')[9])
    output = prepath + '%s' % sb_id + pos_outpath
    dm_img.to_filename(output)
