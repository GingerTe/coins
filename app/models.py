from . import db


class CoinGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    shortname = db.Column(db.String(100), unique=True)

    coins = db.relationship('Coin', lazy='select',
                            backref=db.backref('group', lazy='joined'))
    parent_id = db.Column(db.ForeignKey('coin_group.id'))

    parent = db.relationship('CoinGroup', remote_side=id, backref='children')


class Mint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    abbr = db.Column(db.String(10), unique=True)

    coins = db.relationship('Coin', lazy='select',
                            backref=db.backref('mint', lazy='joined'))


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer, index=True)
    mint_id = db.Column(db.Integer, db.ForeignKey('mint.id'))
    description = db.Column(db.Text)
    description_url = db.Column(db.Text)
    num = db.Column(db.Text)
    date = db.Column(db.Date)
    is_got = db.Column(db.Integer, nullable=False, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('coin_group.id'))
