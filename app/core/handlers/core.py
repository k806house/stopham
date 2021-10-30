import os
import json
from datetime import datetime

import pandas as pd
from flask import Blueprint, Response, request, redirect, current_app, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest


def construct_blueprint():
    core_bp = Blueprint('core', __name__)
    CORS(core_bp)

    @core_bp.route('/recognize', methods=['POST'])
    def recognize():
        if request.method == 'POST':
            return jsonify({
                'status': 'ok'
            })

    return core_bp

