from fastapi import Fastapi

app = Fastapi


@app.get("/")
def hello_world():
    return {"message": "สวัสดีค่ะหนูชื่อ ฉัตรพร แก้วเฉลิม"}