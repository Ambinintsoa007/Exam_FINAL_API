from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()

class Characteristic(BaseModel):
    max_speed: float
    max_fuel_capacity: float

class Car(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

cars_storage: List[Car] = []

@app.get("/ping")
def ping():
    return "pong"

@app.post("/cars", status_code=201)
def create_car(car: Car):
    cars_storage.append(car)
    return car

@app.get("/cars")
def get_cars():
    return cars_storage

@app.get("/cars/{id}")
def get_car(id: str):
    for car in cars_storage:
        if car.identifier == id:
            return car
    return JSONResponse(
        content={"message": f"Car with id {id} not found or does not exist"},
        status_code=404
    )

@app.put("/cars/{id}/characteristics")
def update_car_characteristics(id: str, characteristics: Characteristic):
    for car in cars_storage:
        if car.identifier == id:
            car.characteristics = characteristics
            return car
    return JSONResponse(
        content={"message": f"Car with id {id} not found or does not exist"},
        status_code=404
)