"""
主要实现图标点选验证码的识别
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Request
from app.common import Input, Output, responsesdict
from app.utils import get_res, token_validation


gt4iconmi = APIRouter()
@gt4iconmi.post("/icon4mi", 
    status_code=200, 
    response_model=Output, 
    summary = "四代图标点选 ", 
    description = "这是一个四代的文字点选", 
    response_description = "返回json格式",
    responses=responsesdict
    )
async def icon4mi(
    input: Input,
    request: Request, # 请求对象,用来获取请求头,请求体等信息
) -> Output:
    try:
        headers, input_data = token_validation(input, request)
        if headers is None and input_data is None:
            Output(code=403, msg="Token error", data={})
        # data = get_res("gt4icon", input_data, headers = headers)
        loop = asyncio.get_event_loop()
        newexecutor = ThreadPoolExecutor(max_workers=4)
        data = await loop.run_in_executor(newexecutor, get_res, "gt4icon", input_data, headers)
        return Output(code=200, msg="success", data=data)
    except:
        return Output(code=500, msg="Server Error", data={})
