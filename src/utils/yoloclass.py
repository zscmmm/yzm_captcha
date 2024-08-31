from typing import List
import json
from pathlib import Path

class Shape():
    def __init__(self, points = None):
        # points = [[x1,y1, x2,y2], [x1,y1, x2,y2], ...]
        # 必须是上面的形式
        self.label = ""
        if not points:
            self.points = []
        else:
            if not isinstance(points, list) and len(points) == 4:
                raise Exception("points must be list and len(points) == 4")
            self.points = [[float(points[0]), float(points[1])], [float(points[2]), float(points[3])]]
        self.group_id = None
        self.description = ""
        self.shape_type = "rectangle"
        self.flags = {}
        self.text = ""
        self.mask = None
    def set_group_id(self, group_id):
        assert isinstance(group_id, int), "group_id must be int"
        self.group_id = group_id
    def set_label(self, label):
        self.label = label
    def set_points(self, points):
        if not isinstance(points, list) and len(points)  == 4:
            raise Exception("points must be list and len(points) == 4")
        self.points = [[float(points[0]), float(points[1])], [float(points[2]), float(points[3])]]

    def set_shape_type(self, shape_type):
        self.shape_type = shape_type
    def set_description(self, description):
        self.description = description
    def set_text(self, text):
        self.text = text
    def to_dict(self):
        return self.__dict__
    


class  Labelme():
    def __init__(self):
        self.version = "5.4.1"
        self.flags =  {}
        self.shapes = []
        self.imagePath = ""
        self.imageData = None
        self.imageHeight = 200
        self.imageWidth = 300

    def set_imagePath(self, path):
        self.imagePath = path

    def set_size(self, h, w):
        self.imageHeight = h
        self.imageWidth = w


    def set_poses_list(self, 
                       poses: List[List[int]], 
                       label:list[str],
                       text: list[str] = None,
                       description: list[str] = None,
        ):
        if not isinstance(poses, list):
            raise Exception("poses must be list")
        if not isinstance(label, list):
            raise Exception("label must be list")
        
        if len(poses) != len(label) and len(label) ==1:
            label = label * len(poses)

        if len(poses) != len(label):
            raise Exception("len(poses) must be equal to len(label)")

        for i in range(len(poses)):
            shape = Shape(poses[i])
            shape.set_label(label[i])
            if text:
                shape.set_text(text[i])
            if description:
                shape.set_description(description[i])
            self.shapes.append(shape.to_dict())
    
    def set_shape_text(self, ind:int, texts:str):
        if ind >= len(self.shapes):
            raise Exception("ind must be less than len(self.shapes)")
        self.shapes[ind]["text"] = texts

    def set_shape_description(self, ind:int, description:str):
        if ind >= len(self.shapes):
            raise Exception("ind must be less than len(self.shapes)")
        self.shapes[ind]["description"] = description

    def set_shape_label(self, ind:int, label:str):
        if ind > len(self.shapes):
            raise Exception("ind must be less than len(self.shapes)")
        self.shapes[ind]["label"] = label

    def set_shape_points(self, ind:int, points:List[int]):
        if ind >= len(self.shapes):
            raise Exception("ind must be less than len(self.shapes)")
        self.shapes[ind]["points"] = [[float(points[0]), float(points[1])], [float(points[2]), float(points[3])]]
    



    def set_poses(self, poses: List[List[float]], label="icon1"):
        if not isinstance(poses, list):
            raise Exception("poses must be list")
        temp = poses[0]
        assert isinstance(temp, list) and len(temp) == 4, "poses must be list and len(poses[0]) == 4"
        for pose in poses:
            shape = Shape(pose)
            shape.set_label(label)
            self.shapes.append(shape.to_dict())


    def to_dict(self):
        return self.__dict__
    def to_json_file(self, file_path):
        assert file_path.endswith(".json"), "file_path must be end with .json"
        
        with open(file_path, "w") as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    labelme = Labelme()
    labelme.set_imagePath("../icon4_imgs/imgs_00794_41425_0.png")
    labelme.set_size(200, 300)
    pose = [[1, 2, 3, 4], [5, 6, 7, 9]]
    labelme.set_poses(pose)
    labelme.to_json_file("icon4_imgs.json")