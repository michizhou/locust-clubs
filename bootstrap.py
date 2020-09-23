import os
import json
from app import db, DB_FILE
from models import *

def create_user():
    new_user = User(username='josh', first='Josh', last='Bergmann',
                    email='jberg@seas.upenn.edu', student_type='Undergraduate',
                    class_year=2024, major='Computer Science', sub_school='SEAS')
    db.session.add(new_user)
    db.session.commit()

def load_data():
    with open('clubs.json') as data_file:
      data = json.load(data_file)
      for entry in data:
        new_club = Club(code=entry['code'], name=entry['name'],
                        description=entry['description'])
        for tag in entry['tags']:
          t = Tag(tag_name=tag)
          new_club.tags.append(t)
        db.session.add(new_club)
      db.session.commit()

# No need to modify the below code.
if __name__ == '__main__':
    # Delete any existing database before bootstrapping a new one.
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    db.create_all()
    create_user()
    load_data()
