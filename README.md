# sample
Quick project tying together AWS(SNS/SQS), Python and Docker

# This project is currently being renamed TwoCans
This is a simple point to point chat application. The application starts in a terminal and prompts for a handle for the current user. That handle is used to create an AWS SQS standard queue and an SNS topic with naming based on the handle. Next the application asks for the handle of another user (other end of the can).

The expectation is that a second instance of the application will be started with the handles being reversed. Communication between the two handles occurs over the SQS/SNS PubSub service.

The application has been dockerized and is hosted on dockerhub as the repository elsporko/sample. Deploy the application twice in 2 different terminals and chat between them.

# COMING ATTRACTIONS
The code that runs in the docker container is represented in the master branch on github. A the branch add_logging is under development. This will add a Lambda function that is triggered on SNS publish events. The Lambda calls a Flask API on an external server to log all chat transactions including:
  * Message timestamp
  * Chat session identification
  * Message sender
  * Message receiver
  * Message text
  
