from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

DB_FILE = "clubreview.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_FILE}"
db = SQLAlchemy(app)

from models import *

def get_clubs(club_list):
    club_repo = []
    for club in club_list:
        num_favorites = len(club.favorites)
        club_info = jsonify(name=club.name, code=club.code, desc=club.description,
                            favorites=num_favorites, tags=club.tags)
        club_repo.append(club_info)
    return jsonify(club_repo)

def get_all_clubs():
    clubs = db.session.query(Club).all()
    return get_clubs(clubs)

def add_new_club():
    req = request.get_json()
    new_code, new_name = req.get('code'), req.get('name')
    new_description = req.get('description')
    new_tags = req.get('tags')
    new_club = Club(code=new_code, name=new_name, description=new_description)
    for tag in new_tags:
        t = Tag(tag_name=tag)
        new_club.tags.append(t)
    db.session.add(new_club)
    db.session.commit()
    return "New club has been added!"

@app.route('/')
def main():
    return "Welcome to Penn Club Review!"

@app.route('/api')
def api():
    return jsonify({"message": "Welcome to the Penn Club Review API!."})

@app.route('/api/user/<string:username>')
def show_profile(username):
    user = User.query.filter_by(username=username).first()
    name_parts = [user.first, user.middle, user.last] if user.middle != ' ' else [user.first, user.last] 
    return jsonify(username=user.username, email=user.email, first=user.first,
                   name=' '.join(name_parts), level=user.student_type, 
                   year=user.class_year, major=user.major, school=user.sub_school)

@app.route('/api/clubs', methods=['GET', 'POST'])
def handle_clubs():
    if request.method == 'POST':
        return add_new_club()
    else:
        search_param = request.args.get('search')
        if search_param:
            search_clubs = Club.query.filter_by(Club.name.ilike("%{}%".format(search_param)))
            return get_clubs(search_clubs)
        else:
            return get_all_clubs()

@app.route('/api/clubs/<string:code>', methods=['PATCH'])
def modify_club(code):
    req = request.get_json()
    db.session.query(Club).filter_by(code=code).update(req)
    db.session.commit()
    return "Information for club with code" + code + "has been modified."

@app.route('/api/<string:club>/favorite', methods=['POST'])
def favorite_club(club):
    req = request.get_json()
    new_favorite_username = req.get('user')
    user_club = Club.query.filter_by(name=club).first()
    if new_favorite_username in user_club.favorites:
        return "User has already marked" + club + "as a favorite."
    else:
        user_club.favorites.append(new_favorite_username)
        db.session.commit()
        return "New user has just marked" + club + "as a favorite!"

@app.route('/api/tag_count')
def get_tag_counts():
    tag_counts = []
    tags = db.session.query(Tag).all()
    for tag in tags:
        num_clubs = Tag.query.filter_by(tag_name=tag.tag_name).count()
        tag_info = jsonify(tag=tag.tag_name, count=num_clubs)
        tag_counts.append(tag_info)
    return jsonify(tag_counts)

if __name__ == '__main__':
    app.run()
