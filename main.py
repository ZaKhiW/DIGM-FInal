"""
main.py -  Floor Plan Generator

File containing the entire code string for the scene. This file acts as thr main file 
containing the entirety of the code meant for the Floor Plan Generator.

Assembles complete Floor Plan Generator.
"""

import maya.cmds as cmds
import random
import json

## Floor Plan Generator ##

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

def save_settings(filepath, settings):
    with open(filepath, "w") as f:
        json.dump(settings, f, indent=4)


def load_settings(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

## FloorPlanGenerator UI ##

class FloorPlanGeneratorUI:

    WINDOW_NAME = "FloorPlanGeneratorUI"

    def __init__(self):
        self.build_ui()

    def build_ui(self):

        if cmds.window(self.WINDOW_NAME, exists=True):
            cmds.deleteUI(self.WINDOW_NAME)

        cmds.window(
            self.WINDOW_NAME,
            title="Procedural Floor Plan Generator",
            widthHeight=(350, 500)
        )

        cmds.columnLayout(
            adjustableColumn=True,
            rowSpacing=5
        )

        self.width_field = cmds.intFieldGrp(
            label="Width",
            value1=60
        )

        self.depth_field = cmds.intFieldGrp(
            label="Depth",
            value1=60
        )

        self.room_count_field = cmds.intFieldGrp(
            label="Room Count",
            value1=12
        )

        self.min_room_field = cmds.intFieldGrp(
            label="Min Room Size",
            value1=5
        )

        self.max_room_field = cmds.intFieldGrp(
            label="Max Room Size",
            value1=14
        )

        self.wall_height_field = cmds.floatFieldGrp(
            label="Wall Height",
            value1=10
        )

        self.wall_thickness_field = cmds.floatFieldGrp(
            label="Wall Thickness",
            value1=0.6
        )

        self.hallway_field = cmds.floatFieldGrp(
            label="Hallway Chance",
            value1=0.5
        )

        cmds.separator(height=15)

        cmds.button(
            label="Generate Floor Plan",
            height=40,
            command=lambda *_: self.generate()
        )

        cmds.button(
            label="Save Settings",
            height=30,
            command=lambda *_: self.save_json()
        )

        cmds.button(
            label="Load Settings",
            height=30,
            command=lambda *_: self.load_json()
        )

        cmds.showWindow(self.WINDOW_NAME)

    def get_settings(self):

        return {

            "width":
                cmds.intFieldGrp(
                    self.width_field,
                    q=True,
                    value1=True
                ),

            "depth":
                cmds.intFieldGrp(
                    self.depth_field,
                    q=True,
                    value1=True
                ),

            "room_count":
                cmds.intFieldGrp(
                    self.room_count_field,
                    q=True,
                    value1=True
                ),

            "min_room":
                cmds.intFieldGrp(
                    self.min_room_field,
                    q=True,
                    value1=True
                ),

            "max_room":
                cmds.intFieldGrp(
                    self.max_room_field,
                    q=True,
                    value1=True
                ),

            "wall_height":
                cmds.floatFieldGrp(
                    self.wall_height_field,
                    q=True,
                    value1=True
                ),

            "wall_thickness":
                cmds.floatFieldGrp(
                    self.wall_thickness_field,
                    q=True,
                    value1=True
                ),

            "hallway_chance":
                cmds.floatFieldGrp(
                    self.hallway_field,
                    q=True,
                    value1=True
                )
        }

    def generate(self):

        settings = self.get_settings()

        gen = FloorPlanGenerator(
            width=settings["width"],
            depth=settings["depth"],
            room_count=settings["room_count"],
            min_room=settings["min_room"],
            max_room=settings["max_room"],
            wall_height=settings["wall_height"],
            wall_thickness=settings["wall_thickness"],
            hallway_chance=settings["hallway_chance"],
            seed=random.randint(0, 9999)
        )

        gen.build()

## JSON ##    

    def save_json(self):

        filepath = cmds.fileDialog2(
            fileMode=0,
            caption="Save Floor Plan Settings",
            fileFilter="JSON Files (*.json)"
        )

        if not filepath:
            return

        save_settings(
            filepath[0],
            self.get_settings()
        )

        print("Settings saved:", filepath[0])

    def load_json(self):

        filepath = cmds.fileDialog2(
            fileMode=1,
            caption="Load Floor Plan Settings",
            fileFilter="JSON Files (*.json)"
        )

        if not filepath:
            return

        settings = load_settings(filepath[0])

        cmds.intFieldGrp(
            self.width_field,
            e=True,
            value1=settings["width"]
        )

        cmds.intFieldGrp(
            self.depth_field,
            e=True,
            value1=settings["depth"]
        )

        cmds.intFieldGrp(
            self.room_count_field,
            e=True,
            value1=settings["room_count"]
        )

        cmds.intFieldGrp(
            self.min_room_field,
            e=True,
            value1=settings["min_room"]
        )

        cmds.intFieldGrp(
            self.max_room_field,
            e=True,
            value1=settings["max_room"]
        )

        cmds.floatFieldGrp(
            self.wall_height_field,
            e=True,
            value1=settings["wall_height"]
        )

        cmds.floatFieldGrp(
            self.wall_thickness_field,
            e=True,
            value1=settings["wall_thickness"]
        )

        cmds.floatFieldGrp(
            self.hallway_field,
            e=True,
            value1=settings["hallway_chance"]
        )

        print("Settings loaded:", filepath[0])

## UI ##

FloorPlanGeneratorUI()


