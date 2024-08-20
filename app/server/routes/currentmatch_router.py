from fastapi import APIRouter, Body

from app.server.common.match_constants import MatchConstants
from app.server.service.currentmatch_service import CurrentMatchService
from app.server.model.matchchannel.currentmatch_model import CurrentMatchModel
from datetime import date

router = APIRouter()


@router.get("/", response_description="Match retrieved")
async def getCurrentMatchByAll():
    service = CurrentMatchService()
    currentsL = await service.getAllCurrentMatch()
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/status/{status}")
async def getCurrentMatchByStatus(status: str):
    service = CurrentMatchService()
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_STATUS, status, None)
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}")
async def getCurrentMatchByChampions(championship: str):
    service = CurrentMatchService()
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE, championship, None)
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}/status/{status}", response_description="Match retrieved")
async def getCurrentMatchByChampionsAndStatus(championship: str, status: str):
    service = CurrentMatchService()
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_STATUS_CHAMPIONSHIP_CODE, championship, status)
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.delete("/dateMatch/{dateMatch}", response_description="Data deleted from the database")
async def deleteForDate(dateMatch: str):
    service = CurrentMatchService()
    new_currentMatch = await service.deleteCurrentMatchForCondiction(MatchConstants.DELETE_DATE, dateMatch, None)
    if new_currentMatch:
        return CurrentMatchModel.ResponseModel("DELETE", "delete successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")


@router.delete("/dateMatch/{dateMatch}/championship/{championship}", response_description="Data deleted from the database")
async def deleteForStatus(dateMatch: str, championship: str):
    service = CurrentMatchService()
    new_currentMatch = await service.deleteCurrentMatchForCondiction(MatchConstants.DELETE_DATE_CHAMPIONSHIP_CODE, dateMatch, championship)
    if new_currentMatch:
        return CurrentMatchModel.ResponseModel("DELETE", "delete successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")


@router.put("/", response_description="Data update the database")
async def put(req: CurrentMatchModel.as_optional() = Body(...)):
    # req = {k: v for k, v in req.dict().items() if v is not None}
    service = CurrentMatchService()
    dateCurrent = today = date.today()
    req.dateMatch = str(dateCurrent)
    up_currentMatch = await service.updateOrSaveCurrentMatch(req)
    if up_currentMatch:
        return CurrentMatchModel.ResponseModel("Update/Save CurrentMatch".format(id), "Success")
    return CurrentMatchModel.ErrorResponseModel("Error", 404, "Error update transaction")
