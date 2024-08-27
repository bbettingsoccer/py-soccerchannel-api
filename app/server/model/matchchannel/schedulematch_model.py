from typing import Optional
from pydantic import BaseModel, Field, constr, conint, create_model


class ScheduleMatchModel(BaseModel):
    championshipCode: constr(strict=True) = Field(...)
    dateMatch: constr(strict=True) = Field(...)
    team1: constr(strict=True) = Field(...)
    team2: constr(strict=True) = Field(...)
    imgTeam1: constr(strict=True) = Field(...)
    imgTeam2: constr(strict=True) = Field(...)
    status: constr(strict=True) = Field(...)

    class config:
        championshipCode = "championshipCode"
        dateMatch = "dateMatch"
        team1 = "team1"
        team2 = "team2"
        imgTeam1 = "imgTeam1"
        imgTeam2 = "imgTeam2"
        status = "status"

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        OptionalModel = create_model(
            f"Optional{cls.__name__}",
            __base__=ScheduleMatchModel,
            **{
                k: (v.annotation, None) for k, v in ScheduleMatchModel.model_fields.items()
            })
        return OptionalModel

    def ResponseModel(data, message):
        return {
            "data": [data],
            "code": 200,
            "message": message,
        }

    def ErrorResponseModel(error, code, message):
        return {"error": error, "code": code, "message": message}

    @staticmethod
    def data_helper(scheduleMatch) -> dict:
        return {
            "_id": str(scheduleMatch['_id']),
            "championshipCode": str(scheduleMatch["championshipCode"]),
            "dateMatch": str(scheduleMatch["dateMatch"]),
            "team1": str(scheduleMatch["team1"]),
            "team2": str(scheduleMatch["team2"]),
            "imgTeam1": str(scheduleMatch["imgTeam1"]),
            "imgTeam2": str(scheduleMatch["imgTeam2"]),
            "status": str(scheduleMatch["status"]),
        }
