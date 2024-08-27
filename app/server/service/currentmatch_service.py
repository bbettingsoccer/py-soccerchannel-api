
from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.currentmatch_model import CurrentMatchModel
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import json_util, ObjectId


class CurrentMatchService:

    def __init__(self):
        self.collection = OperationImplDAO("current_match")

    async def getCurrentMatchForAll(self):
        currentsL = []
        try:
            currents = await self.collection.find_condition(None)
            if currents:
                for currented in currents:
                    print(currents)
                    currentsL.append(CurrentMatchModel.data_helper(currented))
                return currentsL
        except Exception as e:
            print("[Error :: Service] - Find")
        return None

    async def getCurrentMatchForCondiction(self, search: str, values: []):
        currentsL = []
        filter = []
        match search:
            case MatchConstants.GET_SEARCH_STATUS:
                filter = {CurrentMatchModel.config.status: values[0]}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {CurrentMatchModel.config.championshipCode: {"$eq": values[0]}}
            case MatchConstants.GET_SEARCH_DATE_MATCH_CHAMPIONSHIP_CODE:
                filter = {"$and": [{CurrentMatchModel.config.championshipCode: {"$eq": values[0]}},
                                   {CurrentMatchModel.config.dateMatch: {"$eq": values[1]}}]}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE_TEAM_DATA:
                filter = {"$and": [{CurrentMatchModel.config.championshipCode: {"$eq": values[0]}},
                                   {CurrentMatchModel.config.team1: {"$eq": values[1]}},
                                   {CurrentMatchModel.config.team2: {"$eq": values[2]}},
                                   {CurrentMatchModel.config.dateMatch: {"$eq": values[3]}}]}
        try:
            currents = await self.collection.find_condition(filter)

            if currents:
                for currented in currents:
                    currentsL.append(CurrentMatchModel.data_helper(currented))
                return currentsL
        except Exception as e:
            print("[Error :: Service] - Find_Condition > Filter :", filter)
        return None

    async def deleteCurrentMatchForCondiction(self, type: str, value1: str, value2: str):
        filter = []
        match type:
            case MatchConstants.DELETE_DATE:
                filter = {CurrentMatchModel.config.dateMatch: value1}
            case MatchConstants.DELETE_DATE_CHAMPIONSHIP_CODE:
                filter = {"$and": [{CurrentMatchModel.config.dateMatch: {"$eq": value1}},
                                   {CurrentMatchModel.config.championshipCode: {"$eq": value2}}]}
        try:
            return await self.collection.delete_condition(filter)
        except Exception as e:
            print("[Error :: Service] -  Delete > ", filter)
            return False

    async def updateCurrentMatch(self, id: str, data: CurrentMatchModel):
        try:
            jsonObj = jsonable_encoder(data)
            dbObj = await self.collection.find_one(id)
            if dbObj:
                await self.collection.update_one(id, jsonObj)
                return True
            else:
                return False
        except Exception as e:
            print("[Error :: Service] - Update")
            return False

    async def saveCurrentMatch(self, data: List[CurrentMatchModel]):
        try:
            for json_obj in data:
                values = [json_obj.championshipCode, json_obj.team1, json_obj.team2, json_obj.dateMatch]
                objUpdateOrSave = await self.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE_TEAM_DATA, values)

                if objUpdateOrSave:  # UPDATE - Transaction
                    objectFind = objUpdateOrSave[0]
                    id = (objectFind['_id'])
                    del objectFind['_id']
                    filter = {"_id": ObjectId(id)}
                    objectFind[CurrentMatchModel.config.scoreTeam1] = json_obj.scoreTeam1
                    objectFind[CurrentMatchModel.config.scoreTeam2] = json_obj.scoreTeam2
                    await self.collection.update_many(filter, objectFind)
                else:  # SAVE - Transaction
                    currentMatchSave = jsonable_encoder(json_obj)
                    await self.collection.save(currentMatchSave)
            return True
        except Exception as e:
            print("[Error :: Service] - Save ", e)
            return False
