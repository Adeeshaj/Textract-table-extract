#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Zeptolytics
####################################################################################################
"""Flask Server entry point"""

##############################LIBRARY IMPORTS#######################################################
import json
from flask import Flask, request
import lib.multipage_detect_analize_text as mulitpage_analizer
import lib.textract_table_parser as table_parser
from lib.s3 import upload_file
from config.config import BUCKET_NAME, TEXTRACT_ROLE_ARN
from model.outputs import Output
from lib.app_handler import merge_to_one
####################################################################################################

APP = Flask(__name__)
APP.config['DEBUG'] = True

@APP.route("/post/ocr/data", methods=['POST'])
def extract_ocr_data():
    if not request.data:
        response = {"response": {"ErrorCode": 400, "Status": "ValidationError", "message": "no request content found"}}
    else:
        content = request.get_json(silent=True)
        if "path" not in content:
            response = {"response": { "ErrorCode": 400, "Status": "ValidationError", "message": "path is required" }}
        else: 
            file_path = content["path"]
            file_name = content["name"]
            uploaded = upload_file(file_path, BUCKET_NAME, file_name)
            if(uploaded):
                analyzer = mulitpage_analizer.DocumentProcessor(TEXTRACT_ROLE_ARN, BUCKET_NAME, file_name)
                analyzer.CreateTopicandQueue()
                tables, job_id = analyzer.ProcessDocument(multipage_analizer.ProcessType.ANALYSIS)
                analyzer.DeleteTopicandQueue()
            if(tables and job_id):
                table = merge_to_one(tables)
                output = Output(file_name, table, file_path, job_id)
                output_id = output.save()
            if(output_id):
                json_tables = table_parser.get_table_json_results(output.table)
    return 0



#invoking the app instance
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=5000)