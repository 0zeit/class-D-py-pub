from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    description: Optional[str] = None


app = FastAPI()

fake_db: dict[int, ItemResponse] = {
    1: ItemResponse(id=1, name="사과", price=1500, in_stock=True, description="굉장한 사과"),
    2: ItemResponse(id=2, name="바나나", price=800, in_stock=False, description="매우긴 바나나"),
    3: ItemResponse(id=3, name="포도", price=4500, in_stock=True, description=None),
}

next_id = 4


@app.get("/items", response_model=list[ItemResponse])
def get_items():
    return list(fake_db.values())


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    
    return fake_db[item_id]


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    global next_id

    new_item = ItemResponse(id=next_id, **item.model_dump())
    fake_db[next_id] = new_item
    next_id += 1
    
    return new_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: Item):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    
    updated = ItemResponse(id=item_id, **item.model_dump())
    fake_db[item_id] = updated
    
    return updated


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="아이템을 찾을 수 없습니다")
    
    del fake_db[item_id]
    
    return {"message": f"아이템 {item_id}번이 삭제되었습니다"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


# http://localhost:8000/docs
# curl http://localhost:8000/items
# curl http://localhost:8000/items/1
# curl http://localhost:8000/items/999
# curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"name": "딸기", "price": 6000, "in_stock": true, "description": "엄청난 딸기"}'
# curl -X PUT http://localhost:8000/items/1 -H "Content-Type: application/json" -d '{"name": "수정된 사과", "price": 2000, "in_stock": false}'
# curl -X DELETE http://localhost:8000/items/2