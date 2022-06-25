import os
import datetime
from flask import Flask, request, jsonify, render_template
from peewee import *
from playhouse.shortcuts import model_to_dict
from app.views import views

app = Flask(__name__)
app.register_blueprint(views)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
)
print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post/<id>', methods=['DELETE'])
def delete_time_line_post(id):
    post_delete = TimelinePost.get(TimelinePost.id == id)
    post_delete.delete_instance()
    return jsonify({"message":"TimelinePost deleted!"})

@app.route('/timeline')
def timeline():
    timeline_posts = [model_to_dict(p) for p in TimelinePost.select().order_by(TimelinePost.
    created_at.desc())]
    return render_template('timeline.html', title="Timeline", posts= timeline_posts)