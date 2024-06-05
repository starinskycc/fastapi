import os
import requests
import json
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class PromptRequest(BaseModel):
    token: str
    text: str

@app.post("/generate-prompt")
async def generate_prompt(request: PromptRequest):
    # 验证token
    validation_token = os.getenv('VALIDATION_TOKEN')
    if request.token != validation_token:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 从环境变量中获取API密钥
    api_key = os.getenv('API_KEY')
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")

    # 设置请求头和数据
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'contents': [
            {
                'parts': [
                    {
                        'text': request.text
                    }
                ]
            }
        ]
    }

    # 发送POST请求
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}',
        headers=headers,
        data=json.dumps(payload)
    )

    # 返回响应内容
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
