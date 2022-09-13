from urllib import response
from urllib.request import Request
from fastapi import FastAPI, Request
import uvicorn
from api import users, courses, sections, file
from db.db_setup import engine
from db.models import user, course
from fastapi.middleware.cors import CORSMiddleware
from auth import authentication
from fastapi.staticfiles import StaticFiles
from api.templates import template
import time

user.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)



app = FastAPI(
    title="Fast API TEST",
    description="API for fastapi demo",
    version="0.0.1",
    contact={
        "name": "Amar",
        "email": "amar9864@gmail.com"
    },
    license_info={
        "name": "MIT",
    },
)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

app.include_router(authentication.router)
app.include_router(file.router)
app.include_router(users.router)
app.include_router(sections.router)
app.include_router(courses.router)
#app.include_router(template.router)

origins = {
    'example_app_or_page'
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount('/files', StaticFiles(directory="files"), name='files')


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=58192)

