from fastapi import FastAPI
from .routes import schedulematch_router as SchedulematchRouter
from .routes import currentmatch_router as CurrentmatchRouter
from .routes import championship_router as  ChampionshipRouter

app = FastAPI()
app.include_router(SchedulematchRouter.router, tags=["ScheduleMatch"], prefix="/soccerchannel/schedule")
app.include_router(CurrentmatchRouter.router, tags=["CurrentMatch"], prefix="/soccerchannel/current")
app.include_router(ChampionshipRouter.router, tags=["Championship"], prefix="/soccerchannel/championship")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this SheduleMatch domain !"}

