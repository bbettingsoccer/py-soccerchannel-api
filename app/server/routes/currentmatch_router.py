from fastapi import APIRouter, Body
from typing import List
from app.server.common.match_constants import MatchConstants
from app.server.service.currentmatch_service import CurrentMatchService
from app.server.model.matchchannel.currentmatch_model import CurrentMatchModel

router = APIRouter()


@router.get("/", response_description="Match retrieved")
async def getCurrentMatchByAll():
    service = CurrentMatchService()
    currentsL = await service.getCurrentMatchForAll()
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/status/{status}")
async def getCurrentMatchByStatus(status: str):
    service = CurrentMatchService()
    values = [status]
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_STATUS, values)
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}")
async def getCurrentMatchByChampions(championship: str):
    service = CurrentMatchService()
    values = [championship]
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE, values)
    if currentsL:
        return CurrentMatchModel.ResponseModel(currentsL, "Match data retrieved successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}/datamatch/{datamatch}", response_description="Match retrieved")
async def getCurrentMatchByChampionsAndStatus(championship: str, datamatch: str):
    service = CurrentMatchService()
    values = [championship, datamatch]
    currentsL = await service.getCurrentMatchForCondiction(MatchConstants.GET_SEARCH_DATE_MATCH_CHAMPIONSHIP_CODE,
                                                           values)
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


@router.delete("/dateMatch/{dateMatch}/championship/{championship}",
               response_description="Data deleted from the database")
async def deleteForStatus(dateMatch: str, championship: str):
    service = CurrentMatchService()
    new_currentMatch = await service.deleteCurrentMatchForCondiction(MatchConstants.DELETE_DATE_CHAMPIONSHIP_CODE,
                                                                     dateMatch, championship)
    if new_currentMatch:
        return CurrentMatchModel.ResponseModel("DELETE", "delete successfully")
    return CurrentMatchModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")


@router.put("/{id}", response_description="Data update the database")
async def put(id: str, req: CurrentMatchModel.as_optional() = Body(...)):
    # req = {k: v for k, v in req.dict().items() if v is not None}
    service = CurrentMatchService()
    up_currentMatch = await service.updateCurrentMatch(id, req)
    if up_currentMatch:
        return CurrentMatchModel.ResponseModel("Update Transaction".format(id), "Success")
    return CurrentMatchModel.ErrorResponseModel("Error", 404, "Error update transaction")


@router.post("/", response_description="Data save the database")
async def post(data: List[CurrentMatchModel] = Body(...)):
    service = CurrentMatchService()
    save_currentMatch = await service.saveCurrentMatch(data)
    if save_currentMatch:
        return CurrentMatchModel.ResponseModel("Save Transaction", "Success")
    return CurrentMatchModel.ErrorResponseModel("Error", 404, "Error update transaction")
