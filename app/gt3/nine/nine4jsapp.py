"""
主要实现九宫格验证码的识别
"""

import asyncio

from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Request

from app.common import Input, Output, responsesdict, InputChangeIdnine
from app.utils import  token_validation
from app.gt3.nine.ninejs import  get_resjs

gt4ninejs = APIRouter()



@gt4ninejs.post("/gt4nine", 
    status_code=200, 
    response_model=Output, 
    summary = "si代九宫格js", 
    description = "这是一个四代九宫格js", 
    response_description = "返回json格式",
    responses=responsesdict
    )
async def gt4nine(
    input: InputChangeIdnine,
    request: Request,
) -> Output:
    try:
        headers, input_data = token_validation(input, request)
        if headers is None and input_data is None:
            Output(code=403, msg="Token error", data={})
        # data = get_res("gt3nine",input_data, headers = headers)
        loop = asyncio.get_event_loop()
        newexecutor = ThreadPoolExecutor(max_workers=3)
        data = await loop.run_in_executor(newexecutor, get_resjs,  input_data, headers)
        return Output(code=200, msg="success", data=data)
    except:
        return Output(code=500, msg="Server Error", data={})
