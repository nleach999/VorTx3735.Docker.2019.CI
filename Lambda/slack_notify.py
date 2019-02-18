import logging
import os
import requests 

# A script for an AWS Lambda function.  Using CloudWatch, sends build failures
# from CodeBuild to this Lambda method.  The payload is parsed and a Slack
# notification is sent. This method is not ideal because the build fail log
# is not easy to send with the Slack notification.

def slack_handler (event, context):

    h = {"content-type" : "application/json" }

    try:
        slack_hook = os.environ['SLACK_HOOK_URI']
    except Exception:
        raise Exception ("SLACK_HOOK_URI is missing from the environment.")
    
    try:
        project_name = os.environ['PROJECT_NAME']
    except Exception:
        raise Exception ("PROJECT_NAME is missing from the environment.")
        

    if (event['detail']['build-status'] == "FAILED" and event['detail']['project-name'] == project_name):
        message = "Build status: {0} for build started at {2}.  Source Tree: {1}".format (event['detail']['build-status'], 
            event['detail']['additional-information']['source']['location'], event['detail']['additional-information']['build-start-time'])
        logging.getLogger (__name__).error (message)



        for phase in event['detail']['additional-information']['phases']:
            if (phase['phase-type'] == "BUILD" and phase['phase-status'] == "FAILED"):
              for line in phase['phase-context']:
                message = message + "\n```"
                message = message + line
                message = message + "```"


        payload = "{{\"text\" : \"{0}\"}}".format (message)
        response = requests.post (url=slack_hook, data=payload, headers=h)

        logging.getLogger (__name__).info (response)
    else:
        logging.getLogger (__name__).info ("State does not indicate failure.")




    return None
