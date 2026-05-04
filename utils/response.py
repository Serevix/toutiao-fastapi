from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

def success_response(msg:str="success",data=None):
    content={
        "code":"200",
        "msg":msg,
        "data":data
    }
    #                            将python对象转换为JSON对象
    return JSONResponse(content=jsonable_encoder(content))