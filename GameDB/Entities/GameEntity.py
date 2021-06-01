#!/usr/bin/env python3
# coding=utf-8

class GameEntity:

    def __init__(self, name = "", platform = "", rating = "", review = "", image_url = "", ID = None):
        
        self.ID       = ID
        self.name     = name
        self.platform = platform
        self.rating   = rating
        self.review   = review
        self.image_url = image_url
        
    def fromList(values: list):
    
        if(len(values) == 6):
            return GameEntity(values[1], values[2], values[3], values[4], values[5], values[0])
        else:
            return None
        
    def toList(self):
        
        if self.ID is None:
            return [self.name, self.platform, self.rating, self.review, self.image_url]
        else:
            return [self.ID, self.name, self.platform, self.rating, self.review, self.image_url]
    
    def clear(self):
        
        self.ID       = None
        self.name     = None
        self.platform = None
        self.rating   = None
        self.review   = None
        self.image_url = None
        
    def isClear(self):
        
        return self.ID is None and self.name is None and self.platform is None and self.rating is None and self.review is None and self.image_url is None
    
    def __eq__(self, model):
    
        return isinstance(model, GameEntity) and self.name == model.name and self.platform == model.platform and self.rating == model.rating and self.review == model.review and self.image_url == model.image_url
        
    def __str__(self):
    
        return "[{}] - [name: {}, platform: {}, rating: {}]".format(self.ID, self.name, self.platform, self.rating)
        