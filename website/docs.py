from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from .models import Empires, Friends, Game, GamesJoined, User
from . import db

docs = Blueprint('docs', __name__)

@docs.route('')
@login_required
def doc():
    return render_template('docs.html', user=current_user)
