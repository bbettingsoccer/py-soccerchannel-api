from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.championship_model import ChampionshipModel
from fastapi.encoders import jsonable_encoder


class ChampionshipService:

    def __init__(self):
        self.collection = OperationImplDAO("championships")

    async def getAllChampionships(self):
        objectL = []
        try:
            objects = await self.collection.find_all()
            if objects:
                for objected in objects:
                    objectL.append(ChampionshipModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("Error Execution Find ", e)
        return None

    async def getChampionshipForCondiction(self, search: str, value1: str, value2: str):
        objectL = []
        filter = []
        match search:
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {ChampionshipModel.config.championshipCode: value1}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_NAME:
                filter = {ChampionshipModel.config.championshipName: {"$eq": value1}}
            case MatchConstants.GET_SEARCH_COUNTRY:
                filter = {ChampionshipModel.config.country: {"$eq": value1}}

        try:
            objects = await self.collection.find_condiction(filter)
            if objects:
                for objected in objects:
                    objectL.append(ChampionshipModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("Error Execution Find ", e)
        return None

    async def deleteChampionshipForCondiction(self, type: str, value1: str, value2: str):
        filter = []
        match type:
            case MatchConstants.DELETE_CHAMPIONSHIP_NAME:
                filter = {ChampionshipModel.config.championshipName: value1}
            case MatchConstants.DELETE_CHAMPIONSHIP_CODE:
                filter = {ChampionshipModel.config.championshipCode: value1}
        try:
            print('filter champion: ', filter)

            return await self.collection.delete_condition(filter)
        except Exception as e:
            print('Error delete process: ', e)
            return False

    async def updateChampionship(self, id: str, data: dict):
        if len(data) < 1:
            return False
        try:
            objFind = await self.collection.find_one(id)
            if objFind:
                objUp = await self.collection.update_condition(id, data)
                if objUp:
                    return True
                return False
        except Exception as e:
            print('Error update process: ', e)
            return False

    async def saveChampionship(self, dataObj: ChampionshipModel):
        objetJson = jsonable_encoder(dataObj)
        try:
            return await self.collection.save(objetJson)
        except Exception as e:
            print('Error update process', e)
            return False
