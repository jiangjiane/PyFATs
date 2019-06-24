# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import numpy as np
import nibabel as nib
from dipy.viz import window, actor
from dipy.tracking.streamline import transform_streamlines

from pyfat.core.dataobject import Fasciculus


prepath = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects/'
tck_path = 'Diffusion/tractography/Det/new_results'
# tck_name = ['lvis1.tck', 'lvis2.tck', 'lvis3.tck', 'lvis4.tck',
#             'rvis1.tck', 'rvis2.tck', 'rvis3.tck', 'rvis4.tck']

# tck_name = ['lvis1_template_centroids.tck', 'lvis2_template_centroids.tck',
#             'lvis3_template_centroids.tck', 'lvis4_template_centroids.tck']

tck_name = ['rvis1_template_centroids.tck', 'rvis2_template_centroids.tck',
            'rvis3_template_centroids.tck', 'rvis4_template_centroids.tck']

subjects_id = '/home/brain/workingdir/pyfat/bin/pipeline_file/subjects_id'

with open(subjects_id, 'r') as f:
    sessid = f.readlines()
    sessid = [_.strip() for _ in sessid]


# sessid = ['101309']
sessid = ['101915']

for sb_id in sessid:
    print sb_id
    fa_file = os.path.join(prepath, str(sb_id), 'Diffusion/metrics/fa.nii.gz')
    img = nib.load(fa_file)
    fa = img.get_data()
    affine = img.affine
    for tck in tck_name:
        tck_file = os.path.join(prepath, str(sb_id), tck_path, tck)
        if os.path.exists(tck_file):
            fas = Fasciculus(tck_file)
            bundle = fas.get_data()

            """
            It happened that this bundle is in world coordinates and therefore we need to
            transform it into native image coordinates so that it is in the same coordinate
            space as the ``fa`` image.
            """

            bundle_native = transform_streamlines(bundle, np.linalg.inv(affine))

            """
            Show every streamline with an orientation color
            ===============================================

            This is the default option when you are using ``line`` or ``streamtube``.
            """

            renderer = window.Renderer()

            stream_actor = actor.line(bundle_native)

            # renderer.set_camera(position=(-176.42, 118.52, 128.20),
            #                     focal_point=(113.30, 128.31, 76.56),
            #                     view_up=(0.18, 0.00, 0.98))

            renderer.add(stream_actor)

            # Uncomment the line below to show to display the window
            window.show(renderer, size=(600, 600), reset_camera=False)
            # window.record(renderer, out_path='bundle1.png', size=(600, 600))

            """
            .. figure:: bundle1.png
               :align: center

               One orientation color for every streamline.

            You may wonder how we knew how to set the camera. This is very easy. You just
            need to run ``window.show`` once see how you want to see the object and then
            close the window and call the ``camera_info`` method which prints the position,
            focal point and view up vectors of the camera.
            """

            renderer.camera_info()

            """
            Show every point with a value from a volume with default colormap
            =================================================================

            Here we will need to input the ``fa`` map in ``streamtube`` or ``line``.
            """

            renderer.clear()
            stream_actor2 = actor.line(bundle_native, fa, linewidth=0.1)

            """
            We can also show the scalar bar.
            """

            bar = actor.scalar_bar(title="FA color coding")

            renderer.add(stream_actor2)
            renderer.add(bar)

            window.show(renderer, size=(600, 600), reset_camera=False)
            out_results_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects_testretest/new_results/'

            window.record(renderer, out_path=os.path.join(out_results_dir, '{}.png'.format(tck.split('.')[0])), size=(600, 600))

            # """
            # .. figure:: bundle2.png
            #    :align: center
            #
            #    Every point with a color from FA.
            #
            # Show every point with a value from a volume with your colormap
            # ==============================================================
            #
            # Here we will need to input the ``fa`` map in ``streamtube``
            # """
            #
            # renderer.clear()
            #
            # hue = (0.0, 0.0)  # red only
            # saturation = (0.0, 1.0)  # white to red
            #
            # lut_cmap = actor.colormap_lookup_table(hue_range=hue,
            #                                        saturation_range=saturation)
            #
            # stream_actor3 = actor.line(bundle_native, fa, linewidth=0.1,
            #                            lookup_colormap=lut_cmap)
            # bar2 = actor.scalar_bar(lut_cmap)
            #
            # renderer.add(stream_actor3)
            # renderer.add(bar2)
            #
            # window.show(renderer, size=(600, 600), reset_camera=False)
            # # window.record(renderer, out_path='bundle3.png', size=(600, 600))
            #
            # """
            # .. figure:: bundle3.png
            #    :align: center
            #
            #    Every point with a color from FA using a non default colormap.
            #
            #
            # Show every bundle with a specific color
            # ========================================
            #
            # You can have a bundle with a specific color. In this example, we are chosing
            # orange.
            # """
            #
            # renderer.clear()
            # stream_actor4 = actor.line(bundle_native, (1., 0.5, 0), linewidth=0.1)
            #
            # renderer.add(stream_actor4)
            #
            # window.show(renderer, size=(600, 600), reset_camera=False)
            # # window.record(renderer, out_path='bundle4.png', size=(600, 600))
            #
            # """
            # .. figure:: bundle4.png
            #    :align: center
            #
            #    Entire bundle with a specific color.
            #
            # Show every streamline of a bundle with a different color
            # ========================================================
            #
            # Let's make a colormap where every streamline of the bundle is colored by its
            # length.
            # """
            #
            # renderer.clear()
            #
            # from dipy.tracking.streamline import length
            #
            # lengths = length(bundle_native)
            #
            # hue = (0.5, 0.5)  # blue only
            # saturation = (0.0, 1.0)  # black to white
            #
            # lut_cmap = actor.colormap_lookup_table(
            #     scale_range=(lengths.min(), lengths.max()),
            #     hue_range=hue,
            #     saturation_range=saturation)
            #
            # stream_actor5 = actor.line(bundle_native, lengths, linewidth=0.1,
            #                            lookup_colormap=lut_cmap)
            #
            # renderer.add(stream_actor5)
            # bar3 = actor.scalar_bar(lut_cmap)
            #
            # renderer.add(bar3)
            #
            # window.show(renderer, size=(600, 600), reset_camera=False)
            # # window.record(renderer, out_path='bundle5.png', size=(600, 600))
            #
            # """
            # .. figure:: bundle5.png
            #    :align: center
            #    **Color every streamline by the length of the streamline **
            #
            #
            # Show every point of every streamline with a different color
            # ============================================================
            #
            # In this case in which we want to have a color per point and per streamline,
            # we can create a list of the colors to correspond to the list of streamlines
            # (bundles). Here in ``colors`` we will insert some random RGB colors.
            # """
            #
            # renderer.clear()
            #
            # colors = [np.random.rand(*streamline.shape) for streamline in bundle_native]
            #
            # stream_actor6 = actor.line(bundle_native, colors, linewidth=0.2)
            #
            # renderer.add(stream_actor6)
            #
            # window.show(renderer, size=(600, 600), reset_camera=False)
            # # window.record(renderer, out_path='bundle6.png', size=(600, 600))
            #
            # """
            # .. figure:: bundle6.png
            #    :align: center
            #
            #    Random colors per points per streamline.
            #
            # In summary, we showed that there are many useful ways for visualizing maps
            # on bundles.
            #
            # """
            #
