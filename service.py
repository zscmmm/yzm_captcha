"""
识别服务,fastapi实现
"""
import time
from fastapi import FastAPI
from loguru import logger
logger.remove()
logger.add("log/app.log", rotation="500 MB", retention="10 days")
from app.gt3.word.word import gt3word
from app.gt3.nine.nine import gt3nine
from app.gt3.nine.nine4jsapp import gt4ninejs
from app.gt3.word.wordjsapp import gt3wordjs
from app.gt4.iconmi.iconmi import gt4iconmi

title = "验证码识别服务"
description = "验证码识别服务"
version = "1.0.0"
contact = {"name": "XXXX", "email": "XXXXXX@gmail.com"}

app = FastAPI(
    title=title,
    description=description,
    version=version,
    contact=contact
)

@app.get("/", summary="根路径", response_description="欢迎信息")
async def root() -> dict[str, str]:
    """
    欢迎访问验证码识别服务, 请查看文档
    """
    try:
        return {"message": "Hello World"}
    except Exception as e:
        return {"error": str(e)}
# 利用路由的方式, 实现模块化
app.include_router(gt3word, prefix="/gt3", tags=["三代文字点选"])
app.include_router(gt3nine, prefix="/gt3", tags=["三代九宫格"])
app.include_router(gt4iconmi, prefix="/gt4", tags=["四代图标点选"])
app.include_router(gt4ninejs, prefix="/gt4js", tags=["四代九宫格js"])
app.include_router(gt3wordjs, prefix="/gt3js", tags=["三代文字点选js"])



if __name__ == '__main__':
    import uvicorn
    port = 9100
    # from app.handleprocess import kill_process  #自己写的
    # kill_process(port)
    # #别人写的,可以在终端直接运行,也提供了一个函数
    import killport
    killport.kill_ports(ports=[port], view_only=False)
    time.sleep(2) # 等待进程结束,不然太快了,易出错
    
    log_config = "app/uvicorn_config.json"
    uvicorn.run("service:app", host="0.0.0.0", port=port, reload=True, 
                log_config=log_config, use_colors=True)

    # 或者直接在命令行: uvicorn service:app --port 9100 --reload
