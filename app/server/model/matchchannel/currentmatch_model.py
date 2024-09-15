import pydantic
from pydantic import BaseModel, Field, constr, conint, create_model, condate
from bson.objectid import ObjectId


class CurrentMatchModel(BaseModel):
    championshipCode: constr(strict=True) = Field(default=None, title="championshipCode")
    dateMatch: constr(strict=True) = Field(default=None, title="dateMatch")
    team1: constr(strict=True) = Field(default=None, title="team1")
    team2: constr(strict=True) = Field(default=None, title="team2")
    scoreTeam1: constr(strict=True) = Field(default=None, title="scoreTeam1")
    scoreTeam2: constr(strict=True) = Field(default=None, title="scoreTeam2")
    status: constr(strict=True) = Field(default=None, title="status")

    class config:
        championshipCode = "championshipCode"
        dateMatch = "dateMatch"
        team1 = "team1"
        team2 = "team2"
        scoreTeam1 = "scoreTeam1"
        scoreTeam2 = "scoreTeam2"
        status = "status"

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        OptionalModel = create_model(
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
            "_id": str(currentmatch['_id']),
            "championshipCode": str(currentmatch["championshipCode"]),
            "dateMatch": str(currentmatch["dateMatch"]),
            "team1": str(currentmatch["team1"]),
            "team2": str(currentmatch["team2"]),
            "scoreTeam1": str(currentmatch["scoreTeam1"]),
            "scoreTeam2": str(currentmatch["scoreTeam2"]),
            "status": str(currentmatch["status"]),
        }
