"""
main.py -  Floor Plan Generator

File containing the entire code string for the scene. This file acts as thr main file 
containing the entirety of the code meant for the Floor Plan Generator.

Assembles complete Floor Plan Generator.
"""

import os
import sys
import maya.cmds as cmds


class FloorPlanGenerator:
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

        if seed is not None:
            random.seed(seed)

        self.rooms = []

    def clear_scene(self):
        objs = cmds.ls("floorGen_*")
        if objs:
            cmds.delete(objs)

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

    def room_overlaps(self, x, z, w, d):
        for rx, rz, rw, rd in self.rooms:
            if (
                abs(x - rx) < (w + rw) / 2 + 1 and
                abs(z - rz) < (d + rd) / 2 + 1
            ):
                return True
        return False

    def generate_rooms(self):
        attempts = 0

        while len(self.rooms) < self.room_count and attempts < 500:
            w = random.randint(self.min_room, self.max_room)
            d = random.randint(self.min_room, self.max_room)

            x = random.uniform(
                -self.width/2 + w/2,
                self.width/2 - w/2
            )

            z = random.uniform(
                -self.depth/2 + d/2,
                self.depth/2 - d/2
            )

            if not self.room_overlaps(x, z, w, d):
                self.rooms.append((x, z, w, d))

            attempts += 1

    def build_room(self, x, z, w, d):
        t = self.wall_thickness

        # Top
        self.create_wall(x, z + d/2, w, t)

        # Bottom
        self.create_wall(x, z - d/2, w, t)

        # Left
        self.create_wall(x - w/2, z, t, d)

        # Right
        self.create_wall(x + w/2, z, t, d)

    def generate_hallways(self):
        for i in range(len(self.rooms)-1):
            if random.random() < self.hallway_chance:
                x1, z1, _, _ = self.rooms[i]
                x2, z2, _, _ = self.rooms[i+1]

                midx = (x1 + x2) / 2
                midz = (z1 + z2) / 2

                self.create_wall(
                    midx,
                    midz,
                    abs(x1-x2)+2,
                    self.wall_thickness
                )

    def build(self):
        self.clear_scene()
        self.create_floor()
        self.generate_rooms()

        for room in self.rooms:
            self.build_room(*room)

        self.generate_hallways()


gen = FloorPlanGenerator(
    width=60,
    depth=60,
    room_count=12,
    min_room=5,
    max_room=14,
    wall_height=10,
    wall_thickness=0.6,
    hallway_chance=0.5,
    seed=random.randint(0, 9999)
)

gen.build()
