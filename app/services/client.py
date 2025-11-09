# import json
# from urllib import response
# import requests
# from typing import Dict, Any
# from pydantic import ValidationError
# from schema import NPCOutput, SCHEMA_FOR_OLLAMA

# OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
# MAX_RETRIES = 3
# TIMEOUT = 3000000


# def extract_content_from_response(resp_json: Dict[str, Any]) -> str:
   
#     if isinstance(resp_json, dict):
#         if "choices" in resp_json and isinstance(resp_json["choices"], list) and resp_json["choices"]:
#             choice = resp_json["choices"][0]
#             # возможные вложенные структуры:
#             if isinstance(choice, dict):
#                 # common: choice["message"]["content"]
#                 if "message" in choice and isinstance(choice["message"], dict) and "content" in choice["message"]:
#                     return choice["message"]["content"]
#                 if "content" in choice:
#                     return choice["content"]
#         # 2) older/newer: message.content
#         if "message" in resp_json and isinstance(resp_json["message"], dict):
#             return resp_json["message"].get("content")
#     # 3) fallback: try to find first string-looking value containing '{'

#     def find_json_string(obj):
#         if isinstance(obj, str) and "{" in obj:
#             return obj
#         if isinstance(obj, dict):
#             for v in obj.values():
#                 s = find_json_string(v)
#                 if s:
#                     return s
#         if isinstance(obj, list):
#             for v in obj:
#                 s = find_json_string(v)
#                 if s:
#                     return s
#         return None
#     candidate = find_json_string(resp_json)
#     if candidate:
#         return candidate
#     # final fallback: return stringified whole response
#     return json.dumps(resp_json)

