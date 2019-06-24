#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# os.environ['HDF5_DISABLE_VERSION_CHECK'] = '2'
import vtk
import numpy as np
import nibabel as nib
import numpy.linalg as npl
from nibabel.affines import apply_affine
from scipy.spatial.distance import cdist

from dipy.viz import actor, window, ui
from dipy.viz import read_viz_icons, fetch_viz_icons
from dipy.tracking.streamline import set_number_of_points
import nibabel.streamlines.array_sequence as nibas

from pyfat.viz.custom_interactor import MouseInteractorStylePP
from pyfat.algorithm.fiber_selection import select_by_vol_roi
from pyfat.io.save import save_tck
from pyfat.core.dataobject import Fasciculus


subjects_dir = '/home/brain/workingdir/data/dwi/hcp/preprocessed/response_dhollander/subjects'

tck_name = ['lvis1_template_centroids.tck', 'lvis2_template_centroids.tck',
            'lvis3_template_centroids.tck', 'lvis4_template_centroids.tck']
#
# tck_name = ['rvis1_template_centroids.tck', 'rvis2_template_centroids.tck',
#             'rvis3_template_centroids.tck', 'rvis4_template_centroids.tck']


vol_name = 'T1w_acpc_dc_restore_brain1.25.nii.gz'

results_dir = 'Diffusion/tractography/Det/new_results'

sessid = ['101309']
# sessid = ['101915']
for i in xrange(len(sessid)):
    for j in xrange(len(tck_name)):
        print 'subjects_id: ', sessid[i]
        print 'fas name: ', tck_name[j]
        vol_file = os.path.join(subjects_dir, sessid[i], vol_name)
        vol = nib.load(vol_file)
        fa_file = os.path.join(subjects_dir, sessid[i], 'Diffusion/metrics/fa.nii.gz')
        img = nib.load(fa_file)
        fa = img.get_data()
        affine = img.affine
        fa = apply_affine(npl.inv(affine), fa)

        tck_path = os.path.join(subjects_dir, sessid[i], results_dir, tck_name[j])

        if not os.path.exists(tck_path):
            continue

        # fib = nib.streamlines.tck.TckFile.load(tck_path)
        fas = Fasciculus(tck_path)
        streamlines = fas.get_data()
        # streamlines = fib.streamlines
        print 'number of fib:', len(streamlines)

        # create a rendering renderer
        ren = window.Renderer()
        stream_actor = actor.line(streamlines)

        ####################################################
        # roi_vis = nib.load(roi_vis)


        def set_viz_roi(roi_img, mask=False):
            roi_data = roi_img.get_data()
            if mask:
                roi_data[roi_data > 0] = 1
            label = list(set(roi_data[roi_data.nonzero()]))
            roi_list = []
            for i in xrange(len(label)):
                roi = np.zeros(roi_data.shape)
                roi[roi_data == label[i]] = i + 1
                roi_list.append(roi)

            return roi_list, roi_img.affine


        def create_roi_actor(roi_list, affine, opacity=0.8):
            roi_actor_list = []
            for i in xrange(len(roi_list)):
                random = np.random.RandomState(i)
                color = random.uniform(0., 1., size=3)
                print color
                i_actor = actor.contour_from_roi(roi_list[i], affine=affine, color=color, opacity=opacity)
                roi_actor_list.append(i_actor)

            return roi_actor_list


        # roi_viz, roi_viz_affine = set_viz_roi(roi_vis)
        # roi_viz_actor = create_roi_actor(roi_viz, roi_viz_affine)

        stream_init_actor = actor.line(streamlines)  # , (0.0, 1.0, 0.0))

        def create_image_actor(vol, opacity=0.6):
            data = vol.get_data()
            shape = vol.shape
            affine = vol.affine

            image_actor_z = actor.slicer(data, affine)
            slicer_opacity = opacity
            image_actor_z.opacity(slicer_opacity)
            image_actor_x = image_actor_z.copy()
            image_actor_x.opacity(slicer_opacity)
            x_midpoint = int(np.round(shape[0] / 2))
            image_actor_x.display_extent(x_midpoint,
                                         x_midpoint, 0,
                                         shape[1] - 1,
                                         0,
                                         shape[2] - 1)

            image_actor_y = image_actor_z.copy()
            image_actor_y.opacity(slicer_opacity)
            y_midpoint = int(np.round(shape[1] / 2))
            image_actor_y.display_extent(0,
                                         shape[0] - 1,
                                         y_midpoint,
                                         y_midpoint,
                                         0,
                                         shape[2] - 1)

            return image_actor_x, image_actor_y, image_actor_z


        def createCubeActor(bounds=None, size=None, center=None, color=None, opacity=0.8):
            cube = window.vtk.vtkCubeSource()
            if bounds is not None:
                cube.SetBounds(bounds)
            if size is not None:
                cube.SetXLength(size[0])
                cube.SetYLength(size[1])
                cube.SetZLength(size[2])
            if center is not None:
                cube.SetCenter(*center)

            cube_mapper = window.vtk.vtkPolyDataMapper()
            cube_mapper.SetInputConnection(cube.GetOutputPort())
            cube_actor = window.vtk.vtkActor()
            cube_actor.SetMapper(cube_mapper)

            if color is not None:
                cube_actor.GetProperty().SetColor(color)
            if opacity is not None:
                cube_actor.GetProperty().SetOpacity(opacity)
            return cube_actor


        image_actor_x, image_actor_y, image_actor_z = create_image_actor(vol)
        # assign actor to the renderer
        ren.add(stream_actor)

        # for act_viz in roi_viz_actor:
        #     ren.add(act_viz)
        #########################################
        ren.add(image_actor_z)
        ren.add(image_actor_x)
        ren.add(image_actor_y)
        show_m = window.ShowManager(ren,
                                    size=(1200, 900))  # , interactor_style=MouseInteractorStylePP(ren, roi_viz_actor))
        show_m.initialize()


        def line_slider(shape, opacity=0.6):
            line_slider_z = ui.LineSlider2D(min_value=0,
                                            max_value=shape[2] - 1,
                                            initial_value=shape[2] / 2,
                                            text_template="{value:.0f}",
                                            length=140)

            line_slider_x = ui.LineSlider2D(min_value=0,
                                            max_value=shape[0] - 1,
                                            initial_value=shape[0] / 2,
                                            text_template="{value:.0f}",
                                            length=140)

            line_slider_y = ui.LineSlider2D(min_value=0,
                                            max_value=shape[1] - 1,
                                            initial_value=shape[1] / 2,
                                            text_template="{value:.0f}",
                                            length=140)

            opacity_slider = ui.LineSlider2D(min_value=0.0,
                                             max_value=1.0,
                                             initial_value=opacity,
                                             length=140)

            return line_slider_x, line_slider_y, line_slider_z, opacity_slider


        line_slider_x, line_slider_y, line_slider_z, opacity_slider = line_slider(vol.shape)
        shape = vol.shape


        def change_slice_z(slider):
            z = int(np.round(slider.value))
            image_actor_z.display_extent(0, shape[0] - 1, 0, shape[1] - 1, z, z)


        def change_slice_x(slider):
            x = int(np.round(slider.value))
            image_actor_x.display_extent(x, x, 0, shape[1] - 1, 0, shape[2] - 1)


        def change_slice_y(slider):
            y = int(np.round(slider.value))
            image_actor_y.display_extent(0, shape[0] - 1, y, y, 0, shape[2] - 1)


        def change_opacity(slider):
            slicer_opacity = slider.value
            image_actor_z.opacity(slicer_opacity)
            image_actor_x.opacity(slicer_opacity)
            image_actor_y.opacity(slicer_opacity)


        line_slider_z.on_change = change_slice_z
        line_slider_x.on_change = change_slice_x
        line_slider_y.on_change = change_slice_y
        opacity_slider.on_change = change_opacity

        """
        We'll also create text labels to identify the sliders.
        """


        def build_label(text):
            label = ui.TextBlock2D()
            label.message = text
            label.font_size = 18
            label.font_family = 'Arial'
            label.justification = 'left'
            label.bold = False
            label.italic = False
            label.shadow = False
            label.actor.GetTextProperty().SetBackgroundColor(0, 0, 0)
            label.actor.GetTextProperty().SetBackgroundOpacity(0.0)
            label.color = (1, 1, 1)

            return label


        line_slider_label_z = build_label(text="Z Slice")
        line_slider_label_x = build_label(text="X Slice")
        line_slider_label_y = build_label(text="Y Slice")
        opacity_slider_label = build_label(text="Opacity")


        def create_panel(line_slider_x, line_slider_label_x, line_slider_y, line_slider_label_y,
                         line_slider_z, line_slider_label_z, opacity_slider, opacity_slider_label):
            """
            Now we will create a ``panel`` to contain the sliders and labels.
            """
            panel = ui.Panel2D(size=(300, 200),
                               color=(1, 1, 1),
                               opacity=0.1,
                               align="right")
            panel.center = (150, 100)

            panel.add_element(line_slider_label_x, (0.1, 0.75))
            panel.add_element(line_slider_x, (0.38, 0.75))
            panel.add_element(line_slider_label_y, (0.1, 0.55))
            panel.add_element(line_slider_y, (0.38, 0.55))
            panel.add_element(line_slider_label_z, (0.1, 0.35))
            panel.add_element(line_slider_z, (0.38, 0.35))
            panel.add_element(opacity_slider_label, (0.1, 0.15))
            panel.add_element(opacity_slider, (0.38, 0.15))

            return panel


        panel = create_panel(line_slider_x, line_slider_label_x, line_slider_y, line_slider_label_y,
                             line_slider_z, line_slider_label_z, opacity_slider, opacity_slider_label)
        show_m.ren.add(panel)
        global size
        size = ren.GetSize()


        def win_callback(obj, event):
            global size
            if size != obj.GetSize():
                size_old = size
                size = obj.GetSize()
                size_change = [size[0] - size_old[0], 0]
                panel.re_align(size_change)


        ################################
        # Call back function
        def _computeFib(stream, spherewidget):
            stream = np.array([f for f in set_number_of_points(stream, 20)])
            center = np.array([spherewidget.GetCenter()])
            dist = np.array([cdist(stream[i], center).min() for i in xrange(len(stream))])
            new_stream = stream[dist <= spherewidget.GetRadius()]
            index = dist <= sphereWidget.GetRadius()

            return new_stream, index


        def computeFibCallback(obj, event):
            global streamlines, stream_actor
            new_f, _ = _computeFib(streamlines, obj)
            try:
                ren.RemoveActor(stream_actor)
                ren.RemoveActor(stream_init_actor)
                # random = np.random.RandomState()
                # color = np.random.uniform(0., 1., size=3)
                stream_actor = actor.line(new_f, (1., 1., 1.))
                ren.add(stream_actor)
            except:
                pass


        # enable user interface interactor
        iren = show_m.iren
        renWin = show_m.window
        renWin.AddRenderer(ren)


        # A Sphere widget
        def create_sphereWidget(center=(3.98, -30.94, 9.16), radius=5, opacity=0.8):
            sphereWidget = vtk.vtkSphereWidget()
            sphereWidget.SetCenter(center)
            sphereWidget.SetRadius(radius)
            sphereWidget.GetSphereProperty().SetOpacity(opacity)
            sphereWidget.SetRepresentationToSurface()
            # sphereWidget.SetKeyPressActivationValue('k')  # By default, the key press activation value is 'i'.
            # sphereWidget.On()
            return sphereWidget


        center_x = image_actor_x.GetSliceNumber()
        center_y = image_actor_y.GetSliceNumber()
        center_z = image_actor_z.GetSliceNumber()
        center = vol.affine.dot([center_x, center_y, center_z, 1])[:3]
        print center
        sphereWidget = create_sphereWidget(center=center)
        sphereWidget.SetInteractor(iren)
        # Connect the event to a function
        # sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
        ######################################
        ######################################

        """
        Buttons
        =======

        We first fetch the icons required for making the buttons.
        """

        fetch_viz_icons()

        """
        Add the icon filenames to a dict.
        """

        icon_file = []
        icon_file.append((['save'], read_viz_icons(fname='floppy-disk.png')))
        icon_file.append((['savefinish'], read_viz_icons(fname='checkmark.png')))

        """
        Create a button through our API.
        """

        button_example = ui.Button2D(icon_fnames=icon_file)

        """
        We now add some click listeners.
        """


        # def left_mouse_button_click(i_ren, obj, button):
        #     print("Left Button Clicked")
        #
        #
        # def left_mouse_button_drag(i_ren, obj, button):
        #     print ("Left Button Dragged")

        def modify_left_button_callback(i_ren, obj, button):
            print button.current_icon_id
            print button.current_icon_name
            if button.current_icon_id == 0:
                new_f, index = _computeFib(streamlines, sphereWidget)
                fas.set_data(nibas.ArraySequence(new_f))
                if 'fasciculus_id' in fas.get_header().keys():
                    del fas.get_header()['fasciculus_id']
                    # ids = {'fasciculus_id': None}
                    # fas.get_header()['fasciculus_id'] = list(fas.get_header()['fasciculus_id'][index])
                    # fas.update_header(ids)
                fas.save2tck(os.path.join(file_select_menu.current_directory, '%s.tck') % text.message)
            if button.current_icon_id == 1:
                pass

            button.next_icon()
            i_ren.force_render()


        print __file__
        print os.getcwd()
        # button_example.on_left_mouse_button_drag = left_mouse_button_drag
        # button_example.on_left_mouse_button_pressed = left_mouse_button_click
        button_example.on_left_mouse_button_pressed = modify_left_button_callback

        # def right_mouse_button_drag(i_ren, obj, button):
        #     print("Right Button Dragged")
        #
        #
        # def right_mouse_button_click(i_ren, obj, button):
        #     print ("Right Button Clicked")
        #
        #
        # button_example.on_right_mouse_button_drag = right_mouse_button_drag
        # button_example.on_right_mouse_button_pressed = right_mouse_button_click


        icon_files = []
        icon_files.append((['play'], read_viz_icons(fname='play3.png')))
        icon_files.append((['stop'], read_viz_icons(fname='stop2.png')))

        """
        Let's have another button.
        """

        second_button_example = ui.Button2D(icon_fnames=icon_files)

        """
        This time, we will call the built in `next_icon` method
        via a callback that is triggered on left click.
        """


        def modify_button_callback(i_ren, obj, button):
            print button.current_icon_id
            print button.current_icon_name
            if button.current_icon_id == 0:
                # ren.RemoveActor(stream_init_actor)
                sphereWidget.AddObserver("InteractionEvent", computeFibCallback)
            if button.current_icon_id == 1:
                ren.RemoveActor(stream_actor)
                sphereWidget.RemoveAllObservers()
                ren.add(stream_init_actor)

            button.next_icon()
            i_ren.force_render()


        second_button_example.on_left_mouse_button_pressed = modify_button_callback

        """
        Panels
        ======

        Simply create a panel and add elements to it.
        """

        panel2 = ui.Panel2D(size=(300, 150), color=(1, 1, 1),
                            align="right")
        panel2.center = (150, 275)
        panel2.add_element(button_example, (0.2, 0.2))
        panel2.add_element(second_button_example, (0.6, 0.2))

        # panel2.add_element(second_button_example, (480, 100))

        """
        TextBox
        =======
        """

        text = ui.TextBox2D(height=3, width=10)
        panel2.add_element(text, (0.2, 0.6))


        # def key_press(i_ren, obj, textbox_object):
        #     """ Key press handler for textbox
        #
        #     Parameters
        #     ----------
        #     i_ren: :class:`CustomInteractorStyle`
        #     obj: :class:`vtkActor`
        #         The picked actor
        #     textbox_object: :class:`TextBox2D`
        #
        #     """
        #     key = i_ren.event.key
        #     print key
        #     is_done = textbox_object.handle_character(key)
        #     print is_done
        #     if is_done:
        #         i_ren.remove_active_prop(textbox_object.actor.get_actor())
        #         print textbox_object.text
        #
        #     i_ren.force_render()


        # text.on_key_press = key_press

        """
        2D File Select Menu
        ==============
        """

        current_directory = os.path.join(subjects_dir, sessid[i], results_dir)
        if not os.path.isdir(current_directory):
            os.makedirs(current_directory)
        file_select_menu = ui.FileMenu2D(size=(300, 500),
                                         position=(0, 350),
                                         font_size=16,
                                         extensions=["tck", "gz"],
                                         directory_path=current_directory)
        # values = os.listdir(current_directory)
        # file_select_menu = ui.ListBox2D(values=values, position=(10, 300), size=(300, 200),
        #                                 multiselection=False)

        print file_select_menu.directory_contents
        print file_select_menu.current_directory


        # def left_button_clicked(i_ren, obj, file_select_text):
        #     """ A callback to handle left click for this UI element.
        #
        #     Parameters
        #     ----------
        #     i_ren: :class:`CustomInteractorStyle`
        #     obj: :class:`vtkActor`
        #         The picked actor
        #     file_select_text: :class:`FileSelectMenuText2D`
        #
        #     """
        #     print "testtestestestestestestestestest"
        #
        #     if file_select_text.file_type == "directory":
        #         file_select_text.file_select.select_file(file_name="")
        #         file_select_text.file_select.window_offset = 0
        #         file_select_text.file_select.current_directory = os.path.abspath(
        #             os.path.join(file_select_text.file_select.current_directory,
        #                          file_select_text.text_actor.message))
        #         file_select_text.file_select.window = 0
        #         file_select_text.file_select.fill_text_actors()
        #         print "----------------------"
        #     else:
        #         file_select_text.file_select.select_file(
        #             file_name=file_select_text.file_name)
        #         file_select_text.file_select.fill_text_actors()
        #         file_select_text.mark_selected()
        #         print "+++++++++++++++++++++++"
        #         data_path = os.path.join(file_select_text.file_select.current_directory, file_select_text.file_name)
        #         suffix = os.path.split(data_path)[-1].split('.')[-1]
        #         print
        #         if suffix == 'tck':
        #             fibs = nib.streamlines.tck.TckFile.load(data_path)
        #             if str(os.path.split(data_path)[-1][4]).isdigit():
        #                 color_seed = int(os.path.split(data_path)[-1][4]) + 1
        #                 random = np.random.RandomState(color_seed)
        #                 color = random.uniform(0., 1., size=3)
        #                 ac = actor.line(fibs.streamlines, colors=color)
        #             else:
        #                 ac = actor.line(fibs.streamlines)
        #             ren.add(ac)
        #         if suffix == 'gz':
        #             img = nib.load(data_path)
        #             # random = np.random.RandomState(i)
        #             color = np.random.uniform(0., 1., size=3)
        #             print color
        #             im = actor.contour_from_roi(img.get_data(), affine=img.affine, color=color, opacity=0.8)
        #             # im = actor.contour_from_roi(img.get_data(), affine=img.affine)
        #             ren.add(im)
        #
        #     i_ren.force_render()
        #     i_ren.event.abort()  # Stop propagating the event.


        def display_element():
            example = file_select_menu.listbox.selected
            for name in example:
                data_path = os.path.join(file_select_menu.current_directory, name)
                if not os.path.isfile(data_path):
                    continue
                suffix = os.path.split(data_path)[-1].split('.')[-1]
                if suffix == 'tck':
                    fibs = nib.streamlines.tck.TckFile.load(data_path)
                    # if str(os.path.split(data_path)[-1][4]).isdigit():
                    #     color_seed = int(os.path.split(data_path)[-1][4]) + 1
                    #     random = np.random.RandomState(color_seed)
                    #     color = random.uniform(0., 1., size=3)
                    #     ac = actor.line(fibs.streamlines, colors=color)
                    # else:
                    #     ac = actor.line(fibs.streamlines)
                    # ren.add(ac)

                    from dipy.tracking.streamline import transform_streamlines

                    fibss = fibs.streamlines

                    hue = (0.0, 0.0)  # red only
                    saturation = (0.0, 1.0)  # white to red

                    lut_cmap = actor.colormap_lookup_table(hue_range=hue,
                                                           saturation_range=saturation)

                    stream_actor3 = actor.line(fibss, fa, linewidth=0.1)#,
                                               # lookup_colormap=lut_cmap)
                    # bar2 = actor.scalar_bar(lut_cmap)
                    bar = actor.scalar_bar()

                    ren.add(stream_actor3)
                    ren.add(bar)

                if suffix == 'gz':
                    img = nib.load(data_path)
                    # random = np.random.RandomState(i)
                    color = np.random.uniform(0., 1., size=3)
                    print color
                    im = actor.contour_from_roi(img.get_data(), affine=img.affine, color=color, opacity=0.8)
                    # im = actor.contour_from_roi(img.get_data(), affine=img.affine)
                    ren.add(im)

            # ren.force_render()
            # ren.event.abort()



            print example
            print file_select_menu.get_directory_names()
            print file_select_menu.current_directory
            print os.path.exists(file_select_menu.current_directory)
            # example.on_left_mouse_button_clicked = left_button_clicked

        file_select_menu.listbox.on_change = display_element

        # for text_actor in file_select_menu.listbox.slots:
        #     text_actor.left_button_state = "pressing"
        #     text_actor.on_left_mouse_button_clicked = left_button_clicked
            # text_actor.handle_events(text_actor)
        # file_select_menu.listbox.on_left_mouse_button_clicked = left_button_clicked

        show_m.ren.add(panel2)
        # show_m.ren.add(text)
        # show_m.ren.add(line_slider_c)
        # show_m.ren.add(disk_slider)
        show_m.ren.add(file_select_menu)
        show_m.ren.reset_camera()
        show_m.ren.azimuth(30)
        ###################################################

        show_m.initialize()
        ren.zoom(1.5)
        ren.reset_clipping_range()
        show_m.add_window_callback(win_callback)
        show_m.render()
        show_m.start()
