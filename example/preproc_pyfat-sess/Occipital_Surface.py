# !/usr/bin/python
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np
import numpy.linalg as npl
from nibabel.affines import apply_affine

from pyfat.io.save import save_nifti
from mayavi import mlab
from surfer import Brain


# load left hemisphere mask and geometry data
roi_surf_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
                  'response_dhollander/subjects/100408/100408/label/lh.aparc.a2009s.annot'
geo_path_l = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
             'response_dhollander/subjects/100408/Native/100408.L.white.native.surf.gii'
#
# # load right hemisphere mask and geometry data
# roi_surf_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#                   'response_dhollander/subjects/996782/996782/label/rh.aparc.a2009s.annot'
# geo_path_r = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
#              'response_dhollander/subjects/996782/Native/996782.R.white.native.surf.gii'


template_vol = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
               'response_dhollander/subjects/100408/T1w_acpc_dc_restore_brain1.25.nii.gz'
out_path = '/home/brain/workingdir/data/dwi/hcp/preprocessed/' \
           'response_dhollander/subjects/100408/ROI/rh_aparc_a2009s_annot_Occipital.nii.gz'

# choose the mask: Occipital
vertices, colortable, label = nib.freesurfer.read_annot(roi_surf_path_l)
gii_data = nib.load(geo_path_l).darrays
coords, faces = gii_data[0].data, gii_data[1].data

l_label_value = np.array(len(coords) * [0])

# for v in list(set(vertices))[13:]:
#     print v
#     l_label_value = np.array(len(coords) * [0])
#     l_label_value[vertices == v] = 1  # lateraloccipital
#     # l_label_value[vertices == 13] = 13  # lingual
#     # l_label_value[vertices == 5] = 5  # cuneus
#     # l_label_value[vertices == 21] = 21  # pericalcarine
#
#
#     # show mask on surface
#     subject_id = "996782"
#     subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/996782"
#     hemi = 'rh'
#     surf = 'white'
#     alpha = 1
#     brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)
#     brain.add_overlay(l_label_value, min=l_label_value[l_label_value > 0].min(),
#                       max=l_label_value.max(), sign='pos', hemi='rh', name='rh')
#     # brain.add_overlay(vertices, min=vertices[vertices > 0].min(),
#     #                   max=vertices.max(), sign='pos', hemi='rh', name='rh')
#
#     mlab.show()

l_label_value[vertices == 2] = 2
l_label_value[vertices == 11] = 11
l_label_value[vertices == 19] = 19
l_label_value[vertices == 20] = 20
l_label_value[vertices == 21] = 21
l_label_value[vertices == 22] = 22
l_label_value[vertices == 43] = 43
l_label_value[vertices == 45] = 45
l_label_value[vertices == 52] = 52
l_label_value[vertices == 58] = 58
l_label_value[vertices == 59] = 59
l_label_value[vertices == 60] = 60
l_label_value[vertices == 61] = 61
l_label_value[vertices == 62] = 62
l_label_value[vertices == 66] = 66


# show mask on surface
subject_id = "100408"
subjects_dir = "/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/100408"
hemi = 'lh'
surf = 'white'
alpha = 1
brain = Brain(subjects_dir=subjects_dir, subject_id=subject_id, hemi=hemi, surf=surf, alpha=alpha)
brain.add_overlay(l_label_value, min=l_label_value[l_label_value > 0].min(),
                  max=l_label_value.max(), sign='pos', hemi='lh', name='lh')


mlab.show()

# l_label_value = np.array(l_label_value)
# coords_c = coords[l_label_value > 0]
# img = nib.load(template_vol)
# new_img = np.zeros(img.shape)
# coords_c = apply_affine(npl.inv(img.affine), coords_c)
#
# for coord in coords_c:
#     new_img[int(round(coord[0])), int(round(coord[1])), int(round(coord[2]))] = 1
#
# save_nifti(new_img, img.affine, out_path)
