from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from .db import Base


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)


class Control(Base):
    __tablename__ = "controls"

    id = Column(String, primary_key=True, index=True)
    framework_id = Column(String, ForeignKey("frameworks.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)


class Lab(Base):
    __tablename__ = "labs"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    repo_path = Column(String, nullable=True)
    aws_services = Column(Text, nullable=True)
    evidence_types = Column(Text, nullable=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, nullable=False, default="planning")
    target_frameworks = Column(Text, nullable=True)


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    control_id = Column(String, ForeignKey("controls.id"), nullable=False)
    lab_id = Column(String, ForeignKey("labs.id"), nullable=True)
    type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)


class RemediationTask(Base):
    __tablename__ = "remediation_tasks"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    control_id = Column(String, ForeignKey("controls.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner = Column(String, nullable=True)
    status = Column(String, nullable=False, default="open")
    due_date = Column(DateTime, nullable=True)
