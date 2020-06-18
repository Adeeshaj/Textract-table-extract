#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Zeptolytics
####################################################################################################
"""Flask Server entry point"""

##############################LIBRARY IMPORTS#######################################################
import json
from flask import Flask, request
import lib.multipage_detect_analize_text as mulitpage_analyser
import lib.textract_table_parser as table_parser
from lib.s3 import upload_file
from config.config import BUCKET_NAME, TEXTRACT_ROLE_ARN
from models.outputs import Output
from models.claims import Claim
from lib.app_handler import merge_to_one, get_valid_tables, create_rooms
####################################################################################################

APP = Flask(__name__)
APP.config['DEBUG'] = True

@APP.route("/extract/tables", methods=['POST'])
def extract_ocr_data():
    if not request.data:
        response = {"response": {"ErrorCode": 400, "Status": "ValidationError", "message": "no request content found"}}
    else:
        content = request.get_json(silent=True)
        if "path" not in content:
            response = {"response": { "ErrorCode": 400, "Status": "ValidationError", "message": "path is required" }}
        elif "name" not in content:
            response = {"response": { "ErrorCode": 400, "Status": "ValidationError", "message": "name is required" }}
        else: 
            file_path = content["path"]
            file_name = content["name"]
            uploaded = upload_file(file_path, BUCKET_NAME, file_name)
            if(uploaded):
                analyzer = mulitpage_analyser.DocumentProcessor(TEXTRACT_ROLE_ARN, BUCKET_NAME, file_name)
                analyzer.CreateTopicandQueue()
                tables, job_id = analyzer.ProcessDocument(mulitpage_analyser.ProcessType.ANALYSIS)
                analyzer.DeleteTopicandQueue()
            else:
                print("not uploaded")


            if(tables and job_id):
                table = merge_to_one(tables)
                output = Output(file_name, table, file_path, job_id)
                output_id = output.save()
            else:
                print("no talble")


            if(output_id):
                json_tables = table_parser.get_table_json_results(output.get_table())
                valid_tables = get_valid_tables(json_tables)
                rooms = create_rooms(valid_tables)
                claim = Claim(file_name, rooms, job_id)
                claim.save()
            else:
                print("no output id")
    return "Done!"



#invoking the app instance
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)