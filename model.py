
from flask_sqlalchemy import SQLAlchemy
import arrow
db = SQLAlchemy()

# time-zone can be dynamic depending on user
tz = 'local'

class Chatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    message = db.Column(db.String(120))
    ip = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime)

    def __init__(self, username, message, ip, timestamp):
        self.username = username
        self.message = message
        self.ip = ip
        self.timestamp = timestamp

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id'         : self.id,
           'username'   : self.username,
           'message'    : self.message,
           'ip'         : self.ip,
           'timestamp'  : arrow.get(self.timestamp).replace(tzinfo=tz).humanize()
       }

    def __repr__(self):
        return '<Chatter %r>' % self.username

        