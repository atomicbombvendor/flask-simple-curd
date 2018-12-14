from flask import request, render_template, jsonify, redirect, url_for, send_from_directory, make_response
import json

from config import TABLE_NAME
from create_app import app
from models import db, Ticket

