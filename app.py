from fastapi import FastAPI, Path

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World testing"}

inventory = {
    1: {
        "name": "Milk",
        "price": 3.99,
        "brand": "Regular"
    }
}

@app.get("/get-item/{item_id}/{name}")
async def get_item(item_id: int = Path(None, description="The ID of the Item you would like to view")):
    return inventory[item_id]


