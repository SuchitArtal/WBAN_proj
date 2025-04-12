from app import db

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(64), primary_key=True)
    pseudo_identity = db.Column(db.String(256), unique=True, nullable=False)
    hashed_password = db.Column(db.String(256), nullable=False)
    public_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_pseudo_identity = db.Column(db.String(256), db.ForeignKey('users.pseudo_identity', ondelete='CASCADE'), nullable=False)
    session_key = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class ECCKey(db.Model):
    __tablename__ = 'ecc_keys'

    user_id = db.Column(db.String(64), db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    private_key = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
