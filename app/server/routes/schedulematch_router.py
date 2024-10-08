from fastapi import APIRouter, Body
from app.server.common.match_constants import MatchConstants
from app.server.model.matchchannel.schedulematch_model import ScheduleMatchModel
from app.server.service.schedulematch_service import ScheduleMatchService
from typing import List

router = APIRouter()


@router.get("/", response_description="Match retrieved")
async def getCurrentMatchByAll():
    service = ScheduleMatchService()
    objectL = await service.getScheduleMatchForAll()
    if objectL:
        return ScheduleMatchModel.ResponseModel(objectL, "Match data retrieved successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/dateMatch/{dateMatch}")
async def getCurrentMatchByStatus(dateMatch: str):
    service = ScheduleMatchService()
    values = [dateMatch]
    objectL = await service.getScheduleMatchForCondiction(MatchConstants.GET_SEARCH_DATE, values)
    if objectL:
        return ScheduleMatchModel.ResponseModel(objectL, "Match data retrieved successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}")
async def getScheduleMatchByChampions(championship: str):
    service = ScheduleMatchService()
    values = [championship]
    objectL = await service.getScheduleMatchForCondiction(MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE, values)
    if objectL:
        return ScheduleMatchModel.ResponseModel(objectL, "Match data retrieved successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.get("/championship/{championship}/dateMatch/{dateMatch}", response_description="Match retrieved")
async def getScheduleMatchByChampionsAndStatus(championship: str, dateMatch: str):
    service = ScheduleMatchService()
    values = [championship, dateMatch]
    objectL = await service.getScheduleMatchForCondiction(MatchConstants.GET_SEARCH_DATE_MATCH_CHAMPIONSHIP_CODE,
                                                          values)
    if objectL:
        return ScheduleMatchModel.ResponseModel(objectL, "Match data retrieved successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 404, "CurrentMatch doesn't exist.")


@router.post("/", response_description="Data saved successfully")
async def postScheduleMatch(data: List[ScheduleMatchModel] = Body(...)):
    service = ScheduleMatchService()
    try:
        json_obj = await service.saveScheduleMatch(data)
        if json_obj:
            return ScheduleMatchModel.ResponseModel(None, "Match data retrieved successfully")
        return ScheduleMatchModel.ErrorResponseModel("You have same registers in database", 400,
                                                         "Champions doesn't exist.")
    except:
        return ScheduleMatchModel.ErrorResponseModel("Error occurred.", 500, "SheduleMatch doesn't exist.")


@router.put("/{id}", response_description="Data update the database")
async def putScheduleMatch(id: str, req: ScheduleMatchModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    print("update ", req)
    service = ScheduleMatchService()
    object = await service.updateScheduleMatch(id, req)
    if object:
        return ScheduleMatchModel.ResponseModel("Update/Save CurrentMatch".format(id), "Success")
    return ScheduleMatchModel.ErrorResponseModel("Error", 404, "Error update transaction")


@router.delete("/dateMatch/{dateMatch}", response_description="Data deleted from the database")
async def deleteScheduleMatchForDate(dateMatch: str):
    service = ScheduleMatchService()
    object = await service.deleteScheduleMatchForCondiction(MatchConstants.DELETE_DATE, dateMatch, None)
    if object:
        return ScheduleMatchModel.ResponseModel("DELETE", "delete for date successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")


@router.delete("/dateMatch/{dateMatch}/championship/{championship}",
               response_description="Data deleted from the database")
async def deleteScheduleMatchForDate(dateMatch: str, championship: str):
    service = ScheduleMatchService()
    object = await service.deleteScheduleMatchForCondiction(MatchConstants.DELETE_DATE_CHAMPIONSHIP_CODE, dateMatch,
                                                            championship)
    if object:
        return ScheduleMatchModel.ResponseModel("DELETE", "delete for date successfully")
    return ScheduleMatchModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")
