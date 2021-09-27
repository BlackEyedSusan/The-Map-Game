from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User, Empires
from . import db
import sqlite3 as dbapi
import json

profiles = Blueprint('profiles', __name__)

@profiles.route('<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    counter=0
    for games in GamesJoined.query.filter_by(id=user_id):
        counter += 1
    if user == current_user:
        is_current_user = True
    else:
        is_current_user = False
    return render_template('profile.html', is_current=is_current_user, user=user, games_joined=counter)