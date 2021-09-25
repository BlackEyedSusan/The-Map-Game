from flask import Blueprint, render_template, request, flash, url_for, redirect, jsonify
from flask_login import login_required, current_user
from .models import Game, GamesJoined, User, Empires
from . import db
import sqlite3 as dbapi
import json

profiles = Blueprint('profiles', __name__)