from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Usuario %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            'is_active': self.is_active,
            # do not serialize the password, its a security breach
        }

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    city = db.Column(db.String(250))    
    age = db.Column(db.Integer)        
    courses = db.relationship('Course', backref='teacher', lazy=True)

    def __repr__(self):
        return '<Teacher %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            'age': self.age
            # do not serialize the password, its a security breach
        }


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))   
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
        nullable=False) 

    def __repr__(self):
        return '<Course %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description
            # do not serialize the password, its a security breach
        }