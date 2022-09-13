from sqlalchemy.orm import Session

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from db.models.course import Section
from pydantic_schemas.section import SectionCreate


def get_section(db: Session, section_id: int):
    return db.query(Section).filter(Section.id == section_id).first()

# async def get_user(db: AsyncSession, user_id: int):
#     query = select(User).where(User.id == user_id)
#     result = await db.execute(query)
#
#   return result.scalar_one_or_none()



def get_sections(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Section).offset(skip).limit(limit).all()


def update_section(db: Session, id:int, request: Section):
    section = db.query(Section).filter(Section.id == id)
    section.update({
        Section.title: request.title,
        Section.description: request.description,
        Section.course_id: request.course_id
    })
    db.commit()
    return 'ok'


def create_section(db: Session, section: Section):
    db_section = Section(
        title= section.title,
        description= section.description,
        course_id= section.course_id
    )
    db.add(db_section)
    db.commit()
    db.refresh(db_section)
    return db_section 


def delete_section(db: Session, id:int):
    section = get_section(db, id)
    db.delete(section)
    db.commit()
