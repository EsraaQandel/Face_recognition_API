# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of Barack Obama.
# The result is returned as json. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns:
#
# {
#  "face_found_in_image": true,
#  "is_picture_of_obama": true
# }
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition

from flask import Flask, render_template, request, \
    redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student

from flask import session as login_session
import random
import string
import httplib2
import json
from flask import make_response
import requests

# json_string = json.dumps(known_face_encoding)
#data  = json.loads(json_string)
# Connect to Database and create database session
engine = create_engine(
    'postgresql://postgres:postgres@localhost/list')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Show Home Page
@app.route('/')
def showHome():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        name = request.form['name']
        ID   = request.form['ID']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file,name,ID)

    # If no valid image file was uploaded, show the file upload form:

    else:
        return render_template('Register.html')

@app.route('/attendence', methods=['GET', 'POST'])
def captureIt():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return list_faces_in_image(file)
    # if didn't submit a file take him to form again
    else:
        return render_template('Capture.html')
    

def detect_faces_in_image(file_stream,name,ID):


    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    face_encodings = face_recognition.face_encodings(img)[0]
    face_encodings_list = face_encodings.tolist()
    newStudent = Student(
          name=name,
          encoding= face_encodings_list,
          id=ID)
    ids = []
    students = session.query(Student).all()
    for student in students:
        ids.append(student.id)

    if int(ID) in ids:
        return render_template('duplicate.html')

    else:
        session.add(newStudent)
        session.commit()
        #flash(' %s is Successfully Registered' % (newStudent.name))
        return render_template('registered.html')

def list_faces_in_image(file_stream):
    # create 2 lists to stores all the registered students' encodings and names
    known_face_encodings = []
    known_face_names = []
    # list to store attendence 
    attendence_list = [] 
    students = session.query(Student).all()
    for student in students:
        the_face_encoding = student.encoding
        name = student.name
        known_face_encodings.append(the_face_encoding)
        known_face_names.append(name)

    # Load the uploaded image file
    unknown_image = face_recognition.load_image_file(file_stream)

    # Find all the faces and face encodings in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        name = "Unknown"
     
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            attendence_list.append(name)
            attendence_json = json.dumps(attendence_list)
    if not attendence_list:
        return render_template('notfound.html')
    else:
        return render_template('list.html',items= attendence_list)    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5007, debug=True)
