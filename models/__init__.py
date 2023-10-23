#!/usr/bin/python3

"""
initialize the package
"""
from models.engine.db_config import DbConfig
storage = DbConfig()
storage.reload()