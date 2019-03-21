import os
from config import db
from models import TwoCans

# Initial data
CHATS = [
    { "sender": "elsporko", "recipient": "homerJ", "text": "My cat's breath smells like catfood", "tag": "chat1"},
    { "sender": "homerJ", "recipient": "elsporko", "text": "Increase my killing power, eh?", "tag": "chat1" },
    { "sender": "elsporko", "recipient": "homerJ", "text": "There once was a man from an island off Massachusetts", "tag": "chat1"}
]

# Delete existing db file
if os.path.exists('twocans.db'):
    os.remove('twocans.db')

# Create fresh db
db.create_all()

# Iterate over structure and build data
for chat in CHATS:
    print("chat: ", chat)
    c = TwoCans(sender=chat['sender'], recipient=chat['recipient'], text=chat['text'], tag=chat['tag'])
    db.session.add(c)

db.session.commit()
