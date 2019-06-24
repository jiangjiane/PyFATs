# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from pyfat.core.dataobject import Fasciculus
from dipy.segment.quickbundles import QuickBundles
from pyfat.algorithm.fiber_maths import create_registration_paths
from pyfat.viz.colormap import create_colormap, create_random_colormap
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_all/' \
       'aligned_centroids/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_aligned_centroids_tmp996782.tck'
img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/' \
           '996782/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
fas = Fasciculus(path)
streamlines = fas.get_data()
# print len(streamlines)
fasciculus_id = np.array(fas.get_header()['fasciculus_id'])
# print fasciculus_id

img = nib.load(img_path)

qb = QuickBundles(streamlines, 4)
clusters = qb.clusters()

fiber_simple_3d_show_advanced(img, streamlines)
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

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5.tck'
# pospath = '1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'

paths_file = create_registration_paths(prepath, pospath)
img_path_pos = '/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
for i in xrange(len(clusters)):
    cluster_id = fasciculus_id[clusters[i]['indices']]
    if len(set(cluster_id)) < 4:
        continue
    print i, cluster_id
    # print fasciculus_id
    # print clusters[i]['indices']
    d_id = {}
    ix = 0
    sum_c = 0
    i_c = 0
    addr_to = list(set(fasciculus_id))
    addr_to.sort(key=list(fasciculus_id).index)
    for index in addr_to:
        c = list(fasciculus_id).count(index)
        if index not in set(cluster_id):
            ix += c
            continue
        else:
            sum_c += list(cluster_id).count(index)

        temp = []
        for j in clusters[i]['indices'][i_c:sum_c]:
            temp.append(j - ix)

        d_id[index] = temp
        ix += c
        i_c = sum_c

    # print d_id
    # print d_id.keys()

    for pf in paths_file:
        sb_id = int(pf.split('/')[9])
        if sb_id not in d_id.keys():
            continue
        # load fib
        fa = Fasciculus(pf)
        stream = fa.get_data()

        # remove unmeaning fib
        length_t = fa.get_lengths()
        ind = length_t > 30.
        stream = stream[ind]
        # print len(streamlines)

        # step1 the first Quickbundle clustering
        # remove strange fib: number of the cluster < thre
        q = QuickBundles(stream, 5)
        cluster = q.clusters()
        # print qb.clusters_sizes()
        indexs = []
        for j in range(len(cluster)):
            if cluster[j]['N'] >= 50:
                indexs += cluster[j]['indices']

        stream = stream[indexs]

        # step2 the second Quickbundle clustering
        # remove short fib: length of the cluster < thre
        q = QuickBundles(stream, 5)
        cluster = q.clusters()
        temp_index = []
        for k in d_id[sb_id]:
            temp_index += cluster[k]['indices']
        img_path_q = prepath + '%s' % sb_id + img_path_pos
        img = nib.load(img_path_q)
        print i, sb_id
        fiber_simple_3d_show_advanced(img, stream[temp_index])

        # #####################################
        # stream = stream[temp_index]
        # labels = np.array(len(stream) * [None])
        # qb = QuickBundles(stream, 5)
        # clust = qb.clusters()
        # # keys = clusters.keys()
        # for c in clust:
        #     labels[clust[c]['indices']] = c
        #
        # colormap = create_random_colormap(len(set(labels)))
        # colormap_full = np.ones((len(stream), 3))
        # # print colormap_full
        # for label, color in zip(set(labels), colormap):
        #     colormap_full[np.array(labels) == label] = color
        #
        # fiber_simple_3d_show_advanced(img, stream, colormap_full)
        ###########################################


# cluster_label_id = {}
# for c in clusters:
#     print c, ':', clusters[c]['N']
#     cluster_id = fasciculus_id[clusters[c]['indices']]
#     cluster_label_id[c] = list(set(cluster_id))
#
# print cluster_label_id
#
# labels = fasciculus_id
# colormap = create_random_colormap(len(set(labels)))
# colormap_full = np.ones((len(streamlines), 3))
# # print colormap_full
# for label, color in zip(set(labels), colormap):
#     colormap_full[np.array(labels) == label] = color
#
# # fiber_simple_3d_show_advanced(img, streamlines, colormap_full)
