# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from surfer import Brain
from mayavi import mlab
from dipy.tracking.utils import length
from pyfat.viz.colormap import create_colormap, create_random_colormap
import nibabel.streamlines.tck as nibas
from pyfat.core.dataobject import Fasciculus
from dipy.segment.quickbundles import QuickBundles
from pyfat.algorithm.fiber_maths import create_registration_paths, bundle_registration, muti_bundle_registration
from pyfat.viz.fiber_simple_viz_advanced import fiber_simple_3d_show_advanced
from pyfat.algorithm.fasc_mapping import terminus2hemi_surface_density_map, terminus2surface_density_map
from pyfat.viz.surfaceview import surface_streamlines_map, surface_roi_contour
from pyfat.algorithm.roi_vol_surf import roi_vol2surf

prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/'
# pos_outpath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5.tck'
# pospath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_rhemi_occipital5.tck'
# pos_outpath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_vis.tck'
pos_outpath = 'Diffusion/SD/1M_20_01_20dynamic250_SD_Stream_lhemi_occipital5_vis_interface.tck'

paths_file = create_registration_paths(prepath, pos_outpath)

img_path = '/Structure/T1w_acpc_dc_restore_brain1.25.nii.gz'
img_path_pos = '/Structure/Native_cytoMPM_thr25_vis.nii.gz'

for pf in paths_file:
    # load fib
    fa = Fasciculus(pf)
    streamlines = fa.get_data()

    qb = QuickBundles(streamlines, 5)
    clusters = qb.clusters()

    # ##########################################
    sb_id = int(pf.split('/')[9])
    img_path_q = prepath + '%s' % sb_id + img_path_pos
    # ####
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

    print sb_id
    fiber_simple_3d_show_advanced(img, streamlines, colormap_full, imgcolor=True)

    # img_path_qs = prepath + '%s' % sb_id + img_path
    # img = nib.load(img_path_qs)
    # fiber_simple_3d_show_advanced(img, streamlines, colormap_full)

    # #################
    # subject_id = "%s" % sb_id
    # subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/%s" % sb_id
    # hemi = 'lh'
    # surf = 'white'
    # alpha = 1
    # geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
    #              'response_dhollander/%s/Native/%s.L.white.native.surf.gii' % (sb_id, sb_id)
    # geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
    #              'response_dhollander/%s/Native/%s.R.white.native.surf.gii' % (sb_id, sb_id)
    #
    # roi_surf = roi_vol2surf(img_path_q, [geo_path_l, geo_path_r])
    #
    # print len(clusters)
    # brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)
    # brain.add_overlay(roi_surf[0], min=roi_surf[0][roi_surf[0] > 0].min(),
    #                   max=roi_surf[0].max(), sign='pos', hemi='lh', name='lh')
    # for c in clusters:
    #     stream = streamlines[clusters[c]['indices']]
    #     value = terminus2surface_density_map(stream, [geo_path_l, geo_path_r])
    #     # surface_roi_contour(subjects_dir, subject_id, hemi, surf, alpha, value, roi_surf)
    #     # surface_streamlines_map(subjects_dir, subject_id, hemi, surf, alpha, value)
    #
    #     brain.add_overlay(value[0], min=value[0][value[0] > 0].min(),
    #                       max=value[0].max(), sign='neg', hemi='lh', name='lh')
    # mlab.show()
