# This file ensures the package is imported correctly
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(config_name=None):
    from app import create_app as _create_app
    return _create_app(config_name)
