import fastapi

from typing import List, Optional

from fastapi import Path, Depends
from pydantic import BaseModel
from api.utils.sections import get_sections, create_section, get_section, update_section, delete_section
from sqlalchemy.orm import Session
from db.db_setup import get_db
from pydantic_schemas.section import Section, SectionCreate


router = fastapi.APIRouter()


@router.get("/sections", tags={"section"}, response_model=List[Section])
async def return_sections(db: Session = Depends(get_db)) -> list:
    return get_sections(db)


@router.post("/sections", tags={"section"})
async def post_section(section: Section, db: Session = Depends(get_db)):
    created_section = create_section(db, section)
    return created_section


@router.get("/section/{id}", tags={"section"})
async def return_section(id:int = Path(..., description="The ID of section you want to retrieve."), db: Session = Depends(get_db)):
    return get_section(db, id)


@router.put("/{id}", tags={"section"})
async def put_section(id: int, request: Section, db: Session = Depends(get_db)):
    return update_section(db, id, request)


@router.delete("/{id}", tags={"section"})
async def remove_section(id:int, db: Session = Depends(get_db)):
    delete_section(db,id)
    return {"message:", "Success"}
