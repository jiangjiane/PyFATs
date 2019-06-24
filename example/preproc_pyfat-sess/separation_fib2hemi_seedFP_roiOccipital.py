#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_extract import FibSelection


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'

# subject_id = [100206, 100307, 100408, 100610]
# subject_id = [200008, 102008, 597869]
# subject_id = [103111, 111211, 201818, 333330, 530635, 555651, 686969,
#               767464, 888678, 995174, 996782, 102513, 102614, 102715,
#               102816, 103010]
subject_id = [100408, 101410]

temp_path = 'Diffusion/tractography/Det'

file_name = ['SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_L_100k.tck',
             'SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_R_100k.tck']

out_file_name = ['SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_L_100k_{hemi}.tck',
                 'SD_Stream_angle20_cutoff0.03_length50_250_seedFP_roiOccipital_R_100k_{hemi}.tck']

h = ['lh', 'rh']

for i in xrange(len(subject_id)):
    print subject_id[i]
    for j in xrange(len(file_name)):
        file_path = os.path.join(subjects_dir, str(subject_id[i]), temp_path, file_name[j])
        out_path = os.path.join(subjects_dir, str(subject_id[i]), temp_path, out_file_name[j])
        fas = Fasciculus(file_path)
        fib_select = FibSelection(fas)
        fib1 = fib_select.endpoint_dissimilarity()
        fas.set_data(fib1)
        fib_select2 = FibSelection(fas)
        fib2 = fib_select2.single_point_mid_sag()
        fas.set_data(fib2)
        f = fas.separation_fib_to_hemi()
        if j == 0:
            fas.set_data(f[1])
            fas.save2tck(out_path.format(hemi=h[1]))
        else:
            fas.set_data(f[0])
            fas.save2tck(out_path.format(hemi=h[0]))
