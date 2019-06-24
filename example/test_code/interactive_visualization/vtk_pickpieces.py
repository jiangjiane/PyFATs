#!/usr/bin/python

# This example creates a board with a flat surface at z=0
# and a number of pieces that may interactively be moved
# around the board by the mouse.
#
# Dov Grobgeld <dov.grobgeld@gmail.com>
# This example is released under the same BSD licence as vtk.

import vtk


# Inherit an interactor and override the button events in order
# to be able to pick up pieces from the board.
class MouseInteractor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, renderer, renWin, pieces):
        super(MouseInteractor, self).__init__()
        # The following three events are involved in the pieces interaction.
        self.AddObserver('RightButtonPressEvent', self.OnRightButtonDown)
        self.AddObserver('RightButtonReleaseEvent', self.OnRightButtonRelease)
        self.AddObserver('MouseMoveEvent', self.OnMouseMove)

        # Remember data we need for the interaction
        self.renderer = renderer
        self.chosenPiece = None
        self.renWin = renWin
        self.pieces = pieces

    def DisplayToWorld(self, XYZ):
        """Translate a display XYZ coordinate to a world XYZ coordinate"""
        worldPt = [0, 0, 0, 0]
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(self.renderer,
                                                        XYZ[0], XYZ[1], XYZ[2],
                                                        worldPt)
        return worldPt[0] / worldPt[3], worldPt[1] / worldPt[3], worldPt[2] / worldPt[3]

    def WorldZToDisplayZ(self, displayXY, worldZ=0):
        """Given a display coordinate displayXY and a worldZ coordinate,
        return the corresponding displayZ coordinate"""
        wzNear = self.DisplayToWorld(list(displayXY) + [0])[2]
        wzFar = self.DisplayToWorld(list(displayXY) + [1])[2]
        return (worldZ - wzNear) / (wzFar - wzNear)

    def OnRightButtonRelease(self, obj, eventType):
        # When the right button is released, we stop the interaction
        self.chosenPiece = None

        # Call parent interaction
        vtk.vtkInteractorStyleTrackballCamera.OnRightButtonUp(self)

    def OnRightButtonDown(self, obj, eventType):
        # The rightbutton is used to pick up the piece.

        # Get the display mouse event position
        clickPos = self.GetInteractor().GetEventPosition()

        # Use a picker to see which actor is under the mouse
        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.renderer)
        actor = picker.GetActor()

        # Is this a piece that we should interact with?
        if actor in self.pieces:
            # Yes! Remember it.
            self.chosenPiece = actor

            # Get the intersection of the click pos in our board plane.
            mouseDisplayZ = self.WorldZToDisplayZ(clickPos, worldZ=0)

            # Get the board xy coordinate of the picked point
            self.worldPickXY = self.DisplayToWorld(list(clickPos) + [mouseDisplayZ])[0:2]
        # Call parent interaction
        vtk.vtkInteractorStyleTrackballCamera.OnRightButtonDown(self)

    def OnMouseMove(self, obj, eventType):
        # Translate a choosen piece
        if self.chosenPiece is not None:
            # Redo the same calculation as during OnRightButtonDown
            mousePos = self.GetInteractor().GetEventPosition()
            mouseDisplayZ = self.WorldZToDisplayZ(mousePos)
            worldMouseXY = self.DisplayToWorld(list(mousePos) + [mouseDisplayZ])[0:2]

            # Calculate the xy movement
            dx = worldMouseXY[0] - self.worldPickXY[0]
            dy = worldMouseXY[1] - self.worldPickXY[1]

            # Remember the new reference coordinate
            self.worldPickXY = worldMouseXY

            # Shift the choosen piece in the xy plane
            x, y, z = self.chosenPiece.GetPosition()
            self.chosenPiece.SetPosition(x + dx, y + dy, z)

            # Request a redraw
            self.renWin.Render()
        else:
            vtk.vtkInteractorStyleTrackballCamera.OnMouseMove(self)
