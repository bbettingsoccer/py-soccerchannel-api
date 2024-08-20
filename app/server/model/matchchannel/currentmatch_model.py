import pydantic
from pydantic import BaseModel, Field, constr, conint, create_model, condate
from bson.objectid import ObjectId

class CurrentMatchModel(BaseModel):
    championshipCode: constr(strict=True) = Field(...)
    dateMatch: constr(strict=True) = Field(...)
    team1: constr(strict=True) = Field(...)
    team2: constr(strict=True) = Field(...)
    scoreTeam1: constr(strict=True) = Field(...)
    scoreTeam2: constr(strict=True) = Field(...)
    imgTeam1: constr(strict=True) = Field(...)
    imgTeam2: constr(strict=True) = Field(...)
    status: constr(strict=True) = Field(...)

    class config:
        championshipCode = "championshipCode"
        dateMatch = "dateMatch"
        team1 = "team1"
        team2 = "team2"
        scoreTeam1 = "scoreTeam1"
        scoreTeam2 = "scoreTeam2"
        imgTeam1 = "imgTeam1"
        imgTeam2 = "imgTeam2"
        status = "status"

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        OptionalModel =  create_model(
            f"Optional{cls.__name__}",
            __base__=CurrentMatchModel,
            **{
                k: (v.annotation, None) for k, v in CurrentMatchModel.model_fields.items()
               })

#        fields = {
 #           attribute: (Optional[data_type.type_], None)
  #          for attribute, data_type in annonations.items()
   #     }
       # OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
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
    def data_helper(currentmatch) -> dict:
        return {
            "id": str(currentmatch['_id']),
            "championshipCode": str(currentmatch["championshipCode"]),
            "dateMatch": str(currentmatch["dateMatch"]),
            "team1": str(currentmatch["team1"]),
            "team2": str(currentmatch["team2"]),
            "scoreTeam1": str(currentmatch["scoreTeam1"]),
            "scoreTeam2": str(currentmatch["scoreTeam2"]),
            "imgTeam1": str(currentmatch["imgTeam1"]),
            "imgTeam2": str(currentmatch["imgTeam2"]),
            "status": str(currentmatch["status"]),
        }
