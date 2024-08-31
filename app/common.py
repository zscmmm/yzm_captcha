"""
一些公共的类
"""
from enum import Enum
from typing import Optional, Union
from typing import List, Optional
from pydantic import BaseModel, Field, validator



class Input(BaseModel):
    """
    输入的数据类
    """
    dataType: int = Field(..., description="数据类型, 1: url, 2: 文件流", example=1) #
    imageSource: list[str]  = Field(..., description="base64的图片", example="[base64编码的图片数据1]")
    extraicon: Optional[list]  = Field(None, description="base64的icon图片", example="[base64编码的图片数据1, base64编码的图片数据2]")
    imageID: Optional[str]  = Field(None, description="图片的id", example="string")
    token: Optional[str]  = Field(None, description="token", example="string")
    
    # # 验证器
    @validator('dataType')
    def dataType_must_be_int(cls, v):
        assert v in [1, 2], "dataType must be 1 or 2"
        return v


class InputChangeIdword3(BaseModel):
    """
    输入的数据类
    """
    challenge: str = Field(..., description="challenge参数", example="string")
    gt: str = Field(..., description="gt参数", example="string")
    key: str = Field(..., description="key参数(授权参数)", example="string")
    referer: Optional[str] = Field(None, description="referer 参数(可选)", example="string")
    ua: Optional[str] = Field(None, description="ua 参数(可选)", example="string")
    origin: Optional[str] = Field(None, description="origin 参数(可选)", example="string")
    pic: Optional[str] = Field(None, description="pic 参数(可选)", example="string")
    c: Optional[List[int]] = Field(None, description="c 参数(可选)", example=[1, 2, 3, 4])
    s: Optional[str] = Field(None, description="s 参数(可选)", example="string")


class InputChangeIdnine(BaseModel):
    """
    输入的数据类
    """
    gt: str  = Field(..., description="gt", example="string")
    key: str = Field(..., description="key", example="string")
    referer: Optional[str] = Field(None, description="referer", example="string")
    ua: Optional[str] = Field(None, description="ua", example="string")
    origin: Optional[str] = Field(None, description="origin", example="string")



class Output(BaseModel):
    code: int = Field(..., description="state code(状态码, 如果是 200,证明这边提供的服务没有问题) ", example=200) #code 的值只能是 StatusCodeEnum 枚举中的值, 200 或 500
    msg: str = Field(..., description="state massage(状态的信息, 这边提供的服务简单的做一下筛选,然后转发给极验)", example="success")
    data: Union[list, dict, str] = Field(..., description="return data(返回的数据, 这是验证码识别的结果,原封不动的返回,不做任何修改)", example={"imageID": "string", "res": [[184, 0, 259, 67], [176,238, 244, 310], [63,70,132,142]]})

    @validator('code')
    def code_must_be_int(cls, v):
        assert v in list(range(100, 6000)), "code must be 100 or 6000,放飞自我"
        return v

responsesdict ={
    403: {"description": "Token Error"},
    422: {"description": "Input Error - Invalid DataType"},
    456: {"description": "算法未实现"},
    500: {"description": "Input Error"}
}