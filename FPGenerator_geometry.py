"""
FPGenerator_geometry.py - Geometry builders for Floor Plan Generator.

Each function creates one type of floor plan element and returns the MAYA node
name(s). No materials or scene logic included.

Usage:
  Import FPGenerator_geometry as geo
  geo.create_wall()
  geo.create_floor()

"""

import maya.cmds as cmds

def __init__(self,
                 width=40,
                 depth=40,
                 room_count=8,
                 min_room=6,
                 max_room=15,
                 wall_height=8,
                 wall_thickness=0.5,
                 hallway_chance=0.3,
                 seed=None):

 self.width = width
        self.depth = depth
        self.room_count = room_count
        self.min_room = min_room
        self.max_room = max_room
        self.wall_height = wall_height
        self.wall_thickness = wall_thickness
        self.hallway_chance = hallway_chance

 def create_wall(self, x, z, sx, sz):
        wall = cmds.polyCube(
            w=sx,
            h=self.wall_height,
            d=sz,
            name="floorGen_wall#"
        )[0]

        cmds.move(
            x,
            self.wall_height / 2,
            z,
            wall
        )

def create_floor(self):
        floor = cmds.polyPlane(
            w=self.width,
            h=self.depth,
            name="floorGen_base"
        )[0]

        cmds.move(0, 0, 0, floor)
