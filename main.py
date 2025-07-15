from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Union
from enum import Enum
import socket
import datetime

app = FastAPI()

class OSType(str, Enum):
    windows = "Windows"
    linux = "Linux"
    macos = "macOS"

class ComputerSchema(BaseModel):
    owner: str
    description: Union[str, None] = Field(default=None, max_length=100)
    OS: OSType
    RAM: int = Field(ge=8, le=64)
    CPU: str

@app.get("/name")
def name():
    hostname = socket.gethostname()
    return{"The hostname is:", hostname}

@app.get("/time")
def time():
    now = datetime.datetime.now()
    return{"The current time is:", now}

existing_pc = []

@app.post("/add_pc")
def add_pc(pc: ComputerSchema):
    existing_pc.append(pc)
    return {"Success": True, "msg": "User added"}

@app.get("/get_pc")
def get_pc():
    return existing_pc