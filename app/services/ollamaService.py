import json
from typing import Any, Dict, Type
import requests
from pydantic import BaseModel
from app.config import settings
# from app.schema import NPCChatResponse


# schema: Dict[str, Any]
def build_payload(systemPrompt: str, userPrompt: str) -> Dict[str, Any]:
    return {
        "model": settings.MODEL,
        "messages": [
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt}
        ],
        "stream": False,
        "options": {"temperature": 0.3},
        "format": "json"  # schema
    }


# def sendRequest(system_prompt: str, player_input: str, schema: Dict[str, Any]) -> Dict[str, Any]:
# payload = build_payload(system_prompt, player_input, schema)

# try:
#     response = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
#     r.raise_for_status()
#     data = r.json()
#     content = extract_content_from_response(data)

#     # если content — уже dict (json parsed), используем как есть
#     if isinstance(content, dict):
#         parsed = content
#     else:
#         # иногда модель возвращает JSON внутри строки — парсим
#         try:
#             parsed = json.loads(content)
#         except json.JSONDecodeError:
#             # Попробуем повторить с уточнением: попросим вернуть строго JSON
#             print(
#                 f"[attempt {3}] Некорректный JSON в ответе. Содержимое: {content[:300]}")
#             # добавляем уточнение в payload (в "system")
#             payload["messages"].append({
#                 "role": "system",
#                 "content": "You MUST output only valid JSON exactly matching the schema. Nothing else."
#             })

#     # Валидация pydantic
#     npc = NPCOutput.model_validate(parsed)
#     return npc.model_dump()
# except (requests.RequestException) as e:
#     print(f"[attempt {3}] Network error: {e}")
# except ValidationError as ve:
#     print(f"[attempt {3}] Validation error: {ve}")
#     # попросим модель исправиться — добавляем системное уточнение
#     payload["messages"].append({
#         "role": "system",
#         "content": "Your previous output didn't match the schema. Output only the JSON object that validates."
#     })
# except Exception as ex:
#     print(f"[attempt {3}] Unexpected error: {ex}")
# return {"error": "no_valid_response", "reason": "max_retries_exceeded"}


def generate_structured_output(
    systemPrompt: str,
    userPrompt: str,
    responseModel: Type[BaseModel]
) -> Dict[str, Any]:

    schema_prompt = f"""
    {systemPrompt}
    
    {responseModel.model_json_schema()}
    """

    payload = build_payload(schema_prompt, userPrompt)

    for attempt in range(3):

        try:
            response = requests.post(
                settings.OLLAMA_URL, json=payload, timeout=50000)
            response.raise_for_status()

            data = response.json()
            content_str = data.get("message", {}).get("content", "")

            if not content_str:
                raise ValueError("Ollama вернул пустой 'message.content'")

            parsed_json = json.loads(content_str)

            validated_output = responseModel.model_validate(parsed_json)

            return validated_output.model_dump()

        except Exception as e:
            print(f"Error in ollama Service: {e}")
            return {"error": str(e)}
    return {"error": "Failed to get structured output after 4 attempts"} 
