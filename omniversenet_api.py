from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import uuid
import json

app = FastAPI()

# In-memory data storage (replace with a database in a real application)
data: Dict[str, Dict] = {}

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None
    tags: Optional[List[str]] = None

@app.post("/items/", response_model=Item, status_code=201)
async def create_item(item: Item):
    item_id = str(uuid.uuid4())
    data[item_id] = item.dict()
    return {**item.dict(), "id": item_id}

@app.get("/items/", response_model=List[Dict])
async def read_items():
    return [{"id": id, **item} for id, item in data.items()]

@app.get("/items/{item_id}", response_model=Dict)
async def read_item(item_id: str):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **data[item_id]}

@app.put("/items/{item_id}", response_model=Dict)
async def update_item(item_id: str, item: ItemUpdate):
    if item_id not in data:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item.dict(exclude_unset=True)
    data[item_id].update(update_data)
    return {"id": item_id, **data[item_id]}

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: str):
