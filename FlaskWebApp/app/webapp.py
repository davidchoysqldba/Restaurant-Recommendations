import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import request


#basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://restuser:restuser@rest_recomm_dev/restaurantdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


class RecommendationBoro(db.Model):
    __tablename__ = 'recommendation_boro'
    recommendation_id = db.Column(db.Integer, primary_key=True)
    boro = db.Column(db.String(20))
    dba = db.Column(db.String(200))
    grade_average = db.Column(db.Float)
    grade_count = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    is_latest = db.Column(db.Boolean)

    def __repr__(self):
        return "<RecommendationBoro(recommendation_id=%d, boro='%s', dba='%s')>" % (self.recommendation_id, self.boro, self.dba)

    def to_json(self):
        json_boro = {
            'boro': self.boro,
            'dba': self.dba,
            'grade_average': self.grade_average,
            'grade_count': self.grade_count,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }
        return json_boro

class RecommendationZipcode(db.Model):
    __tablename__ = 'recommendation_zipcode'
    recommendation_id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(10))
    boro = db.Column(db.String(20))
    dba = db.Column(db.String(200))
    grade_average = db.Column(db.Float)
    grade_count = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    is_latest = db.Column(db.Boolean)

    def __repr__(self):
        return "<RecommendationBoro(recommendation_id=%d, zipcode=%s, boro='%s', dba='%s')>" % (self.recommendation_id, self.zipcode, self.boro, self.dba)

    def to_json(self):
        json_zipcode = {
            'zipcode': self.zipcode,
            'boro': self.boro,
            'dba': self.dba,
            'grade_average': self.grade_average,
            'grade_count': self.grade_count,
            'date_created': self.date_created,
            'date_modified': self.date_modified
        }
        return json_zipcode


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('get_recommend_boro'))


@app.route('/recommend_boro')
def get_recommend_boro():
    boros = RecommendationBoro.query.filter_by(is_latest=True)
    return render_template('recommend_boro.html', boros=boros)


@app.route('/recommend_zipcode')
def get_recommend_zipcode():
    zipcodes = RecommendationZipcode.query.filter_by(is_latest=True)
    return render_template('recommend_zipcode.html', zipcodes=zipcodes)


@app.route('/api/zipcode')
def get_zipcode():
    zipcodes = RecommendationZipcode.query.filter_by(is_latest=True)
    return jsonify({'zipcodes': [zipcode.to_json() for zipcode in zipcodes]})


@app.route('/api/boro')
def boro():
    boros = RecommendationBoro.query.filter_by(is_latest=True)
    return jsonify({'boros': [boro.to_json() for boro in boros]})
