#!/usr/bin/python3
from app import app
from app.routes import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
