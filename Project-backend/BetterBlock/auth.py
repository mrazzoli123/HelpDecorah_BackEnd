#!/usr/bin/env python3
"""
Final Project authentication

@author: Gennaro Dimuro - Zoltan Mraz
@version: 2025.12
"""
import json

import requests
from flask import Blueprint, abort, current_app, flash, jsonify, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from . import client, db, login_manager
from .models import TaskSchema, User, UserSchema

auth = Blueprint("auth", __name__, url_prefix="/auth")

def get_google_provider_cfg():
    return current_app.config["GOOGLE_CONFIG"]

@auth.get("/login")
def login():
    """Log in"""
    google_cfg = get_google_provider_cfg()
    authorization_endpoint = google_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )

    return redirect(request_uri)


@auth.route("/login/callback")
def callback():
    """Google callback"""
    code = request.args.get("code")

    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )

    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(
            current_app.config["GOOGLE_CLIENT_ID"],
            current_app.config["GOOGLE_CLIENT_SECRET"],
        ),
    )

    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    google_id = userinfo_response.json()["sub"]
    email = userinfo_response.json()["email"]
    profile_pic = userinfo_response.json()["picture"]
    name = userinfo_response.json()["given_name"]

    user = db.session.query(User).filter_by(google_id=google_id).first()

    if not user:
        user = User(google_id=google_id, name=name, email=email, profile_pic=profile_pic)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    
    FRONTEND_URL = "https://gennarodimuro.github.io/BetterBlock/jobs.html"
    return redirect(FRONTEND_URL)


@auth.route("/logout")
@login_required
def logout():
    """Log out"""
    logout_user()
    
    FRONTEND_URL = "https://gennarodimuro.github.io/BetterBlock"
    return redirect(FRONTEND_URL)


@login_manager.user_loader
def load_user(user_id):
    """User loader"""
    return db.session.query(User).filter_by(id=user_id).first()

@auth.route("/user", methods=["GET"])
def user():
    if not current_user.is_authenticated:
        return jsonify({"authenticated": False}), 401

    schema = UserSchema()
    result = schema.dump(current_user)

    return jsonify({
        "authenticated": True,
        "user": result
    }), 200



    

    