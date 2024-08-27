from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.schedulematch_model import ScheduleMatchModel
from fastapi.encoders import jsonable_encoder
from typing import List


class ScheduleMatchService:

    def __init__(self):
        self.collection = OperationImplDAO("schedule_match")

    async def getScheduleMatchForAll(self):
        objectL = []
        try:
            objects = await self.collection.find_condition(None)
            if objects:
                for objected in objects:
                    objectL.append(ScheduleMatchModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("[Error :: Service] - FindAll")
        return None

    async def getScheduleMatchForCondiction(self, search: str, values: []):
        objectL = []
        filter = []
        match search:
            case MatchConstants.GET_SEARCH_DATE:
                filter = {ScheduleMatchModel.config.dateMatch: values[0]}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {ScheduleMatchModel.config.championshipCode: {"$eq": values[0]}}
            case MatchConstants.GET_SEARCH_DATE_MATCH_CHAMPIONSHIP_CODE:
                filter = {"$and": [{ScheduleMatchModel.config.championshipCode: {"$eq": values[0]}},
                                   {ScheduleMatchModel.config.dateMatch: {"$eq": values[1]}}]}
            case MatchConstants.GET_SEARCH_DATE_CHAMPIONSHIP_CODE_TEAM:
                filter = {"$and": [{ScheduleMatchModel.config.championshipCode: {"$eq": values[0]}},
                                   {ScheduleMatchModel.config.dateMatch: {"$eq": values[1]}},
                                   {ScheduleMatchModel.config.team1: {"$eq": values[2]}},
                                   {ScheduleMatchModel.config.team2: {"$eq": values[3]}}]}
        try:
            objects = None
            objects = await self.collection.find_condition(filter)
            if objects:
                for objected in objects:
                    objectL.append(ScheduleMatchModel.data_helper(objected))
                return objectL
        except Exception as e:
            print("[Error :: Service] - FindCondition > Filter :", filter)
            return None

    async def deleteScheduleMatchForCondiction(self, type: str, value1: str, value2: str):
        filter = []
        match type:
            case MatchConstants.DELETE_DATE:
                filter = {ScheduleMatchModel.config.dateMatch: value1}
            case MatchConstants.DELETE_DATE_CHAMPIONSHIP_CODE:
                filter = {"$and": [{ScheduleMatchModel.config.dateMatch: {"$eq": value1}},
                                   {ScheduleMatchModel.config.championshipCode: {"$eq": value2}}]}
        try:
            return await self.collection.delete_condition(filter)
        except Exception as e:
            print('Error :: Service] - DeleteCondition > Filter ', filter)
            return False

    async def updateScheduleMatch(self, id: str, data: dict):
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

    async def saveScheduleMatch(self, data: List[ScheduleMatchModel]):
        result = False
        try:
            for json_obj in data:
                values = [json_obj.championshipCode, json_obj.dateMatch, json_obj.team1, json_obj.team2]
                objUpdateOrSave = await self.getScheduleMatchForCondiction(
                    MatchConstants.GET_SEARCH_DATE_CHAMPIONSHIP_CODE_TEAM, values)

                if objUpdateOrSave is None: # SAVE - Transaction
                    result = True
                    currentMatchSave = jsonable_encoder(json_obj)
                    await self.collection.save(currentMatchSave)
            return result
        except Exception as e:
            print("[Error :: Service] - Save")
