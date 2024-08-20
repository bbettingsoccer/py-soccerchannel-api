from abc import ABC
from typing import List
import json
from motor.core import AgnosticCollection

from .operation_dao import OperationDAO
from bson.objectid import ObjectId
from ..common.database import MongoManager
from ..model.matchchannel.currentmatch_model import CurrentMatchModel


class OperationImplDAO(OperationDAO, ABC):
    instance_collection = None

    def __init__(self, collection):
        self.collection = collection
        self.instance_collection = self.get_collection()

    def get_collection(self) -> AgnosticCollection:
        database = MongoManager.getInstance()
        return database.get_collection(self.collection)

    async def find_all(self) -> list[dict]:
        schedulematchs1 = []
        async for scheduled in self.instance_collection.find():
            schedulematchs1.append(scheduled)
        return schedulematchs1

    async def save(self, data: dict) -> dict:
        try:
            collectionObj = await self.instance_collection.insert_one(data)
            new_collectionObj = await self.instance_collection.find_one({"_id": collectionObj.inserted_id})
            return new_collectionObj
        except Exception as e:
            print("Error try save", e)
            return None

    async def find_condiction(self, filter) -> list[dict]:
        currentsL = []
        try:
            async for objectFind in self.instance_collection.find(filter):
                currentsL.append(objectFind)
            return currentsL
        except Exception as e:
            print("Error Execute Find_condiction", e)
            return None

    async def find_one(self, id: str) -> dict:
        try:
            collectionObj = await self.instance_collection.find_one({"_id": ObjectId(id)})
            if collectionObj:
                return collectionObj
        except Exception as e:
            print('Error findOne transaction: ', e)

    async def update_condition(self, id, data):
        try:
            object = await self.instance_collection.update_many(
                {"_id": ObjectId(id)}, {"$set": data})
            return object
        except:
            print("Error try update")
            return None

    async def delete_condition(self, filter):
        try:
            object = await self.instance_collection.delete_many(filter)
            return True
        except Exception as e:
            print('Error DELETE transaction: ', e)

