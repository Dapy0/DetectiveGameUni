from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from fastapi.middleware.cors import CORSMiddleware
# from schema import NPCOutput, SCHEMA_FOR_OLLAMA
# from app.services.client import send_request

from app.api.npcRoutes import npcRouter
from app.api.sceneRoutes import sceneRouter
from app.config import settings

app = FastAPI()

app.include_router(npcRouter)
app.include_router(sceneRouter)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно указать ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# SYSTEM_PROMPT = pathlib.Path("system_prompt.txt").read_text()


# class NpcInteractionRequest(BaseModel):
#     sceneContext: str
#     playerText: str
#     # metadata: Dict[str, Any] = {}


# class PlotModel(BaseModel):
#     title: str
#     # nodes: List[ScriptNode]


# STORE = {
#   "currentPlot": None,
# }

# @app.post("/injectPlot")
# def injectPlot(plot: PlotModel):
    
  


# @app.post("/npc")
# def interactWithNpc(data: NpcInteractionRequest):
#     print(f"Контекст {data.sceneContext}")
#     print(f"То что написал чел {data.playerText}")
    

#     res = send_request(SYSTEM_PROMPT, payload.player_text, SCHEMA_FOR_OLLAMA)
#     if "error" in res:
#         raise HTTPException(status_code=502, detail=res)
#     # ещё одна проверка pydantic (чтобы наверняка)
#     try:
#         npc = NPCOutput.parse_obj(res)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail={
#                             "error": "invalid_after_validation", "reason": str(e)})
#     return npc.dict()
  
  
@app.post("/health")
@app.get("/health")
def health():
    return {"ok": True, "model": settings.MODEL, "ollama": "local"}
