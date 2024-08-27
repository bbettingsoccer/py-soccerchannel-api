from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.championship_model import ChampionshipModel
from fastapi.encoders import jsonable_encoder
from typing import List


class ChampionshipService:

    def __init__(self):
        self.collection = OperationImplDAO("championships")

    async def getChampionshipsForAll(self):
        objectL = []
        try:
            objects = await self.collection.find_condition(None)
            if objects:
                for objected in objects:
                    objectL.append(ChampionshipModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("[Error :: Service] - FindAll")
        return None

    async def getChampionshipForCondition(self, search: str, values: [str]):
        objectL = []
        filter = []
        match search:
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {ChampionshipModel.config.championshipCode: values[0]}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_NAME:
                filter = {ChampionshipModel.config.championshipName: {"$eq": values[0]}}
            case MatchConstants.GET_SEARCH_COUNTRY:
                filter = {ChampionshipModel.config.country: {"$eq": values[0]}}

        try:
            objects = await self.collection.find_condition(filter)
            if objects:
                for objected in objects:
                    objectL.append(ChampionshipModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("[Error :: Service] - FindCondition > Filter :", filter)
        return None

    async def deleteChampionshipForCondition(self, type: str, value1: str, value2: str):
        filter = []
        match type:
            case MatchConstants.DELETE_CHAMPIONSHIP_NAME:
                filter = {ChampionshipModel.config.championshipName: value1}
            case MatchConstants.DELETE_CHAMPIONSHIP_CODE:
                filter = {ChampionshipModel.config.championshipCode: value1}
        try:
            return await self.collection.delete_condition(filter)
        except Exception as e:
            print('Error :: Service] - DeleteCondition > Filter ', filter)
            return False

    async def updateChampionship(self, id: str, data: dict):
        if len(data) < 1:
            return False
        try:
            objFind = await self.collection.find_one(id)
            if objFind:
                await self.collection.update_one(id, data)
                return True
        except Exception as e:
            print('Error :: Service] - Update >', data)
            return False

    async def saveChampionship(self, data: List[ChampionshipModel]):
        filter = []
        result = False
        try:
            for json_obj in data:
                values = [json_obj.championshipName]
                objUpdateOrSave = await self.getChampionshipForCondition(MatchConstants.GET_SEARCH_CHAMPIONSHIP_NAME, values)

                if objUpdateOrSave is None:  # SAVE - Transaction
                    jsonObj = jsonable_encoder(json_obj)
                    await self.collection.save(jsonObj)
                    result = True
            return result
        except Exception as e:
            print('Error :: Service] - Save >', e)
            raise
