from app import db

# Your database models should go here.
# Check out the Flask-SQLAlchemy quickstart for some good docs!
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

class User(db.Model):
  user_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(80), unique=True, nullable=False)
  first = db.Column(db.String(80), nullable=False)
  middle = db.Column(db.String(80), default=' ')
  last = db.Column(db.String(80), nullable=False)
  student_type = db.Column(db.String(20), nullable=False)
  class_year = db.Column(db.Integer, nullable=False)
  major = db.Column(db.String(50), nullable=False, default='Undecided')
  sub_school = db.Column(db.String(50), nullable=False)

  club_id = db.Column(db.String(20), db.ForeignKey('club.code'))
  club = db.relationship('Club', backref=db.backref('favorites', lazy=True))

  def __repr__(self):
    return self.username

class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  tag_name = db.Column(db.String(20), nullable=False)

  club_id = db.Column(db.String(20), db.ForeignKey('club.code'))
  club = db.relationship('Club', backref=db.backref('tags', lazy=True))

  def __repr__(self):
    return self.tag_name

class Club(db.Model):
  code = db.Column(db.String(20), primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  description = db.Column(db.Text, nullable=False)

  def __repr__(self):
    return self.name