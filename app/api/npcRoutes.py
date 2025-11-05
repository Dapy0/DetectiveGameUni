from pathlib import Path
from fastapi import APIRouter, HTTPException

from app.schema import NPCChatRequest, NPCChatResponse
from app.services.ollamaService import generate_structured_output

npcRouter = APIRouter(prefix="/npc")

try:

    SCENARIO = Path("assets/scenario_lore.txt").read_text(encoding="utf-8")
    NPCPERSONA = Path("assets/npc_persona.txt").read_text(encoding="utf-8")
except Exception as e:
    print(f"Error in npc Router:\n${e}")
    raise HTTPException(status_code=502, detail=e)


@npcRouter.post("/chat", response_model=NPCChatResponse)
def chatWithNpc(data: NPCChatRequest):

    system_prompt = f"""
      {NPCPERSONA}

      GLOBALNA FABUŁA:
      <lore>
      {SCENARIO}
      </lore>

      BIEŻĄCA SCENA:
      <scene>
      {data.sceneContext}
      </scene>

      TWOJA POSTAĆ:
      Imię: {data.npcName}
      Rola: {data.npcRole}
    """

    user_prompt = f"Gracz mówi do Ciebie: \"{data.playerText}\""

    print(">>> Calling generate_structured_output")
    response = generate_structured_output(
        system_prompt,
        user_prompt,
        NPCChatResponse
    )
    print(">>> Response:   ", response)

    if "error" in response:
        raise HTTPException(status_code=502, detail=response)

    return response
