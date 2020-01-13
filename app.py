from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# Doctor Class/Model
class Doctor(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  spcl = db.Column(db.String(200))
  __tablename__ = 'doctor'
  clinics = relationship('Clinic', secondary = 'practice')
  

  def __init__(self, name, spcl):
    self.name = name
    
    self.spcl = spcl

# Product Schema
class DoctorSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'spcl')

# Init schema
doctor_schema = DoctorSchema()
doctors_schema = DoctorSchema(many=True)


#Create a doctor 
@app.route('/doctor', methods = ['POST'])
def add_product():
    name = request.json['name']
    spcl = request.json['spcl']
    

    new_doctor = Doctor(name, spcl)
    db.session.add(new_doctor)
    db.session.commit()
    return doctor_schema.jsonify(new_doctor)

#Get all doctor
@app.route('/doctors', methods=['GET'])
def get_doctors():
    all_doctors = Doctor.query.all()
    print(all_doctors)
    result = doctors_schema.dump(all_doctors)
    print(result)
    return jsonify(result)



#Get single product
@app.route('/doctor/<id>', methods=['GET'])
def get_doctor(id):
    doctor= Doctor.query.get(id)
    
    return doctor_schema.jsonify(doctor)


# Clinic Class/Model
class Clinic(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  adr = db.Column(db.String(200))
  __tablename__ = 'clinic'
  doctors = relationship('Doctor', secondary = 'practice')
  

  def __init__(self, name, adr):
    self.name = name
    
    self.adr = adr

# CLinic Schema
class ClinicSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'adr')

# Init schema
clinic_schema = ClinicSchema()
clinics_schema = ClinicSchema(many=True)


#Create a clinic
@app.route('/clinic', methods = ['POST'])
def add_clinic():
    name = request.json['name']
    adr = request.json['adr']
    

    new_clinic = Clinic(name, adr)
    db.session.add(new_clinic)
    db.session.commit()
    return clinic_schema.jsonify(new_clinic)

#Get all clinics
@app.route('/clinics', methods=['GET'])
def get_clinics():
    all_clinics = Clinic.query.all()
    
    result = clinics_schema.dump(all_clinics)
    
    return jsonify(result)



#Get single clinic
@app.route('/clinic/<id>', methods=['GET'])
def get_clinic(id):
    clinic= Clinic.query.get(id)
    
    return clinic_schema.jsonify(clinic)


class Practice(db.Model):
    __tablename__ = 'practice'
    doctor_id =  db.Column(db.Integer, ForeignKey('doctor.id'), primary_key = True)
    clinic_id = db.Column(db.Integer, ForeignKey('clinic.id'), primary_key = True)
    price = db.Column(db.Integer)

    def __init__(self, doctor_id, clinic_id, price):
        self.doctor_id = doctor_id
        self.clinic_id = clinic_id
        self.price = price 

# CLinic Schema
class PracticeSchema(ma.Schema):
  class Meta:
    fields = ('doctor_id', 'clinic_id','price')

# Init schema
practice_schema = PracticeSchema()
practices_schema = PracticeSchema(many=True)


#Create a Practice
@app.route('/practice', methods = ['POST'])
def add_practice():
    doctor_id = request.json['doctor_id']
    clinic_id = request.json['clinic_id']
    price = request.json['price']

    new_practice = Practice(doctor_id, clinic_id, price)
    db.session.add(new_practice)
    db.session.commit()
    return practice_schema.jsonify(new_practice)
    
@app.route('/practices', methods=['GET'])
def get_practices():
    
    all_practices = Practice.query.all()
    
    result = practices_schema.dump(all_practices)
    '''
    for x in Practice.query.filter(Practice.doctor_id == Doctor.id , Practice.clinic_id == Clinic.id ).all():
	    print("Doctor -> {} Clinic-> {} ".format(x.doctor.name, x.clinic.name ))
        #print(x)
    '''

    return jsonify(result)
# Run Server
if __name__ == '__main__':
  app.run(debug=True)