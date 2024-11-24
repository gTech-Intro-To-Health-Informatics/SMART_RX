from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from data_layer import PatientData
import twilio_integration.twilio

app = FastAPI()

manager = PatientData("Tables/patient.csv")

class UpdateRequest(BaseModel):
    id: int
    value: str

class CreateChat(BaseModel):
    name: str
    email: str
    phone: str
    drugs: str
    patient_history: str
    conversation_history: str


@app.get("/load_csv")
async def load_csv():
    manager.load_csv()
    return {"message": "CSV loaded successfully."}

@app.get("/get_column_data/{column_name}/{id_value}")
async def get_column_data(column_name: str, id_value: int):
    data = manager.get_column_data_by_id(column_name, id_value)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Data not found for ID {id_value} in column {column_name}.")
    return {column_name: data}

@app.get("/get_name/{id_value}")
async def get_name(id_value: int):
    return await get_column_data("name", id_value)

@app.get("/get_email/{id_value}")
async def get_email(id_value: int):
    return await get_column_data("email", id_value)

@app.get("/get_phone/{id_value}")
async def get_phone(id_value: int):
    return await get_column_data("phone", id_value)

@app.get("/get_drugs/{id_value}")
async def get_drugs(id_value: int):
    return await get_column_data("drugs", id_value)

@app.get("/get_patient_history/{id_value}")
async def get_patient_history(id_value: int):
    return await get_column_data("patient_history", id_value)

@app.get("/get_conversation_history/{id_value}")
async def get_conversation_history(id_value: int):
    return await get_column_data("conversation_history", id_value)

@app.get("/get_all_conversation_history")
async def get_all_conversation_history():
    return await get_all_conversation_data()

@app.put("/set_column_data/{column_name}")
async def set_column_data(column_name: str, request: UpdateRequest):
    success = manager.update_column_by_id(column_name, request.id, request.value)
    if success is None:
        raise HTTPException(status_code=404, detail=f"Column '{column_name}' or ID {request.id} not found.")
    return {"message": f"Updated {column_name} for ID {request.id} to '{request.value}'."}

@app.put("/set_new_chat")
async def set_new_chat(request: CreateChat):
    response = twilio_integration.twilio.create_and_send_conversation(request.phone)
    conversation_id = response["conversation_id"]
    return await set_new_patient_conversation(conversation_id,request.name,request.email,request.phone,request.drugs,request.patient_history,request.conversation_history)

@app.put("/set_name")
async def set_name(request: UpdateRequest):
    return await set_column_data("name", request)

@app.put("/set_email")
async def set_email(request: UpdateRequest):
    return await set_column_data("email", request)

@app.put("/set_phone")
async def set_phone(request: UpdateRequest):
    return await set_column_data("phone", request)

@app.put("/set_drugs")
async def set_drugs(request: UpdateRequest):
    return await set_column_data("drugs", request)

@app.put("/set_patient_history")
async def set_patient_history(request: UpdateRequest):
    return await set_column_data("patient_history", request)

@app.put("/set_conversation_history")
async def set_conversation_history(request: UpdateRequest):
    return await set_column_data("conversation_history", request)