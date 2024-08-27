from typing import Optional
from pydantic import BaseModel, Field, constr, conint, create_model


class ChampionshipModel(BaseModel):
    championshipCode: constr(strict=True) = Field(...)
    championshipName: constr(strict=True) = Field(...)
    country: constr(strict=True) = Field(...)
    image: constr(strict=True) = Field(...)
    totalTeams: conint(strict=True) = Field(...)
    dateStart: constr(strict=True) = Field(...)
    dateEnd: constr(strict=True) = Field(...)
    status: constr(strict=True) = Field(...)

    class config:
        championshipCode = "championshipCode"
        championshipName = "championshipName"
        country = "country"
        image = "image"
        totalTeams = "totalTeams"
        dateStart = "dateStart"
        dateEnd = "dateEnd"
        status = "status"

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        OptionalModel = create_model(
            f"Optional{cls.__name__}",
            __base__=ChampionshipModel,
            **{
                k: (v.annotation, None) for k, v in ChampionshipModel.model_fields.items()
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
    def data_helper(championship) -> dict:
        return {
            "_id": str(championship['_id']),
            "championshipCode": str(championship["championshipCode"]),
            "championshipName":  str(championship["championshipName"]),
            "country": str(championship["country"]),
            "image": str(championship["image"]),
            "totalTeams": str(championship["totalTeams"]),
            "dateStart": str(championship["dateStart"]),
            "dateEnd": str(championship["dateEnd"]),
            "status": str(championship["status"]),
        }
