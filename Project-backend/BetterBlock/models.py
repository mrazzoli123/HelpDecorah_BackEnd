#!/usr/bin/env python3
"""
Final Project models

@author: Gennaro Dimuro - Zoltan Mraz
@version: 2025.12
"""
import datetime

from flask_login import UserMixin

from marshmallow import fields
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from . import db, mm

class User(db.Model, UserMixin):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    google_id: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    profile_pic: Mapped[str] = mapped_column(nullable=False)

    tasks: Mapped[list["Task"]] = relationship(secondary="signup", back_populates="users")
    
    def __repr__(self):
        return f"User({self.google_id})"

class Task(db.Model):
    __tablename__ = "task"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    organization: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    voluntary: Mapped[str] = mapped_column(nullable=True)
    age: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime.date] = mapped_column(nullable=False)
    time: Mapped[datetime.time] = mapped_column(nullable=False)
    
   
    users: Mapped[list["User"]] = relationship(secondary="signup", back_populates="tasks")
    
    def __repr__(self):
        return f"Task({self.title})"

class Signup(db.Model):
    __tablename__ = "signup"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"), nullable=False)
    
    def __repr__(self):
        return f"Signup(user={self.user_id}, task={self.task_id})"
    
class UserSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        include_fk = True
        
    tasks = fields.Nested("TaskSchema", many=True, exclude=("users",))
    
class TaskSchema(mm.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
    
    users = fields.Nested("UserSchema", many=True, exclude=("tasks", ))