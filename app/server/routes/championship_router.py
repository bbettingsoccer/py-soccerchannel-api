from typing import List

from fastapi import APIRouter, Body
from app.server.common.match_constants import MatchConstants
from app.server.model.matchchannel.championship_model import ChampionshipModel
from app.server.service.championship_service import ChampionshipService

router = APIRouter()


@router.get("/", response_description="Match retrieved")
async def getChampionshipByAll():
    service = ChampionshipService()
    objectL = await service.getChampionshipsForAll()
    if objectL:
        return ChampionshipModel.ResponseModel(objectL, "Championship data retrieved successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 404, "Championship doesn't exist.")


@router.get("/championship/code/{code}")
async def getChampionshipByCode(code: str):
    service = ChampionshipService()
    values = [code]
    objectL = await service.getChampionshipForCondition(MatchConstants.GET_SEARCH_CHAMPIONSHIP_CODE, values)
    if objectL:
        return ChampionshipModel.ResponseModel(objectL, "Data retrieved successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 404, "Championship doesn't exist.")


@router.get("/championship/name/{name}")
async def getChampionshipByChampions(name: str):
    service = ChampionshipService()
    values = [name]
    objectL = await service.getChampionshipForCondition(MatchConstants.GET_SEARCH_CHAMPIONSHIP_NAME, values)
    if objectL:
        return ChampionshipModel.ResponseModel(objectL, "Match data retrieved successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 404, "Championship doesn't exist.")


@router.get("/championship/country/{country}", response_description="Data retrieved")
async def getChampionshipByChampionsAndStatus(country: str):
    service = ChampionshipService()
    values = [country]
    objectL = await service.getChampionshipForCondition(MatchConstants.GET_SEARCH_COUNTRY,values)
    if objectL:
        return ChampionshipModel.ResponseModel(objectL, "Data retrieved successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 404, "Championship doesn't exist.")


@router.post("/", response_description="Data saved successfully")
async def postChampionship(data: List[ChampionshipModel] = Body(...)):
    service = ChampionshipService()
    try:
        jsonObj = await service.saveChampionship(data)
        if jsonObj:
            return ChampionshipModel.ResponseModel(None, "Match data retrieved successfully")
        return ChampionshipModel.ErrorResponseModel("You have same registers in database", 400,
                                                         "Champions doesn't exist.")
    except Exception as e:
        return ChampionshipModel.ErrorResponseModel("Error occurred.", 500, "SheduleMatch doesn't exist.")


@router.put("/{id}", response_description="Data update the database")
async def putChampionship(id: str, data: ChampionshipModel = Body(...)):
    data = {k: v for k, v in data.dict().items() if v is not None}
    print(" Championship UP ", data)
    service = ChampionshipService()
    json_obj = await service.updateChampionship(id, data)
    if json_obj:
        return ChampionshipModel.ResponseModel("Update Championship".format(id), "Success")
    return ChampionshipModel.ErrorResponseModel("Error", 404, "Error update transaction")


@router.delete("/championship/name/{name}", response_description="Data deleted from the database")
async def deleteChampionshipForDate(name: str):
    service = ChampionshipService()
    object = await service.deleteChampionshipForCondition(MatchConstants.DELETE_CHAMPIONSHIP_NAME, name, None)
    if object:
        return ChampionshipModel.ResponseModel("DELETE", "delete for date successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")


@router.delete("/championship/code/{code}", response_description="Data deleted from the database")
async def deleteChampionshipForDate(code: str):
    service = ChampionshipService()
    object = await service.deleteChampionshipForCondition(MatchConstants.DELETE_CHAMPIONSHIP_CODE, code, None)
    if object:
        return ChampionshipModel.ResponseModel("DELETE", "delete for date successfully")
    return ChampionshipModel.ErrorResponseModel("An error occurred.", 500, "SheduleMatch doesn't exist.")