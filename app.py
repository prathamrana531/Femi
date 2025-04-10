#from flask_ngrok import run_with_ngrok
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from werkzeug.utils import secure_filename
import os

from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask import flash
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:@localhost/crop'
db =SQLAlchemy(app)
app.config['SECRET_KEY'] = 'super secret key'


class Users(db.Model):
    ID= db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(100),unique=True, nullable=False)
    email= db.Column(db.String(100), nullable=False)
    password= db.Column(db.String(100), nullable=False)
    
model_path = "soilClassify.h5"
SoilNet = load_model(model_path)

alluvialsoil_desc = """Alluvial soils support more than 40% of India's population by providing the most productive agricultural lands. The soil is porous because of its loamy nature. The proportion of potash, phosphoric acid and alkalies are adequate in alluvial soils. 
Crops: rice, wheat, sugarcane, tobacco, cotton, jute, maize, oilseeds, vegetables and fruits"""

blacksoil_desc = """Black soils when seen in uplands are considered to be present with low fertility while those in the valleys are very fertile. The black colour arises due to the presence of a small proportion of titaniferous magnetite or iron and black constituents of the parent rock. 
Crops: cotton (best suited), wheat, jowar, linseed, Virginia, tobacco, castor, sunflower, millets"""

desertsoil_desc = """Desert soil is mostly sandy soil (90–95%) found in low-rainfall regions. It has a low content of nitrogen and organic matter with very high calcium carbonate and phosphate, thus making it infertile. The amount of calcium is 10 times higher in the lower layer than in the topsoil."""

redsoil_desc = """Red soils originate from parent rocks which are crystalline and metamorphic in nature like acid granites, gneisses and quartzites. On the uplands, the red soils are poor, gravelly and porous but in the lower areas, they are rich, deep dark and fertile. The red color is due to the presence of iron oxide. 
Crops: cotton, wheat, rice, pulses, millets, tobacco, oil seeds, potatoes and fruits"""

cindersoil_desc = """Cinders are crushed volcanic rocks formed during the cooling and depressurization process of a volcanic eruption. Their bubble-like cavities, called vesicles, allow them to float in water. Depending on chemical composition, cinders can appear red, black, or brown. Adding cinders to topsoil yields a product called cinder soil."""

def predict_model(img_path, model):
    img = load_img(img_path, target_size=(224, 224))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, axis = 0)
    result = np.argmax(model.predict(img))
    print(result)
    return result

@app.route("/predictSoil", methods=["GET", "POST"])
def predictSoil():
    print("Welcome")
    if request.method == "POST":
        uploadedImg = request.files["image"]
        nameUploadedImg = uploadedImg.filename
        print("You have uploaded ", nameUploadedImg)

        uploadedImg_path = os.path.join('static/uploaded_by_user', nameUploadedImg)
        uploadedImg.save(uploadedImg_path)
        
        print("Predicting soil.....")
        result = predict_model(uploadedImg_path, SoilNet)
        
        if (result == 0):
            return render_template("afterUploadSoil.html", soil_type='Alluvial', user_image_path=uploadedImg_path, desc=alluvialsoil_desc)
        elif (result == 1):
            return render_template("afterUploadSoil.html", soil_type='Black', user_image_path=uploadedImg_path, desc=blacksoil_desc)
        elif result == 2:
            return render_template("afterUploadSoil.html", soil_type='Desert', user_image_path=uploadedImg_path, desc=desertsoil_desc)
        elif result == 3:
            return render_template("afterUploadSoil.html", soil_type='Red', user_image_path=uploadedImg_path, desc=redsoil_desc)
        elif result == 4:
            return render_template("afterUploadSoil.html", soil_type='cinder', user_image_path=uploadedImg_path, desc=cindersoil_desc)    
        return "An error occurred"
    return render_template("uploadSoil.html")

@app.route("/predictCrop", methods=["GET", "POST"])
def predictCrop():
    if request.method == "POST":
        uploadedImg = request.files["image"]
        nameUploadedImg = uploadedImg.filename
        print("You have uploaded ", nameUploadedImg)

        uploadedImg_path = os.path.join('static/uploaded_by_user', nameUploadedImg)
        uploadedImg.save(uploadedImg_path)

        print("Predicting crop.....")
        result = predict_model(uploadedImg_path, SoilNet)
        
        if (result == 0):
            return render_template("alluvialCrop.html")
        elif (result == 1):
            return render_template("blackCrop.html")
        elif result == 2:
            return render_template("desertCrop.html")
        elif result == 3:
            return render_template("redCrop.html")
        elif result == 4:
            return render_template("cinderCrop.html")
        return "An error occurred"
    return render_template("uploadCrop.html")

@app.route("/" , methods=["GET", "POST"] )
def login():
    if(request.method=='POST'):
        mail = request.form.get('email')
        password = request.form.get('password')
        existing_user =  Users.query.filter_by(email=mail ).first()
        print (existing_user);
        if(existing_user):
            if(existing_user.password==password):
                return render_template("homepage.html",);
            else:
                flash("Wrong password")
                return render_template("login.html",email=mail,pa="");
                
        else:
            flash("No account exist with provided email");
            return render_template("login.html");       
    return render_template("login.html")


# @app.route("/forget")
# def forget():
#     email = request.form.get('email')
#     existing_user =  Users.query.filter_by(email=email ).first()
#     print (existing_user);
#     if(existing_user):
#         password = request.form.get('password')
        
# return render_template("login.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    # username="",
    # email="",
    # password="",
    # cpassword=""
    if(request.method=='POST'):
        '''Add entry to the database'''
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
       
        existing_user = Users.query.filter(
            Users.username == username ).first()
        print(existing_user);
        existing_mail = Users.query.filter(
            Users.email == email ).first()
          
        if  existing_user:
            flash("Username exist. Please change your username");
            username="";
            return render_template("register.html",name=username,mail=email, pa=password,cpass=cpassword)  
        
        if  existing_mail:
            flash("Account with email adrees exist. Please change your email or login with existing email.");
            email="";
            return render_template("register.html",name=username,mail=email, pa=password,cpass=cpassword)

        if(password==cpassword and password!=""):
            entry = Users(username=username,email = email,password=password )
            print(Users.email," ",Users.password)
            db.session.add(entry)
            db.session.commit()
            # flash("Registration Completed")
            return render_template("homepage.html")
        else:
            flash("Password not matched")            
            print("Please re-enter passwords")
            password=""
            cpassword=""
            return render_template("register.html",name=username,mail=email, pa=password,cpass=cpassword)
    return render_template("register.html")

@app.route("/home")
def home():
    return render_template("homepage.html")

@app.route("/intuition")
def intuition():
    return render_template("intuition.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/uploadCrop")
def uploadCrop():
    return render_template("uploadCrop.html")

@app.route("/log")
def log():
    return render_template("login.html")

@app.route("/uploadSoil")
def uploadSoil():
    return render_template("uploadSoil.html")

#@app.route("/crop")
#def crop_suggestion():
#    return render_template("afterUploadCrop.html")

#@app.route("/soil")
#def soil_suggestion():
#   return render_template("afterUploadSoil.html")
#app.run()

if __name__ == '__main__':
    app.run(debug=True)