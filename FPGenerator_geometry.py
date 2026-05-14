"""
FPGenerator_geometry.py - Geometry builders for Floor Plan Generator.

Each function creates one type of floor plan element and returns the MAYA node
name(s). No materials or scene logic included.

Usage:
  Import FPGenerator_geometry as geo
  geo.create_wall()

"""

import maya.cmds as cmds
