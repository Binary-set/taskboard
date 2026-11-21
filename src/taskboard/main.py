from fastapi import @"
Host github.com
  Hostname ssh.github.com
  Port 443
  User git

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}