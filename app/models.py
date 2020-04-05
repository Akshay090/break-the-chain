from app import db, ma


class User(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    MobileNo = db.Column(db.String(30), index=True)
    State_Id = db.Column(db.Integer, db.ForeignKey('state.Id'))


class State(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    State = db.Column(db.String(120), index=True, unique=True)
    Confirmed = db.Column(db.String(10))
    Cured = db.Column(db.String(10))
    Dead = db.Column(db.String(10))
    Users = db.relationship('User', backref='states', lazy=True)


class News(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.Text)
    Description = db.Column(db.Text)


class StateSchema(ma.ModelSchema):
    class Meta:
        model = State


class UserSchema(ma.ModelSchema):
    States = ma.Nested(StateSchema, many=True)

    class Meta:
        model = User


class NewsSchema(ma.ModelSchema):
    class Meta:
        model = News
