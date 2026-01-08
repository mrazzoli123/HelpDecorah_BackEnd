#!/usr/bin/env python3
"""
Final Project routes

@author: Gennaro Dimuro - Zoltan Mraz
@version: 2025.12
"""
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from sqlalchemy import and_

from .models import User, UserSchema, Task, TaskSchema, Signup
from . import db

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Backend running successfully"}), 200

@main.route("/google", methods=["GET"])
def google_info():
    
    users = db.session.query(User).all()
    schema = UserSchema(many=True)
    result = schema.dump(users)
    
    return jsonify({"users": result}), 200

@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    
    task_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
    task_time = datetime.strptime(data.get("time"), "%H:%M").time()

    task = Task(
        title = data.get("title"),
        organization = data.get("organization"),
        location = data.get("location"),
        voluntary = data.get("voluntary"),
        age = data.get("age"),
        description = data.get("description"),
        date = task_date,
        time = task_time,
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully"
        }), 200

@main.route("/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    existing_task = db.session.query(Task).filter_by(id=task_id).first()
    if not existing_task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    changed = False

    if "title" in data and data["title"] is not None:
        if existing_task.title != data["title"]:
            existing_task.title = data["title"]
            changed = True

    if "organization" in data and data["organization"] is not None:
        if existing_task.organization != data["organization"]:
            existing_task.organization = data["organization"]
            changed = True

    if "location" in data and data["location"] is not None:
        if existing_task.location != data["location"]:
            existing_task.location = data["location"]
            changed = True

    if "voluntary" in data and data["voluntary"] is not None:
        if existing_task.voluntary != data["voluntary"]:
            existing_task.voluntary = data["voluntary"]
            changed = True

    if "age" in data and data["age"] is not None:
        if existing_task.age != data["age"]:
            existing_task.age = data["age"]
            changed = True

    if "description" in data and data["description"] is not None:
        if existing_task.description != data["description"]:
            existing_task.description = data["description"]
            changed = True

    if "date" in data and data["date"]:
        new_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
        if existing_task.date != new_date:
            existing_task.date = new_date
            changed = True

    if "time" in data and data["time"]:
        new_time = datetime.strptime(data["time"], "%H:%M").time()
        if existing_task.time != new_time:
            existing_task.time = new_time
            changed = True

        if changed:
            db.session.commit()

        return jsonify({"message": "Task updated successfully"}), 200

@main.route("/tasksinfo", methods=["GET"])
def tasks_info():
    
    tasks = db.session.query(Task).all()
    schema = TaskSchema(many=True)
    result = schema.dump(tasks)
    
    return jsonify({"tasks": result}), 200

@main.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        existing_user = db.session.query(User).filter_by(id=user_id).first()
        
        if existing_user:
            db.session.query(User).filter_by(id=user_id).delete()
        
            db.session.delete(existing_user)
            db.session.commit()
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred during deletion: {str(e)}"}), 500
    
    return jsonify({"message": "User deleted successfully"}), 200

@main.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        existing_task = db.session.query(Task).filter_by(id=task_id).first()
        
        if existing_task:
            db.session.query(Task).filter_by(id=task_id).delete()
        
            db.session.delete(existing_task)
            db.session.commit()
        else:
            return jsonify({"error": "Task not found"}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred during deletion: {str(e)}"}), 500
    
    return jsonify({"message": "Task deleted successfully"}), 200

@main.route("/tasks/<int:task_id>/register", methods=["POST"])
@login_required
def register_task(task_id):
    task = db.session.query(Task).filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    existing_signup = db.session.query(Signup).filter(
        and_(
            Signup.user_id == current_user.id,
            Signup.task_id == task_id
        )
    ).first()

    if existing_signup:
        return jsonify({
            "registered": False,
            "message": "User already registered",
            "count": len(task.users)
        }), 200

    signup = Signup(
        user_id=current_user.id,
        task_id=task_id
    )

    db.session.add(signup)
    db.session.commit()

    return jsonify({
        "registered": True,
        "message": "User registered successfully",
        "count": len(task.users)
    }), 201

@main.route("/my_jobs", methods=["GET"])
def get_my_jobs():
    
    
    currentid = current_user.id 
    signups = db.session.query(Signup).filter_by(user_id=currentid).all()
    task_ids = [signup.task_id for signup in signups]
    tasks = db.session.query(Task).filter(Task.id.in_(task_ids)).all()
    
    schema = TaskSchema(many=True)
    result = schema.dump(tasks)
    
    if not tasks:
        return jsonify({"message": "Task not found"}), 200
    
    return jsonify({"tasks": result}), 200

@main.route("/remove_job_for_user/<int:task_id>", methods=["DELETE"])
def remove_job_for_user(task_id):
    currentid = current_user.id 
    signup = db.session.query(Signup).filter_by(user_id=currentid, task_id=task_id).first()
    
    if not signup:
        return jsonify({"error": "Signup not found"}), 404

    db.session.delete(signup)
    db.session.commit()

    return jsonify({"message": "Signup removed successfully"}), 200