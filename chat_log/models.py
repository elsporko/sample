from datetime import datetime
from config import db, ma

class TwoCans(db.Model):
    __tablename__ = 'chat_log'
    chat_id = db.Column(db.Integer, primary_key = True)
    # TODO - Validate lengths in application so they don't cause the db to crash
    recipient = db.Column(db.String(25))
    sender = db.Column(db.String(25))
    text = db.Column(db.Text)
    tag = db.Column(db.String(25))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class TwoCanSchema(ma.ModelSchema):
    class Meta:
        model = TwoCans
        sqla_session = db.session
