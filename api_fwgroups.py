#!/usr/bin/python3

import request
import json
import time

from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json

#remove the InsecureRequestWarning messages
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
