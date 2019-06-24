#!/usr/bin/env mayavi2
"""This script demonstrates how one can script Mayavi's core API to display
streamlines and an iso surface.
"""
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Copyright (c) 2005-2007, Enthought, Inc.
# License: BSD Style.

# Standard library imports
from os.path import join, abspath, dirname

# Enthought library imports
import mayavi
from mayavi.scripts import mayavi2
from mayavi.sources.vtk_xml_file_reader import VTKXMLFileReader
from mayavi.sources.vtk_file_reader import VTKFileReader
from mayavi.modules.streamline import Streamline


def setup_data(fname):
    """Given a VTK XML file name `fname`, this creates a mayavi2
    reader for it and adds it to the pipeline.  It returns the reader
    created.
    """
    r = VTKXMLFileReader()
    # r = VTKFileReader()
    r.initialize(fname)
    mayavi.add_source(r)
    return r


def streamline():
    """Sets up the mayavi pipeline for the visualization.
    """
    s = Streamline(streamline_type='line')
    mayavi.add_module(s)
    # s.stream_tracer.integration_direction = 'both'
    # s.seed.widget.center = 3.5, 0.625, 1.25
    # s.seed.widget.center = -9, 0.38, 1.25
    # s.module_manager.scalar_lut_manager.show_scalar_bar = True

@mayavi2.standalone
def main():
    mayavi.new_scene()

    data_dir = mayavi2.get_data_dir(dirname(abspath(__file__)))

    fname = join(data_dir, 'fire_ug.vtu')
    # fname = join(data_dir, 'vtk_test.vtk')
    r = setup_data(fname)
    # streamline()


if __name__ == '__main__':
    main()
