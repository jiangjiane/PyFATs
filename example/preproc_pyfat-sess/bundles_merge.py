# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
print nib.__version__
from dipy.segment.quickbundles import QuickBundles
import nibabel.streamlines.array_sequence as nibas


from pyfat.core.dataobject import Fasciculus


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'
subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'

temp_path = 'Diffusion/tractography/Det/new_results'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]

tck_name_l = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck']
tck_name_r = ['rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

for subject_id in sessid:
    print subject_id
    filename = os.listdir(os.path.join(subjects_dir, subject_id, temp_path))
    l_filename = []
    r_filename = []
    for k in range(len(tck_name_l)):
        if tck_name_l[k] in filename:
            l_filename.append(tck_name_l[k])

        if tck_name_r[k] in filename:
            r_filename.append(tck_name_r[k])

    first_file_l = os.path.join(subjects_dir, subject_id, temp_path, l_filename[0])
    # fib_l = Fasciculus(first_file_l)
    # fib_data_l = fib_l.get_data()
    print l_filename[0][4]
    fib_l = nib.streamlines.tck.TckFile.load(first_file_l)
    fib_data_l = fib_l.streamlines
    centroids_l = QuickBundles(fib_data_l, float('inf')).centroids
    bundle_header_l = dict()
    bundle_header_l['fasciculus_id'] = len(fib_data_l) * [int(l_filename[0][4])]

    first_file_r = os.path.join(subjects_dir, subject_id, temp_path, r_filename[0])
    # fib_r = Fasciculus(first_file_r)
    # fib_data_r = fib_r.get_data()
    fib_r = nib.streamlines.tck.TckFile.load(first_file_r)
    fib_data_r = fib_r.streamlines
    centroids_r = QuickBundles(fib_data_r, float('inf')).centroids
    bundle_header_r = dict()
    bundle_header_r['fasciculus_id'] = len(fib_data_r) * [int(r_filename[0][4])]

    for i in range(len(l_filename)-1):
        print l_filename[i+1]
        temp_file = os.path.join(subjects_dir, subject_id, temp_path, l_filename[i+1])
        temp_fib = Fasciculus(temp_file).get_data()
        temp_centrois = QuickBundles(temp_fib, float('inf')).centroids

        lenth = len(fib_data_l)
        fib_data_l.extend(temp_fib)
        centroids_l.extend(temp_centrois)
        bundle_header_l['fasciculus_id'] += (len(fib_data_l) - lenth) * [int(l_filename[i+1][4])]

    for j in range(len(r_filename)-1):
        print r_filename[j+1]
        temp_file = os.path.join(subjects_dir, subject_id, temp_path, r_filename[j + 1])
        temp_fib = Fasciculus(temp_file).get_data()
        temp_centrois = QuickBundles(temp_fib, float('inf')).centroids

        lenth = len(fib_data_r)
        fib_data_r.extend(temp_fib)
        centroids_r.extend(temp_centrois)
        bundle_header_r['fasciculus_id'] += (len(fib_data_r) - lenth) * [int(r_filename[j+1][4])]

    fib_l = Fasciculus(first_file_l)
    fib_l.set_data(nibas.ArraySequence(centroids_l))
    out_centroids = os.path.join(subjects_dir, subject_id, temp_path, 'left_vis_all_centroids.tck')
    fib_l.save2tck(out_centroids)
    fib_l.update_header(bundle_header_l)
    fib_l.set_data(fib_data_l)
    out_fib_l = os.path.join(subjects_dir, subject_id, temp_path, 'left_vis_all.tck')
    fib_l.save2tck(out_fib_l)

    fib_r = Fasciculus(first_file_r)
    fib_r.set_data(nibas.ArraySequence(centroids_r))
    out_centroids = os.path.join(subjects_dir, subject_id, temp_path, 'right_vis_all_centroids.tck')
    fib_r.save2tck(out_centroids)
    fib_r.update_header(bundle_header_r)
    fib_r.set_data(fib_data_r)
    out_fib_r = os.path.join(subjects_dir, subject_id, temp_path, 'right_vis_all.tck')
    fib_r.save2tck(out_fib_r)
