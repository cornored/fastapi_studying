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

class InputComputerModel(BaseModel):
    owner: str
    description: Union[str, None] = Field(default=None, max_length=100)
    OS: OSType
    RAM: int = Field(ge=8, le=64)
    CPU: str

class OutputComputerModel(InputComputerModel):
    creation_time: str

@app.get("/name")
def name():
    hostname = socket.gethostname()
    return{"The hostname is:", hostname}

@app.get("/time")
def time(format: str = "%Y-%m-%d %H:%M:%S"):
    current_time = datetime.datetime.now().strftime(format)
    return{"The current time is:", current_time}

existing_pc = []

@app.post("/pc")
def add_pc(pc: InputComputerModel, format: str = "%Y-%m-%d %H:%M:%S"):
    new_pc = OutputComputerModel(
        **pc.model_dump(),
        creation_time=datetime.datetime.now().strftime(format)
    )
    existing_pc.append(new_pc)
    return new_pc

@app.get("/pc", response_model=list[OutputComputerModel])
def get_pc():
    return existing_pc