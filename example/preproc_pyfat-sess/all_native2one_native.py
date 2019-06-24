# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas
from pyfat.algorithm.fiber_maths import muti_bundle_registration


from pyfat.core.dataobject import Fasciculus


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'

temp_path = 'Diffusion/tractography/Det/results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

paths_file_l = []
paths_file_r = []
for subject_id in sessid:
    paths_file_l.append(os.path.join(subjects_dir, subject_id, temp_path, 'l_vis_centroids.tck'))
    paths_file_r.append(os.path.join(subjects_dir, subject_id, temp_path, 'r_vis_centroids.tck'))

# print int(filter(lambda x: x.isdigit(), paths_file_l[0].split('/'))[0])

for i in range(len(paths_file_l)):
    print 'l', int(filter(lambda x: x.isdigit(), paths_file_l[i].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[i], temp_path, 'l_vis_centroids_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_l, 20)
    fas.save2tck(out_path)
    temp = paths_file_l.pop(0)
    paths_file_l.append(temp)

for j in range(len(paths_file_r)):
    print 'r', int(filter(lambda x: x.isdigit(), paths_file_r[j].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[j], temp_path, 'r_vis_centroids_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_r, 20)
    fas.save2tck(out_path)
    temp = paths_file_r.pop(0)
    paths_file_r.append(temp)
