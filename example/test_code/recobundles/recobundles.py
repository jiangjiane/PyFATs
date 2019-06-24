# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from dipy.tracking.utils import length
from pyfat.viz.colormap import create_colormap, create_random_colormap
import nibabel.streamlines.tck as nibas
from pyfat.core.dataobject import Fasciculus
from dipy.segment.quickbundles import QuickBundles
from pyfat.algorithm.fiber_maths import create_registration_paths, bundle_registration, muti_bundle_registration
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'
pos_outpath = '1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_centroids.tck'

paths_file = create_registration_paths(prepath, pospath)

img_path_pos = '/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'

for pf in paths_file:
    # load fib
    fa = Fasciculus(pf)
    streamlines = fa.get_data()

    # remove unmeaning fib
    length_t = fa.get_lengths()
    ind = length_t > 30.
    streamlines = streamlines[ind]
    # fa.set_data(streamlines)
    # print len(streamlines)

    # step1 the first Quickbundle clustering
    # remove strange fib: number of the cluster < thre
    qb = QuickBundles(streamlines, 1)
    clusters = qb.clusters()
    # print qb.clusters_sizes()
    indexs = []
    for i in range(len(clusters)):
        if clusters[i]['N'] >= 50:
            indexs += clusters[i]['indices']

    streamlines = streamlines[indexs]

    # step2 the second Quickbundle clustering
    # remove short fib: length of the cluster < thre
    qb = QuickBundles(streamlines, 2)
    clusters = qb.clusters()

    ##########################################
    sb_id = int(pf.split('/')[9])
    img_path_q = prepath + '%s' % sb_id + img_path_pos
    img = nib.load(img_path_q)
    labels = np.array(len(streamlines) * [None])
    # keys = clusters.keys()
    for c in clusters:
        labels[clusters[c]['indices']] = c

    colormap = create_random_colormap(len(set(labels)))
    colormap_full = np.ones((len(streamlines), 3))
    # print colormap_full
    for label, color in zip(set(labels), colormap):
        colormap_full[np.array(labels) == label] = color

    fiber_simple_3d_show_advanced(img, streamlines, colormap_full)
    ####################################################

    centroids = qb.centroids
    print len(centroids)
    # fa.set_data(nibas.ArraySequence(centroids))
    # fa.save2tck(os.path.join(os.path.split(pf)[0], pos_outpath))

#
# prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
# pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_centroids.tck'
# # pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5_centroids.tck'
# paths_file = create_registration_paths(prepath, pospath)
#
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_all/' \
#            'aligned_centroids/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_aligned_centroids_tmp%s.tck'
#
# for _ in range(len(paths_file)):
#     fas = muti_bundle_registration(paths_file, 20)
#     subject_id = paths_file[0].split('/')[9]
#     fas.save2tck(out_path % subject_id)
#     temp = paths_file.pop(0)
#     paths_file.append(temp)
