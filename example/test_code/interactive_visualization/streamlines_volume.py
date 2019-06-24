#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from os.path import join, abspath, dirname
import mayavi
from mayavi import mlab
from traits.api import Instance
from mayavi.core.ui.api import MlabSceneModel
from mayavi.scripts import mayavi2
from mayavi.modules.streamline import Streamline
from mayavi.modules.api import Outline, ScalarCutPlane, Streamline
from mayavi.modules.image_plane_widget import ImagePlaneWidget
from mayavi.core.api import Engine
from mayavi.sources.vtk_file_reader import VTKFileReader
from mayavi.sources.vtk_xml_file_reader import VTKXMLFileReader
from mayavi.core.ui.engine_view import EngineView
from pyface.api import GUI
from mayavi.tools.pipeline import streamline


e = Engine()
e.start()
# ev = EngineView(engine=e)
# ui = ev.edit_traits()
scene = e.new_scene()
# scene = Instance(MlabSceneModel, ())
data_dir = mayavi2.get_data_dir(dirname(abspath(__file__)))
# fname = join(data_dir, '1M_20_01_20dynamic250_SD_Stream_occipital5.vtk')
# r = VTKFileReader()
fname = join(data_dir, 'fire_ug.vtu')
r = VTKXMLFileReader()
r.initialize(fname)
e.add_source(r)
s = Streamline(streamline_type='line')
# s.seed.visible = True
# s.remove()
# s.stop()
# e.add_module(s)

streamline(r, integration_direction='both', seed_visible=True)
mlab.view()
# gui = GUI()
# gui.start_event_loop()
mlab.show()
