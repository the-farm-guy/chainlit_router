from fastapi import FastAPI
import routers.router as router 

app = FastAPI()
app.include_router(router.router)

@app.get('/')
async def home():
    return {
        'message' : 'home page'
    }