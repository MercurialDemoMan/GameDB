#!/usr/bin/env python3
# coding=utf-8

import os

from GameDB.Configuration import Configuration

class CsvDatabase:
    """database using csv as its backend"""
    
    def __init__(self, csv_path = None, separator = ";"):
        """initialize database"""
    
        self._db = None
        self._db_name = None
        self._separator = separator
        self._cache = {}
        self._scheme = []
        self._next_id = 0
        self._modified = False
        
        if csv_path is not None:
            self.open(csv_path)
    
    def cacheItemToDbItem(cache_item: list, separator: str = ";"):
        
        db_item = ""
        
        for i in range(len(cache_item)):
            if i == len(cache_item) - 1:
                db_item += str(cache_item[i])
            else:
                db_item += str(cache_item[i]) + separator
                
        return db_item + "\n"
        
    def dbItemToCacheItem(db_item: str, separator: str = ";"):
    
        return db_item.split(separator)
    
    def create(csv_path: str, scheme: list):
        """create local database with particular scheme and opens it"""

        if not os.path.isabs(csv_path):
            csv_path = Configuration.DatabasePath() + csv_path

        if not os.path.exists(csv_path):
                                
            db = open(csv_path, "w")
            
            if len(scheme) == 0:
                print("fuckem")
                
            if scheme[0] != "ID":
                scheme.insert(0, "ID")
            
            db.write(CsvDatabase.cacheItemToDbItem(scheme))
            db.close() 
                
    def open(self, csv_path: str):
        """open already created database"""
    
        self._db = open(csv_path, "r")
            
        self._db_name = csv_path
            
        scheme_read = False
        initialize_ids = False
            
        for entry in self._db:
            
            db_item = entry.rstrip("\n\r")
        
            cache_item = CsvDatabase.dbItemToCacheItem(db_item, self._separator)
                    
            if(len(cache_item) == 0):
                continue
            
            if not scheme_read:
            
                if cache_item[0] != "ID":
                    initialize_ids = True
                    self._scheme.append("ID")
            
                for attribute in cache_item:
                    self._scheme.append(attribute)
                scheme_read = True
            else:
            
                if initialize_ids:

                    if len(cache_item) == len(self._scheme) - 1:
                        self._cache[self._next_id] = cache_item
                        self._next_id += 1
                else:
                
                    if len(cache_item) == len(self._scheme):
                        self._cache[cache_item[0]] = cache_item[1:]
                        self._next_id += 1
        
        if initialize_ids:
            self._modified = True
        
    def close(self):
        """close database"""
    
        if self._db is not None:
            if self._modified:
                self.flush()
            self._db.close()
        
    def addOrUpdate(self, item: list):
        """insert or update item"""
    
        if (len(item) != len(self._scheme)) and (len(item) != len(self._scheme) - 1):
            return None
            
        self._modified = True
            
        if len(item) == len(self._scheme):
            self._cache[item[0]] = item[1:]
            return item
        else:
            
            while str(self._next_id) in self._cache:
                self._next_id += 1
        
            self._cache[str(self._next_id)] = item
            self._next_id += 1
            
            return [str(self._next_id - 1)] + item
    
    def getAll(self):
        """extract all items from database"""
        
        cache_items = []
        
        for item in self._cache.items():
            cache_items.append([item[0]] + item[1])
            
        return cache_items
    
    def getByID(self, identificator):
        """extract particular item"""
        
        cache_item = self._cache[identificator]
        
        if cache_item is None:
            return None
            
        return [identificator] + cache_item
    
    def getByQuery(self, query, mapper = None):
        """extract items"""
        
        result = []
        
        if mapper is None:
        
            for entry in self._cache.items():
            
                cache_item = [entry[0]] + entry[1]
            
                if query(cache_item):
                    result.append(cache_item)
        
        else:
            
            for entry in self._cache.items():
                
                cache_item = [entry[0]] + entry[1]
                
                mapped_entity = mapper(cache_item)
                
                if query(mapped_entity):
                    result.append(mapped_entity)
        
        return result
    
    def deleteById(self, identificator):
        """delete item"""
    
        if identificator in self._cache:
            del self._cache[identificator]
            self._modified = True
    
    def migrate(self, new_scheme: list):
        """migrate to a new scheme"""
        
        scheme_helper = []
        
        for i in range(len(new_scheme)):
            
            new_column = new_scheme[i]
            
            column_found = False
            
            for j in range(len(self._scheme)):
            
                old_column = self._scheme[j]
            
                if old_column == new_column:
                    
                    scheme_helper.append(j)
                    column_found = True
                    break
                    
            if not column_found:
                scheme_helper.append(None)
        
        CsvDatabase.create(self._db_name + "~migration", new_scheme)
        migration_db = CsvDatabase(self._db_name + "~migration")
        
        for old_entity in self.getAll():
            
            new_entity = [old_entity[0]]
            
            for index in scheme_helper:
                if index is None:
                    new_entity.append("")
                else:
                    new_entity.append(old_entity[index])
            
            migration_db.addOrUpdate(new_entity)
        
        migration_db.close()
    
    def flush(self):
        """flush cache to disk"""
    
        if(self._db is not None):
            self._db.close()
            self._db = open(self._db_name, "w")
            
            scheme = CsvDatabase.cacheItemToDbItem(self._scheme, self._separator)
            self._db.write(scheme)
            
            for entry in self._cache.items():
                
                cache_item = [entry[0]] + entry[1]
                db_item = CsvDatabase.cacheItemToDbItem(cache_item, self._separator)
                self._db.write(db_item)
            
            self._db.close()
            self._db = open(self._db_name, "r")
   
if __name__ == "__main__":
    db = CsvDatabase("Games.DB/finished.csv")
    db.migrate(["Title", "Platform", "Rating", "Review", "ImageURL"])
    db.close()