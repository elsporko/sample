import boto3
import json
import sys
import re
from datetime import datetime

"""
Module to help facilitate calls to AWS SNS/SQS
"""
class AWS(object):
    """Container to handle interactions with AWS"""
    def __init__(self):
        self.sns = boto3.client('sns', 'us-east-2')
        self.sqs = boto3.client('sqs', 'us-east-2')
        self.sqs_res = boto3.resource('sqs', 'us-east-2')
        self.target_list = {}
        self.chat_tag = ''
        self.tag_set = False

    def create_topic(self, topic_name):
        self.topic = self.sns.create_topic(Name=topic_name)
        self.topic_arn = self.topic['TopicArn']
        self.topic_name = topic_name

        return True

    def create_queue(self, queue_name):
        self.queue = self.sqs.create_queue(QueueName=queue_name)
        self.sqs_arn = self.sqs.get_queue_attributes(QueueUrl=self.queue['QueueUrl'], AttributeNames=['QueueArn'])['Attributes']['QueueArn']

        return True

    def add_policy(self):
        """
        Create/Add security policy to queue to allow topics to get tied to them
        """
        self.policy = None
        try:
            self.policy = json.loads(self.get_policy())
            # Do not bother adding a new policy if there is one in place for this topic already
            if self.topic_name in [s['Sid'] for s in self.policy['Statement']]:
                return True
        except KeyError:
            pass

        if not self.policy:
            self.policy = {
                "Version": "2012-10-17",
                "Id": "{}/SQSDefaultPolicy".format(self.sqs_arn),
                "Statement": [],
            }

        self.policy['Statement'].append({
          "Sid": self.topic_name,
          "Effect": "Allow",
          "Principal": {
            "AWS": "*"
          },
          "Action": "SQS:SendMessage",
          "Resource": self.sqs_arn,
          "Condition": {
            "ArnEquals": {
              "aws:SourceArn": self.topic_arn
            }
          }
        })
        self.sqs.set_queue_attributes(QueueUrl=self.queue['QueueUrl'], Attributes={'Policy': json.dumps(self.policy)})
        return True

    def subscribe_to_topic(self):
        """Subscribe to the topic"""
        sub = self.sns.subscribe(TopicArn=self.topic_arn, Protocol='sqs', Endpoint=self.sqs_arn)
        return sub
        return True

    def get_policy(self):
        return self.sqs.get_queue_attributes(QueueUrl=self.queue['QueueUrl'], AttributeNames=['Policy'])['Attributes']['Policy']

    def delete_message(self, receipthandle):
        self.sqs.delete_message(QueueUrl=self.queue['QueueUrl'], ReceiptHandle=receipthandle)
        return True

    def receive_message(self, MaxNumberOfMessages=3, WaitTimeSeconds=2, VisibilityTimeout=10):
        return self.sqs.receive_message(QueueUrl=self.queue['QueueUrl'],MaxNumberOfMessages=MaxNumberOfMessages, WaitTimeSeconds=WaitTimeSeconds, VisibilityTimeout=VisibilityTimeout)

    def send_message(self, msg, target):
        return self.sns.publish(Message=msg, TopicArn=self.target_list[target], MessageAttributes={'chat_tag': {'DataType': 'String', 'StringValue': self.chat_tag}})

    def register_target(self, topic):
        self.target_list[topic]=re.sub(self.topic_name, topic, self.topic_arn)
        return True

    def delete_queue(self):
        self.sqs.delete_queue(QueueUrl=self.queue['QueueUrl'])

    def delete_topic(self):
        self.sns.delete_topic(TopicArn=self.topic_arn)

    def set_chat_tag(self, my_topic=None, o_topic=None, chat_tag=None):
        # Memoize chat_tag, but update it if the tag recieved is different than the one
        # on record. The idea is the first message published gets to name the chat_tag.
        if self.chat_tag and self.chat_tag!=chat_tag:
                self.chat_tag=chat_tag
                self.tag_set=True

        if my_topic and o_topic:
            now = datetime.now()
            self.chat_tag=(my_topic + '_' + o_topic + '_' + now.strftime("%m%d%Y_%H%M%S"))

        return self.chat_tag
