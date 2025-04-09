from sqlalchemy.orm import Session
from sqlmodel import select, desc
from .model import Projects
from .schema import ProjectCreate, ProjectUpdate
import uuid
from datetime import datetime
from typing import List, Optional

class ProjectService:
    def get_all_projects(self, session: Session) -> List[Projects]:
        statement = select(Projects).order_by(desc(Projects.created_at))
        result = session.execute(statement)
        return result.scalars().all()

    def get_single_project(self, project_uid: uuid.UUID, session: Session) -> Optional[Projects]:
        statement = select(Projects).where(Projects.uid == project_uid.bytes)
        result = session.execute(statement)
        return result.scalar_one_or_none()

    def create_project(self, project_data: ProjectCreate, session: Session):
        # Pydantic's EmailStr validation is already handled in ProjectCreate
        new_project = Projects(
            name=project_data.name,
            desc=project_data.desc,
            email=project_data.email,  # EmailStr validated by Pydantic
            type=project_data.type,
        )
        
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return new_project

    def update_project(self, project_uid: uuid.UUID, 
                      project_update_data: ProjectUpdate, 
                      session: Session):
        project = session.query(Projects).filter(Projects.uid == project_uid.bytes).first()
        if not project:
            return None

        # Only update fields that were actually provided
        update_data = project_update_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)

        project.updated_at = datetime.now()
        session.commit()
        session.refresh(project)
        return project
    
    def delete_project(self, project_uid: uuid.UUID, session: Session):
        project = session.get(Projects, project_uid.bytes)
        if not project:
            return False
            
        session.delete(project)
        session.commit()
        return True