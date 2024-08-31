"""
主要实现九宫格验证码的识别
"""

import asyncio

from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Request

from app.common import Input, Output, responsesdict
from app.utils import get_res, token_validation

gt3nine = APIRouter()


# 这 @gt3 是一个路径操作装饰器,
@gt3nine.post("/nine3", 
    status_code=200, 
    response_model=Output, 
    summary = "三代九宫格", 
    description = "这是一个三代九宫格", 
    response_description = "返回json格式",
    responses=responsesdict
    )
async def nine3(
    input: Input,
    request: Request,
) -> Output:
    try:
        headers, input_data = token_validation(input, request)
        if headers is None and input_data is None:
            Output(code=403, msg="Token error", data={})
        # data = get_res("gt3nine",input_data, headers = headers)
        loop = asyncio.get_event_loop()
        newexecutor = ThreadPoolExecutor(max_workers=3)
        data = await loop.run_in_executor(newexecutor, get_res, "gt3nine", input_data, headers)
        return Output(code=200, msg="success", data=data)
    except:
        return Output(code=500, msg="Server Error", data={})
