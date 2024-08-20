from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.schedulematch_model import ScheduleMatchModel
from fastapi.encoders import jsonable_encoder

class ScheduleMatchService:

    def __init__(self):
        self.collection = OperationImplDAO("schedule_match")

    async def getAllScheduleMatch(self):
        objectL = []
        try:
            objects = await self.collection.find_all()
            if objects:
                for objected in objects:
                    objectL.append(ScheduleMatchModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("Error Execution Find ", e)
        return None

    async def getScheduleMatchForCondiction(self, search: str, value1: str, value2: str):
        objectL = []
        filter = []
        match search:
            case MatchConstants.GET_SEARCH_DATE:
                filter = {ScheduleMatchModel.config.dateMatch: value1}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {ScheduleMatchModel.config.championshipCode: {"$eq": value1}}
            case MatchConstants.GET_SEARCH_STATUS_CHAMPIONSHIP_CODE:
                filter = {"$and": [{ScheduleMatchModel.config.championshipCode: {"$eq": value1}},
                                   {ScheduleMatchModel.config.dateMatch: {"$eq": value2}}]}
        try:
            print("getScheduleMatchForCondiction FILTER", filter)
            objects = await self.collection.find_condiction(filter)
            if objects:
                for objected in objects:
                    objectL.append(ScheduleMatchModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("Error Execution Find ", e)
        return None

    async def deleteScheduleMatchForCondiction(self, type: str, value1: str, value2: str):
        filter = []
        match type:
            case MatchConstants.DELETE_DATE:
                filter = {ScheduleMatchModel.config.dateMatch: value1}
            case MatchConstants.DELETE_DATE_CHAMPIONSHIP:
                filter = {"$and": [{ScheduleMatchModel.config.dateMatch: {"$eq": value1}},
                                   {ScheduleMatchModel.config.championshipCode: {"$eq": value2}}]}
        try:
            return await self.collection.delete_condition(filter)
        except Exception as e:
            print('Error delete process: ', e)
            return False

    async def updateScheduleMatch(self, id: str, data: dict):
        if len(data) < 1:
            return False
        try:
            print(" updateScheduleMatch ID ", id)
            objFind = await self.collection.find_one(id)
            if objFind:
                objUp = await self.collection.update_condition(id,data)
                if objUp:
                    return True
                return False
        except Exception as e:
            print('Error update process: ', e)
            return False

    async def saveScheduleMatch(self, scheduleMatchObj: ScheduleMatchModel):
        objetJson = jsonable_encoder(scheduleMatchObj)
        try:
            return await self.collection.save(objetJson)
        except Exception as e:
            print('Error update process', e)
            return False
