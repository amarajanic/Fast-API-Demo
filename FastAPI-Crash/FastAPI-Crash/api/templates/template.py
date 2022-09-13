from urllib.request import Request
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router= APIRouter(
    prefix='/templates',
    tags =['templates']
)

templates = Jinja2Templates(directory='templates')

# @router.get("/users/{id}", response_class=HTMLResponse)
# def get_users(id:str, request: Request):
#     return templates.TemplateResponse(
#         "template.html",
#         {
#             "request": request,
#             "id": id
#         }
#     )