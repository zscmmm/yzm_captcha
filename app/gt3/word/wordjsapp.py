"""
主要实现三代文字点选字js的接口
"""

import asyncio

from concurrent.futures import ThreadPoolExecutor

from fastapi import APIRouter, Request

from app.common import Input, Output, responsesdict, InputChangeIdword3
from app.utils import  token_validation
from app.gt3.word.wordjs import get_resjs, aioget_resjs
from loguru import logger
gt3wordjs = APIRouter()


@gt3wordjs.post("/gt3word", 
    status_code=200, 
    response_model=Output, 
    summary = "三代文字点选(适合b站)", 
    description = "三代文字点选(适合b站), 只需要传递 gt 和 challenge 两个参数即可,返回 json 格式数据识别结果, data 字段是极验返回的识别结果",
    response_description = "返回json格式, data 字段是极验返回的识别结果",
    responses=responsesdict
    )
async def gt3word(
    input: InputChangeIdword3,
    request: Request,
) -> Output:
    """
    参数:
    - input: 传入参数
    - request: 请求
    """
    try:
        headers, input_data = token_validation(input, request)
        if headers is None and input_data is None:
            logger.info(f"ip地址:{client_host}, input_data: {input_data}, 1返回信息: Token error")
            Output(code=403, msg="Token error", data={})
    except:
        logger.info(f"ip地址:{client_host}, input_data: {input_data}, 2返回信息: headers or input_data is None")
        return Output(code=403, msg="headers or input_data is None", data={"headers": headers, "input_data": input_data})
    try:
        client_host = request.client.host

        # data = get_resjs(input_data, headers = headers)
        data = await asyncio.gather(aioget_resjs(input_data, headers))
        # 如果 data 是 list 类型, 则返回第一个元素
        if isinstance(data, list):
            data = data[0]
        logger.info(f"ip地址:{client_host}, input_data: {input_data}, 3返回信息: {data}")
        return Output(code=200, msg="success", data=data)
    except:
        logger.info(f"ip地址:{client_host}, input_data: {input_data}, 4返回信息: Server Error")
        return Output(code=500, msg="Server Error", data={})
