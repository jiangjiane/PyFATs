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
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_ids'

temp_path = 'Diffusion/tractography/Det/results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

paths_file_l1 = []
paths_file_l2 = []
paths_file_l3 = []
paths_file_l4 = []

paths_file_r1 = []
paths_file_r2 = []
paths_file_r3 = []
paths_file_r4 = []

for subject_id in sessid:
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'lvis1.tck')):
        paths_file_l1.append(os.path.join(subjects_dir, subject_id, temp_path, 'lvis1.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'lvis2.tck')):
        paths_file_l2.append(os.path.join(subjects_dir, subject_id, temp_path, 'lvis2.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'lvis3.tck')):
        paths_file_l3.append(os.path.join(subjects_dir, subject_id, temp_path, 'lvis3.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'lvis4.tck')):
        paths_file_l4.append(os.path.join(subjects_dir, subject_id, temp_path, 'lvis4.tck'))

    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'rvis1.tck')):
        paths_file_r1.append(os.path.join(subjects_dir, subject_id, temp_path, 'rvis1.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'rvis2.tck')):
        paths_file_r2.append(os.path.join(subjects_dir, subject_id, temp_path, 'rvis2.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'rvis3.tck')):
        paths_file_r3.append(os.path.join(subjects_dir, subject_id, temp_path, 'rvis3.tck'))
    if os.path.exists(os.path.join(subjects_dir, subject_id, temp_path, 'rvis4.tck')):
        paths_file_r4.append(os.path.join(subjects_dir, subject_id, temp_path, 'rvis4.tck'))

# print int(filter(lambda x: x.isdigit(), paths_file_l[0].split('/'))[0])

for i in range(len(paths_file_l1)):
    print 'l', int(filter(lambda x: x.isdigit(), paths_file_l1[i].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[i], temp_path, 'lvis1_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_l1, 20)
    fas.save2tck(out_path)
    temp = paths_file_l1.pop(0)
    paths_file_l1.append(temp)

print 'lvis1, Done'

for i in range(len(paths_file_l2)):
    print 'l', int(filter(lambda x: x.isdigit(), paths_file_l2[i].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[i], temp_path, 'lvis2_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_l2, 20)
    fas.save2tck(out_path)
    temp = paths_file_l2.pop(0)
    paths_file_l2.append(temp)

print 'lvis2, Done'

for i in range(len(paths_file_l3)):
    print 'l', int(filter(lambda x: x.isdigit(), paths_file_l3[i].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[i], temp_path, 'lvis3_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_l3, 20)
    fas.save2tck(out_path)
    temp = paths_file_l3.pop(0)
    paths_file_l3.append(temp)

print 'lvis3, Done'


for i in range(len(paths_file_l4)):
    print 'l', int(filter(lambda x: x.isdigit(), paths_file_l4[i].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[i], temp_path, 'lvis4_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_l4, 20)
    fas.save2tck(out_path)
    temp = paths_file_l4.pop(0)
    paths_file_l4.append(temp)

print 'lvis4, Done'

for j in range(len(paths_file_r1)):
    print 'r', int(filter(lambda x: x.isdigit(), paths_file_r1[j].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[j], temp_path, 'rvis1_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_r1, 20)
    fas.save2tck(out_path)
    temp = paths_file_r1.pop(0)
    paths_file_r1.append(temp)

print 'rvis1, Done'

for j in range(len(paths_file_r2)):
    print 'r', int(filter(lambda x: x.isdigit(), paths_file_r2[j].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[j], temp_path, 'rvis2_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_r2, 20)
    fas.save2tck(out_path)
    temp = paths_file_r2.pop(0)
    paths_file_r2.append(temp)

print 'rvis2, Done'

for j in range(len(paths_file_r3)):
    print 'r', int(filter(lambda x: x.isdigit(), paths_file_r3[j].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[j], temp_path, 'rvis3_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_r3, 20)
    fas.save2tck(out_path)
    temp = paths_file_r3.pop(0)
    paths_file_r3.append(temp)

print 'rvis3, Done'

for j in range(len(paths_file_r4)):
    print 'r', int(filter(lambda x: x.isdigit(), paths_file_r4[j].split('/'))[0])
    out_path = os.path.join(subjects_dir, sessid[j], temp_path, 'rvis4_all_subjects.tck')
    fas = muti_bundle_registration(paths_file_r4, 20)
    fas.save2tck(out_path)
    temp = paths_file_r4.pop(0)
    paths_file_r4.append(temp)

print 'rvis4, Done'
