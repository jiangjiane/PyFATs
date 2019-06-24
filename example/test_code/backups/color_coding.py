# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from pyfat.io.save import save_nifti
import nibabel.streamlines.array_sequence as nibas
from pyfat.io.save import save_nifti
from pyfat.algorithm.cc_seg import endpoints_axis2cc, cc_seg_mp, cc_seg_mpm
from dipy.segment.quickbundles import QuickBundles
from pyfat.core.dataobject import Fasciculus
from pyfat.algorithm.fiber_clustering import FibClustering
from pyfat.viz.colormap import create_colormap, create_random_colormap
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced


img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
# img_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/101107/lab_map/native1.25_wang_maxprob_vol_lh_mask.nii.gz'
tck_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/101107/Diffusion/1M_20_01_20dynamic250_SD_Stream_occipital8_lr5.tck'

img = nib.load(img_path)
fasciculus = Fasciculus(tck_path)
streamlines = fasciculus.get_data()
print len(streamlines)
# fasciculus.set_data(streamlines[fasciculus.get_lengths() > 150])
# streamlines = fasciculus.get_data()
# print len(streamlines)


# qb = QuickBundles(streamlines, 10)
# # qb.remove_small_clusters(50)
# clusters = qb.clusters()
#
# print len(clusters)
#
# # Color each streamline according to the cluster they belong to.
# colormap = create_random_colormap(len(set(clusters)))
# colormap_full = np.ones((len(streamlines), 3))
# # print colormap_full
# for cluster, color in zip(clusters, colormap):
#     colormap_full[clusters[cluster]['indices']] = color
# print colormap_full


fibclusters = FibClustering(fasciculus)
labels = fibclusters.endpoints_seg(temp_clusters=5000, mode='lh', thre=5.5)
print len(set(labels))
colormap = create_random_colormap(len(set(labels)))
colormap_full = np.ones((len(streamlines), 3))
# print colormap_full
for label, color in zip(set(labels), colormap):
    colormap_full[labels == label] = color

hemi_fib = fibclusters.hemisphere_cc(hemi='lh')

fiber_simple_3d_show_advanced(img, hemi_fib, colormap_full)

# y_cc_density = endpoints_axis2cc(img_path, tck_path, axis='y', mode='max')
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/Structure/SD_Stream_plenium_roi_fib_y_y_cc_density_l.nii.gz'
# save_nifti(y_cc_density[0], img.affine, out_path)
# out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#            'response_dhollander/100408/Structure/SD_Stream_plenium_roi_fib_y_y_cc_density_r.nii.gz'
# save_nifti(y_cc_density[1], img.affine, out_path)

# cc_mp = cc_seg_mp(img_path, tck_path, labels)
# output = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/cc_seg_mp.nii.gz'
# save_nifti(cc_mp, img.affine, output, float)
#
# cc_mpm = cc_seg_mpm(cc_mp, 0.1)
# output = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/100408/Structure/cc_seg_mmp.nii.gz'
# save_nifti(cc_mpm, img.affine, output, float)
