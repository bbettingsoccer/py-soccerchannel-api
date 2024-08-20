from app.server.common.match_constants import MatchConstants
from app.server.dao.operationimpl_dao import OperationImplDAO
from app.server.model.matchchannel.currentmatch_model import CurrentMatchModel
from datetime import date
from fastapi.encoders import jsonable_encoder


class CurrentMatchService:

    def __init__(self):
        self.collection = OperationImplDAO("current_match")

    async def getAllCurrentMatch(self):
        currentsL = []
        try:
            currents = await self.collection.find_all()
            if currents:
                for currented in currents:
                    currentsL.append(CurrentMatchModel.data_helper(currented))
                return currentsL
        except Exception as e:
            print("Error Execution Find ", e)
        return None

    async def getCurrentMatchForCondiction(self, search: str, value1: str, value2: str):
        currentsL = []
        filter = []

        match search:
            case MatchConstants.GET_SEARCH_STATUS:
                filter = {CurrentMatchModel.config.status: value1}
            case MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE:
                filter = {CurrentMatchModel.config.championshipCode: {"$eq": value1}}
            case MatchConstants.GET_SEARCH_STATUS_CHAMPIONSHIP_CODE:
                filter = {"$and": [{CurrentMatchModel.config.championshipCode: {"$eq": value1}},
                                   {CurrentMatchModel.config.status: {"$eq": value2}}]}
        try:
            currents = await self.collection.find_condiction(filter)
            if currents:
                for currented in currents:
                    currentsL.append(CurrentMatchModel.data_helper(currented))
                return currentsL
        except Exception as e:
            print("Error FindCondition Proccess ", e)
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
            print('Error DeleteCondition Proccess: ', e)
            return False

    async def updateOrSaveCurrentMatch(self, currentMatchObj: CurrentMatchModel):
        dtToday = date.today()
        filter = {"$and": [{CurrentMatchModel.config.team1: {"$eq": currentMatchObj.team1}},
                           {CurrentMatchModel.config.team2: {"$eq": currentMatchObj.team2}}]}
        try:
            objUpdateOrSave = await self.collection.find_condiction(filter)

            if objUpdateOrSave:
                objUpdateOrSave[CurrentMatchModel.config.scoreTeam1] = currentMatchObj.scoreTeam1
                objUpdateOrSave[CurrentMatchModel.config.scoreTeam2] = currentMatchObj.scoreTeam2
                await self.collection.update_condition(objUpdateOrSave['_id'], objUpdateOrSave)
            else:
                currentMatchSave = jsonable_encoder(currentMatchObj)
                await self.collection.save(currentMatchSave)
            return True
        except Exception as e:
            print('Error updateOrSave Proccess: ', e)
            return False
