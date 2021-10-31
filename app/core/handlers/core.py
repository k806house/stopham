import os
import json
import tempfile

from flask import Blueprint, Response, request, redirect, current_app, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

from core.s3 import upload_file_by_name


def _not_valid(body):
    return 'source' not in body or 'prefix' not in body


def get_result(src_url):
    audio = {
        "result": [
            {
                "time_start": 1.23456,
                "time_end": 2.3456
            }
        ]
    }
    video = {
        "result": [
            {
                "time_start": 1.23456,
                "time_end": 2.3456
            }
        ]
    }

    return {'audio': audio, 'video': video}

def construct_blueprint():
    core_bp = Blueprint('core', __name__)
    CORS(core_bp)

    @core_bp.route('/recognize', methods=['POST'])
    def recognize():
        if request.method == 'POST':
            data = request.get_json(force=True)

            if _not_valid(data):
                raise BadRequest('Data doesn\'t contain all required fields')

            src_url = data['source']
            prefix = data['prefix']

            result_files = get_result(src_url)
            for type_file, result_file in result_files.items():
                with tempfile.NamedTemporaryFile(mode="w+") as tmp_file:
                    json.dump(result_file, tmp_file)
                    tmp_file.flush()
                    upload_file_by_name(tmp_file.name, current_app.config["S3_BUCKET"], '', f'{prefix}_{type_file}.json')


            return Response(
                json.dumps({
                    "code": "200",
                    "message": "Files saved"
                }),
                status=200
            )

    return core_bp

