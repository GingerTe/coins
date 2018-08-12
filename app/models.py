from . import db


class CoinGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    shortname = db.Column(db.String(100), unique=True)

    coins = db.relationship('Coin', lazy='select',
                            backref=db.backref('group', lazy='joined'))
    parent_id = db.Column(db.ForeignKey('coin_group.id'))

    parent = db.relationship('CoinGroup', remote_side=id, backref='children')
    order = db.Column(db.Integer, nullable=False, server_default='0')

    def get_root(self, group=None):
        group = group or self

        if not group.parent:
            return group
        else:
            return self.get_root(group.parent)

    @classmethod
    def get_all_hierarchical(cls, parent_id=None, with_parent_duplication=False):
        res = []
        for coin_group in cls.query.filter_by(parent_id=parent_id):
            if not coin_group.children:
                res.append({
                    'id': coin_group.id,
                    'text': coin_group.name
                })
            else:
                if with_parent_duplication:
                    res.append({
                        'id': coin_group.id,
                        'text': coin_group.shortname,
                    })
                res.append({
                    'id': coin_group.id,
                    'text': coin_group.shortname if not with_parent_duplication else '',
                    'children': cls.get_all_hierarchical(coin_group.id, with_parent_duplication)
                })
        return res


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
