from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User
import random
import string
from . import db

rooms = Blueprint('rooms', __name__)

@rooms.route('/<int:game_id>')
@login_required
def room(game_id):
    return render_template("room.html", user=current_user, )