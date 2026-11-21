from fastapi import FastAPI

app = FastAPI()
# 路由装饰器，表示这个函数响应 GET 请求
@app.get("/")
def read_root():
    return {"Hello": "World"}