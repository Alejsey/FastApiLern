from fastapi import FastAPI
from app.users.router import router as router_users
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine


app = FastAPI()
app.mount('/static', StaticFiles(directory='app/static'), 'static')
Base.metadata.create_all(engine)


@app.get("/")
def home_page():
    return {"message": "Привет!"}





app.include_router(router_users)
"""app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_pages)"""
