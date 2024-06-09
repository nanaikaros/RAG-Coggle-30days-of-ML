import time
import jwt
import requests

# 实际KEY，过期时间
def generate_token(apikey: str, exp_seconds: int):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("invalid apikey", e)

    payload = {
        "api_key": id,
        "exp": int(round(time.time() * 1000)) + exp_seconds * 1000,
        "timestamp": int(round(time.time() * 1000)),
    }
    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
headers = {
  'Content-Type': 'application/json',
  'Authorization': generate_token("b19dbe196885e88a3cd3ff787d5c80d7.jKgf9lVtGWa0wLHe", 1000)
}

# data = {
#     "model": "glm-3-turbo",
#     "messages": [{"role": "user", "content": """你好"""}]
# }

# data = {
#   "model": "embedding-2",
#   "input": "测试文本，今天很开心。"
# }
data = {
  "model": "glm-3-turbo", # "gpt-4-0613",
  "messages": [
    {"role": "user", "content": "李华和小王是不是认识？"},
  ],
  "tools": [
    {
      "name": "get_connection",
      "description": "判断用户1和用户2 是否为朋友关系",
      "parameters": {
        "type": "object",
        "properties": {
          "user_id1": {
            "type": "string",
            "description": "用户ID 1"
          },
          "user_id2": {
            "type": "string",
            "description": "用户ID 2"
          },
        },
        "required": ["user_id1", "user_id2"]
      }
    }
  ]
}


response = requests.post(url, headers=headers, json=data)

print("Status Code", response.status_code)
print("JSON Response ", response.json())