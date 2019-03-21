"""
This is the twocans module and supports all the REST actions for chat_log
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort
from config import db
from models import TwoCans, TwoCanSchema


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def read_all():
    """
    This function responds to a request for /api/chat_log
    with the complete lists of chat logs
    :return:        json string of list of chat logs
    """
    # Create the list of chat logs from our data
    chats = TwoCans.query.order_by(TwoCans.timestamp).all()
    chat_schema = TwoCanSchema(many=True)
    return chat_schema.dump(chats).data


def get_by_tag(tag_id):
    chats = TwoCans.query.filter(TwoCans.tag==tag_id).all()
    chat_schema = TwoCanSchema(many=True)
    return chat_schema.dump(chats).data

def get_by_name(sender):
    chats = TwoCans.query.filter(TwoCans.sender==sender).all()
    chat_schema = TwoCanSchema(many=True)
    return chat_schema.dump(chats).data

def create(chat_log):
    """
    This function creates a new chat_log in the people structure
    based on the passed in chat_log data
    :param chat_log:  chat_log to create in people structure
    :return:        201 on success, 406 on chat_log exists
    """
    sender    = chat_log.get("sender", None)
    recipient = chat_log.get("recipient", None)
    tag       = chat_log.get("tag", None)
    text      = chat_log.get("text", None)

    schema = TwoCanSchema()
    new_chat = schema.load(chat_log, session=db.session).data

    db.session.add(new_chat)
    db.session.commit()

    return schema.dump(chat_log).data, 201

def delete(tag_id):
    """
    This function deletes a chat_log from the people structure
    :param lname:   last name of chat_log to delete
    :return:        200 on successful delete, 404 if not found
    """

    for d in [k for k in get_by_tag(tag_id)]:
        chat = TwoCans.query.filter(TwoCans.tag == tag_id).one_or_none()

        if chat is not None:
            db.session.delete(chat)
            db.session.commit()
