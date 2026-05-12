from .db import db
from datetime import datetime

class PredictionHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    magnitudo = db.Column(db.Float)
    depth = db.Column(db.Float)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    prediction = db.Column(db.Integer)
    probability = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)