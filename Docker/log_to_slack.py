#!/usr/local/bin/python
import logging
import os
import requests
import sys
import time
from datetime import datetime
import pytz
import io


slack_http_headers = {"content-type" : "application/json" }


def send_log_to_slack(hook_uri, log_file): 
  
    response = requests.post (url=slack_hook, json=generate_slack_payload (open (log_file, "r") ), headers=slack_http_headers)

    logging.getLogger (__name__).info (response)



def get_environment_variable (varName, default=''):

    try:
        return os.environ[varName]
    except Exception:
        return default


def generate_slack_payload (fromBuffer):
    sourceRepoURL = get_environment_variable ('CODEBUILD_SOURCE_REPO_URL', 'Unknown')
    srcVersion = get_environment_variable ('CODEBUILD_RESOLVED_SOURCE_VERSION', 'Unknown')
    startTime = get_environment_variable ('CODEBUILD_START_TIME', 0)
    buildImage = get_environment_variable ('CODEBUILD_BUILD_IMAGE', 'Unknown')
    buildTimezone = get_environment_variable ('REPORT_TIMEZONE', 'UTC')

    stamp = datetime.fromtimestamp(int(startTime)/1000.0, tz=pytz.timezone (buildTimezone) )
    

    log = {"text": fromBuffer.read (), "pretext" : "```Repository [{0}]\nSource version [{1}]\nBuild image [{2}]```"
        .format (sourceRepoURL, srcVersion, buildImage),
        "footer" : "VorTx 3735 CI Slack Notification", "footer_icon" : "https://pbs.twimg.com/profile_images/784822961446334464/6Fm10ITh_400x400.jpg"} 
     

    message = { "text" : "Build failure for build started [{0}]".format (stamp), "attachments" : [log]}    
    
    return message



if __name__ == "__main__":
    notify = True

    try:
        slack_hook = os.environ['SLACK_HOOK_URI']
    except Exception:
        logging.getLogger (__name__).warning ("SLACK_HOOK_URI is missing from the environment, no notifications will be sent to Slack.")
        notify = False

    try:
        log_file_name = sys.argv[1]
    except Exception:
        logging.getLogger (__name__).warning ("The log file was not pass to the script, no notifications will be sent to Slack.")
        notify = False
    

    if notify:
        send_log_to_slack (slack_hook, log_file_name)
