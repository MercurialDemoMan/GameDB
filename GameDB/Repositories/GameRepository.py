#!/usr/bin/env python3
# coding=utf-8

from GameDB.Database.CsvDatabase import CsvDatabase
from GameDB.Entities.GameEntity import GameEntity

from GameDB.Configuration import Configuration

class GameRepository:

    Scheme = ["ID", "Title", "Platform", "Rating", "Review", "ImageURL"]

    def __init__(self, db_path = None):
    
        self._db = None
        
        if db_path is not None:
            self.open(db_path)
        
    def create(db_path: str):
        
        CsvDatabase.create(db_path, GameDatabase.Scheme)
        
    def open(self, db_path: str):
    
        self._db = CsvDatabase(Configuration.DatabasePath() + db_path)
        
    def close(self):
        
        if self._db is not None:
            self._db.close()
        
    def save(self, entity: GameEntity):
    
        if self._db is None:
            return None
        
        return self._db.addOrUpdate(entity.toList())

    def getAll(self):
        
        entities = []
        
        items = self._db.getAll()
        
        for item in items:
            entities.append(GameEntity.fromList(item))
            
        return entities

    def getByID(self, identificator):
        
        return GameEntity.fromList(self._db.getByID(identificator))
    
    def getByQuery(self, query):
        
        return self._db.getByQuery(query, GameEntity.fromList)
        

    def deleteById(self, identificator):
        
        self._db.deleteById(identificator)
        
    def delete(self, entity):
        
        if entity.ID is None:
            return
            
        self._db.deleteById(entity.ID)
    
    