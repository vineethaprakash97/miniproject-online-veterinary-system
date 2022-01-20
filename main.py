import db
from flask import Flask,render_template,request,session,redirect
from flask_mail import Mail,Message
import mysql.connector
import json
from werkzeug import secure_filename
import os
#from chatterbot import ChatBot
# from chatterbot.trainers import ListTrainer
from datetime import datetime, timedelta
import difflib
# import datetime
# import dateutil.relativedelta
app=Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'petsake123@gmail.com'
app.config['MAIL_PASSWORD'] = 'Pet@123456789'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail=Mail(app)
app.secret_key="admin"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


@app.route("/")
def main():
	

	# d = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d")
	# d2 = d - dateutil.relativedelta.relativedelta(months=3) 
	# print(d2)
	return render_template("index.html")

@app.route("/login",methods=["GET","POST"])
def login():
	username=request.form.get('txtuname')
	password=request.form.get('txtpasswd')
	r=db.dblogsel(username,password)
	
	print(r)
	if r==False:
		return render_template("message.html",message="Invalid username or password",route="/login1")
	elif r[0][0] == "normalusers":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("showusernotifications")
	elif r[0][0] == "clinic":
		status=db.getclinicstatus(username)
		if(status == 'Requested'):
			return render_template("message.html",message="your account is not verified yet",route="/login1")
		elif(status == 'Reject'):
			return render_template("message.html",message="sorry,your account is rejected",route="/login1")
		else:
			session['useremail']=username
			session['usertype']=r[0][0]
			return redirect("showclinichome")
	elif r[0][0] == "doctor":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("doctorhome")
	elif r[0][0] == "attender":
		session['useremail']=username
		session['usertype']=r[0][0]
		return render_template("attender/home.html")
	elif r[0][0] == "li":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("lihome")
	elif r[0][0] == "admin":
		session['useremail']=username
		session['usertype']=r[0][0]
		return redirect("showadminhome")
	elif r[0][0] == "cattlefarmers":
		session['useremail']=username 
		session['farmid']=db.getfarmid(username)
		session['usertype']=r[0][0]
		return redirect("showcattlefarmhome")

@app.route("/showusernotifications")
def showusernotifications():
	notification=db.viewnotifications()
	return render_template("user/notification.html",data=notification)
			
# my_bot = ChatBot('MyBot')
# trainer = ListTrainer(my_bot)
data={"hi":"hello welcome","hello":"hai","what is your name?,who are you?":"iam AI bot ","how are you?":"iam good",
"what is the best common cat food?,what can cats eat?,what can cats eat besides cat food?" : 'salmon,trout,chicken,fish,beef,eggs,blueberries',
	 'what should i feed my cat?' : 'salmon,trout,chicken,fish,beef,eggs,blueberries',
	 "vaccinations for cat?":"FVRCP Also called “the feline distemper vaccine which protects against three feline viruses rhinotracheitis, calicivirus and panleukopenia",
	 "cat vaccination schedule?":"6 to 10 weeks old=FVRCP,11 to 14 weeks old=FVRCP and FeLv,15 weeks old=fvcp,felv ,rabies",
	 "diseases of cat?":"heartworm,rabies,ringworm,worms,respiratory infections,felv",
	 "symptoms of a sick cat":"vomiting,diarrhoea,foul smell,behavioral changes","what is the best common dog food?,what shoul i feed my dog":"carrots,peanut butter,meat,fish,egg,bread,tomato,oatmeal,rice","dog food?":"pedigree",
	 "vaccinations for dog":"parvovirus,coronavirus,rabies","common vaccinations for dog":"parvovirus,coronavirus,rabies","vaccination schedule of dog":"6 to 16 week=distemper,parvovirus,3 to 4 weeks=parainfluenza,9 weeks=lymedisease,1 year=rabies",
	 "common diseases of dog":"diabetes,kennel cough,heart worm,parvovirus,ringworm","symptoms of sick dog":"vomiting,diabetes,diarrhoea,exessive thirst,urination,behavioral changes,red gums,runny eyes or nose,weight loss",

	 "common food of birds?":"plant leafs,nuts,fruits","pigeon  food?":"Millet, cracked corn, wheat, milo, Nyjer, buckwheat, sunflower hearts","dove food?":"Millet, cracked corn, wheat, milo, Nyjer, buckwheat, sunflower hearts","humming bird food?":"plant nectar,sugar solution,small insects","vaccination of bird?":"polymavirus",
	 "squirrel food":"any fruits,vegetables,nuts","squirrel vaccination":"no vaccination"
}
# trainer.train([
#               'what cm of rainfall is required for the growth of rice?',
#               'it is above 100 cm',
#               'what cm of rainfall is required for the growth of wheat?',
#               'it is between 50-75 cm',
#               'what cm of rainfall is required for the growth of cotton?',
#               'it is between 50-100 cm',

#               'which is the best picking time of cotton?',
#               'it is during frost free days',
#               'which is the best picking time of jute?',
#               'it is during hot and humid climate',
#               'what degree of temperature is required for the growth of jute?',
#               'it requires 30 degree celsius',
#               'which type of soil is required for the growth of jute?',
#               'well drained fertile loamy soil is required',
#               'which type of soil is required for the growth of cotton?',
#               'loamy and black soil is required',
#               'which type of soil is required for the growth of sugarcane?',
#               'black soil is required',
#               'which type of soil is required for the growth of citrus fruit?',
#               'black soil is required',
#               'which type of soil is required for the growth of tapioca?',
#               'laterite soil is required',
#               'which type of soil is required for the growth of cashew?',
#               'laterite soil is required',
#               'which type of soil is required for the growth of rice?',
#               'black soil is required',
#               'what cm of rainfall is required for the growth of jute?',
#               'it is near about 150 cm',
#               'what degree of temperature is required for the growth of rice?',
#               'it is above 25 degree celsius',
#               'what degree of temperature is required for the growth of wheat?',
#               'it is  15 degree celsius',
#               'what degree of temperature is required for the growth of cotton?',
#               'it is more than 21 degree celsius',
#               'what degree of temperature is required for the growth of jute?',
#               'it requires 30 degree celsius',
#               'what is the tip of growing raddish?',
#               'sow 4 weeks after last frost,and throughout summer and harvest after a month.sow directly into the ground for quick growth and colorful veg',
           
#               'what is the tip of growing beetroot?',
#               'sow march to july and harvest from may to september.sow directly into the moist soil and thin seedlings to about 5cm apart for quick growth and colorful veg',
#               'what is the tip of growing apple?',
#               'well drained soil and top tip prune every winter to stimulate growth and get the best crops',
#               'what is the tip of growing potato?',
#               'sow late feb or mar.harvest jul to sep.grow in ground or bags to stimulate growth of potatoes',
#               'what is the tip of growing carrot?',
#               'sow in early spring to late summer',
#               'how do you do?',
#               'how are you?',
#               'i\'m cool.',
#               'fine, you?',
#               'always cool.',
#               'i\'m ok',
#               'glad to hear that.',
#               'i\'m fine',
#               'glad to hear that.',
#               'i feel awesome',
#               'excellent, glad to hear that.',
#               'not so good',
#               'hi',
#               'sorry to hear that.',
#               'what\'s your name?',
#               'i\'m AI Bot. ask me a question, please.'])
# math_talk_1 = ['pythagorean theorem',
#                'a squared plus b squared equals c squared.']
# math_talk_2 = ['law of cosines',
#                'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)']

# list_trainer = ListTrainer(my_bot)
# for item in (small_talk):
#     list_trainer.train(item)
#     print(item)
# print(list_trainer)
# print(my_bot.get_response("hi"))
@app.route("/showchatbot",methods=["GET","POST"])
def index():
  return render_template("chat.html")
@app.route("/send",methods=["GET","POST"])
def send():
  temp={}
  response=""
  message=request.form["message"]
  for key, value in data.items():
  	a=message
  	b=key
  	seq = difflib.SequenceMatcher(None,a,b)
  	d = seq.ratio()*100
  	if(d >= 50):
  		temp[key]=d
  print(temp)
  # print(max(temp.iterkeys(), key=lambda k: temp[k]))
  maxratio=0
  maxkey=""
  for key, value in temp.items():
  	if(maxratio < value):
  		maxratio=value
  		maxkey=key
  if(maxkey == ""):
  	return "I don't understand"
  else:
  	return str(data[maxkey])
  # response=my_bot.get_response(str(message))
  # print(response)

  		# return str(value)

@app.route("/login1")
def login1():
	return render_template("login.html")

@app.route("/saveuserreg",methods=['GET','POST'])	
def saveuserreg():
	name=request.form['txtname']
	hname=request.form['txthname']
	state=request.form['state']
	district=request.form['district']
	place=request.form['txtplace']
	pincode=request.form['txtpincode']
	dob=request.form['txtdob']
	phone=request.form['txtphn']
	email=request.form['txtemail']
	password=request.form['txtpassword']
	category=request.form['category']
	ques=request.form['txtquestion']
	ans=request.form['txtans']
	db.saveuser(name,hname,state,district,place,pincode,dob,phone,email,password,category,ques,ans)
	if category =='cattlefarmers':
		return render_template("message.html",message="Registration Successfull",route="/login1")
	else:
		return render_template("message.html",message="Registration Successfull",route="/login1")

@app.route("/showuserreg")
def showuserreg():
	state=db.dbstate()
	
	return render_template("userreg.html",state=state)	

@app.route("/showuserhome")
def showuserhome():
	return render_template("user/home.html")	

@app.route("/showadminhome")
def showadminhome():
	return render_template("admin/adminform.html")


@app.route("/saveclinicreg",methods=['GET','POST'])	
def saveclinicreg():
	file = request.files['file']
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	name=request.form.get('txtclname')
	reg=request.form.get('txtclregnum')
	place=request.form.get('place')
	district=request.form.get('district')
	state=request.form.get('state')
	phone=request.form.get('txtclphn')
	pincode=request.form.get('txtpin')
	email=request.form.get('txtclemail')
	govform=request.form.get('govform')
    
	txtname=request.form.get('txtname')
	address=request.form.get('address')
	txtphn=request.form.get('txtphn')
	password=request.form['txtpswrd']
	ques=request.form['txtquestion']
	ans=request.form['txtans']
	db.saveclinic(name,reg,place,district,state,phone,pincode,email,govform,txtname,address,txtphn,password,ques,ans,filename)
	return render_template("message.html",message="Registration Successfull",route="/login1")	





@app.route("/showclinicreg")
def showclinicreg():
	state=db.dbstate()
	return render_template("clinicregistration.html",state=state)	

@app.route("/showclinichome")
def showclinichome():
	return render_template("clinic/home.html")	

@app.route("/savefarmreg",methods=['GET','POST'])	
def savefarmreg():
	file = request.files['file']
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	name=request.form.get('txtfname')
	state=request.form.get('state')
	district=request.form.get('district')
	place=request.form.get('txtplace')
	year=request.form.get('txtyear')
	regno=request.form.get('txtfregnum')
	phone=request.form.get('txtphn')
	email=request.form.get('txtemail')
	session["farmid"]=db.savefarm(name,state,district,place,year,regno,phone,email,filename,session["useremail"])
	return render_template("message.html",message="Registration Successfull",route="/showcattlefarmhome")

@app.route("/showfarmreg")
def showfarmreg():
	state=db.dbstate()
	return render_template("cattlefarmer/cattlefarmreg.html",state=state)	

@app.route("/showcattlefarmhome")
def showcattlefarmhome():
	return render_template("cattlefarmer/home.html")	

@app.route("/savefarmanimal",methods=['GET','POST'])	
def savefarmanimal():
	species=request.form.get('species')
	breed=request.form.get('breed')
	no=request.form.get('txtno')
	datee=request.form.get('txtdate')
	db.savefarmanimal(species,breed,no,datee,session["farmid"])
	return render_template("message.html",message="Added Successfully",route="/showcattlefarmhome")

@app.route("/showfarmanimal")
def showfarmanimal():
	species=db.dbspecies()
	return render_template("cattlefarmer/addfarmanimal.html",species=species)	




@app.route("/saveuserpetdetails",methods=['GET','POST'])	
def saveuserpetdetails():

	file = request.files['file']
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	pname=request.form.get('txtpname')
	name=request.form.get('species')
	breed=request.form.get('breed')
	other=request.form.get('txtother')
	gender=request.form.get('gender')
	age=request.form.get('txtage')
	weekmonth=request.form.get('txtweekmonth')
	description=request.form.get('txtdesc')
	d=""
	if(weekmonth == "weeks"):
		d = datetime.today() - timedelta(days=(int(age)*7))
	elif(weekmonth == "months"):
		d = datetime.today() - timedelta(days=(int(age)*30))
	print(d)
	db.saveuserpetdetails(pname,name,breed,other,gender,age,weekmonth,description,filename,session["useremail"])
	return render_template("message.html",message="Success",route="/showuserhome")

@app.route("/showuserpetdetails")
def showuserpetdetails():
	pname=db.dbpname(session["useremail"])
	petid=request.args.get("petid")
	return render_template("user/userpetdetails.html",pname=pname,petdetails=db.getpetdetails(petid))	

@app.route("/showmanagepets")
def showmanagepets():
	species=db.dbspecies()
	pname=db.dbpname(session["useremail"])
	return render_template("user/showmanagepets.html",pname=pname,species=species)

@app.route("/showpets",methods=["GET","POST"])
def showpets():
	data=db.getpetlist(session["useremail"])
	return render_template("user/viewpets.html", petlist=data)

@app.route("/showeditpets",methods=["GET","POST"])
def showeditpets():
	petid=request.args.get("petid")
	data=db.petdetails(petid,session["useremail"])
	return render_template("user/editpets.html",data=data[0],species=db.dbspecies())

@app.route("/showviewmore",methods=["GET","POST"])
def showviewmore():
	petid=request.args.get("petid")
	res=db.getviewmore(petid)
	res1=db.getviewmoreb(petid)
	print(res[0])
	return render_template("user/viewmore.html",data=res[0],data1=res1[0])



@app.route("/delpets",methods=["GET","POST"])
def deletepets():
	petid=request.form.get('petid')
	db.delpets(petid)
	return "ok"

@app.route("/saveeditpet",methods=["GET","POST"])
def saveeditpet():
	filename=""
	file = request.files.get('file')
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	pname=request.form.get('txtpname')
	petid=request.form.get('petid')
	name=request.form.get('species')
	breed=request.form.get('breed')
	other=request.form.get('txtother')
	gender=request.form.get('gender')
	age=request.form.get('txtage')
	weekmonths=request.form.get('txtweekmonth')
	description=request.form.get('txtdesc')
	# if(filename == ""):
	# 	db.editpets(pname,name,breed,other,gender,age,description,session["useremail"])
	# else:
	db.editpets(petid,pname,name,breed,other,gender,age,weekmonths,description,session["useremail"],filename)
	return render_template("message.html",message="Updated Successfully",route="/showuserhome")

@app.route("/saveeditfarm",methods=["GET","POST"])
def saveeditfarm():
	filename=""
	file = request.files.get('file')
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	fname=request.form.get('txtfname')
	state=request.form.get('state')
	district=request.form.get('district')
	place=request.form.get('txtplace')
	yearr=request.form.get('txtyear')
	regnum=request.form.get('txtfregnum')
	phone=request.form.get('txtphn')

	# if(filename == ""):
	# 	db.editpets(pname,name,breed,other,gender,age,description,session["useremail"])
	# else:
	db.editfarm(fname,state,district,place,yearr,regnum,phone,session["useremail"],filename)
	return render_template("message.html",message="Updated Successfully",route="/showcattlefarmhome")

@app.route("/showfarmedit",methods=["GET","POST"])
def showfarmedit():
	data=db.farmdetails(session["useremail"])
	return render_template("cattlefarmer/editfarm.html",data=data[0],state=db.dbstate())

@app.route("/saveuseredit",methods=["GET","POST"])
def saveuseredit():
	name=request.form.get('txtname')
	hname=request.form.get('txthname')
	state=request.form.get('state')
	district=request.form.get('district')
	place=request.form.get('txtplace')
	pincode=request.form.get('txtpincode')
	dob=request.form.get('txtdob')
	phone=request.form.get('txtphn')
	db.edituser(name,hname,state,district,place,pincode,dob,phone,session["useremail"])
	return render_template("message.html",message="Updated Successfully",route="/showuserhome")

@app.route("/showuseredit",methods=["GET","POST"])
def showuseredit():
	data=db.userdetails(session["useremail"])
	return render_template("user/editprofile.html",data=data[0],state=db.dbstate())

@app.route("/showfarmeredit",methods=["GET","POST"])
def showfarmeredit():
	data=db.userdetails(session["useremail"])
	return render_template("cattlefarmer/editprofile.html",data=data[0],state=db.dbstate())

@app.route("/savedoctoredit",methods=["GET","POST"])
def savedoctoredit():
	filename=""
	file = request.files.get('file')
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	dname=request.form.get('txtdname')
	hname=request.form.get('txthname')
	state=request.form.get('state')
	district=request.form.get('district')
	place=request.form.get('txtplace')
	dob=request.form.get('txtdate')
	phone=request.form.get('txtphn')
	regnum=request.form.get('txtregnum')
	yearr=request.form.get('yor')
	specification=request.form.get('spec')
	db.editdoc(dname,hname,state,district,place,dob,phone,regnum,yearr,specification,session["useremail"],filename)
	return render_template("message.html",message="Updated Successfully",route="/doctorhome")

@app.route("/showdocedit",methods=["GET","POST"])
def showdocedit():
	data=db.docdetails(session["useremail"])
	return render_template("doctor/editprofile.html",data=data[0],state=db.dbstate())

@app.route("/saveliedit",methods=["GET","POST"])
def saveliedit():
	filename=""
	file = request.files.get('file')
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	lname=request.form.get('txtlname')
	state=request.form.get('state')
	district=request.form.get('district')
	place=request.form.get('txtplace')
	dob=request.form.get('txtdate')
	phone=request.form.get('txtphn')
	pen=request.form.get('txtpen')
	db.editli(lname,state,district,place,dob,phone,pen,session["useremail"],filename)
	return render_template("message.html",message="Updated Successfully",route="/lihome")

@app.route("/showliedit",methods=["GET","POST"])
def showliedit():
	data=db.lidetails(session["useremail"])
	return render_template("li/editprofile.html",data=data[0],state=db.dbstate())


@app.route("/savefarmappointment",methods=['GET','POST'])	
def savefarmappointment():
	clinic=request.form["clinic"]
	print("clinic" + clinic)
	staff=request.form.get("staff")
	print(staff)
	res=staff.split("-")
	print(res)
	reason=request.form.get('txtreason')
	date=request.form.get('txtdate')
	time=request.form.get('txttime')
	print(session["farmid"])
	db.savefarmappointment(clinic,res[0],res[1],reason,date,time,session["useremail"],session["farmid"])
	return render_template("message.html",message="Appointment Successfull",route="/showcattlefarmhome")

@app.route("/showfarmappointment")
def showfarmappointment():
	email= session["useremail"]
	clinic = db.dbclinic(email)
	'''pname = db.dbpname(session["useremail"])'''
	return render_template("cattlefarmer/takeappointment.html",clinic=clinic)

@app.route("/viewfarmappointments",methods=['GET','POST'])
def viewfarmappointments():
	userid= session["useremail"]
	appointment = db.viewfarmappointments(userid)
	appointmentli=db.viewfarmlappointments(userid)
	return render_template("cattlefarmer/farmviewappointment.html",appointment=appointment,appointmentl=appointmentli)




@app.route("/saveappointment",methods=['GET','POST'])	
def saveappointment():
	pname=request.form.get('pname')
	reason=request.form.get('txtreason')
	date=request.form.get('txtdate')
	time=request.form.get('txttime')
	clinic=request.form["clinic"]
	print("clinic" + clinic)
	staff=request.form.get("staff")
	print(staff)
	res=staff.split("-")
	print(res)
	db.saveappointment(pname,reason,date,time,clinic,res[0],res[1])
	return render_template("message.html",message="Appointment Successfull",route="/showuserhome")

@app.route("/showcliniclist")
def showcliniclist():
	'''admin_id = session["useremail"]'''
	cliniclist = db.fetchcliniclist()
	print(cliniclist)
	return render_template("admin/viewclinic.html", cliniclist = cliniclist)

@app.route("/showappointment")
def showappointment():
	clinic = db.dbclinic(session["useremail"])
	pname = db.dbpname(session["useremail"])
	return render_template("user/appointment.html",pname=pname,clinic=clinic)

@app.route("/showdappointment")
def showdappointment():
	dr_id = session["useremail"]
	appointment = db.fetchAppointments(dr_id)
	# print(appointment)
	return render_template("doctor/viewappointment.html", appointment = appointment)

@app.route("/showfarmdappointment")
def showfarmdappointment():
	dr_id = session["useremail"]
	appointment = db.fetchfarmAppointments(dr_id)
	print(appointment)
	return render_template("doctor/farmappointmnt.html", appointment = appointment)

@app.route("/showfarmliappointment")
def showfarmliappointment():
	li_id = session["useremail"]
	appointment = db.fetchfarmliAppointments(li_id)
	print(appointment)
	return render_template("li/farmliappointment.html", appointment = appointment)
	
@app.route("/showliappointment")
def showliappointment():
	li_id = session["useremail"]
	appointment = db.fetchliAppointments(li_id)
	print(appointment)
	return render_template("li/viewappointment.html", appointment = appointment)

@app.route("/appointmentstatus",methods=['GET','POST'])
def appointmentstatus():
	userid= session["useremail"]
	status=db.getnotification(userid)
	print(status)
	return render_template("user/appointmentstatus.html", appointmentstatus = status)

@app.route("/farmappointmentstatus",methods=['GET','POST'])
def farmappointmentstatus():
	userid= session["useremail"]
	status=db.getnotification(userid)
	print(status)
	return render_template("cattlefarmer/farmappointmentstatus.html", appointmentstatus = status)

@app.route("/viewappointments",methods=['GET','POST'])
def viewappointments():
	userid= session["useremail"]
	appointment = db.viewappointments(userid)
	appointmentl=db.viewlappointments(userid)
	return render_template("user/viewappointment.html",appointment=appointment,appointmentl=appointmentl)

@app.route("/close",methods=['GET','POST'])
def close():
	id= request.form.get("id")
	db.close(id)
	return "ok"

@app.route("/closecomp",methods=['GET','POST'])
def closecomp():
	id= request.form.get("id")
	db.closecomp(id)
	return "ok"


@app.route("/viewadminresponse",methods=['GET','POST'])
def viewadminresponse():
	userid= session["useremail"]
	compresponse = db.viewadminresponse(userid)
	return render_template("user/complaintstatus.html",compresponse=compresponse)

@app.route("/viewfadminresponse",methods=['GET','POST'])
def viewfadminresponse():
	userid= session["useremail"]
	compresponse = db.viewfadminresponse(userid)
	return render_template("cattlefarmer/complaintstatus.html",compresponse=compresponse)

'''@app.route("/viewclinicresponse",methods=['GET','POST'])
def viewclinicresponse():
	userid= session["useremail"]
	compresponse = db.viewclinicresponse(userid)
	return render_template("user/complaintstatus.html",compresponse=compresponse)'''

@app.route("/viewfarmerschemes",methods=['GET','POST'])
def viewfarmerschemes():
	userid= session["useremail"]
	scheme = db.viewschemes(userid)
	return render_template("cattlefarmer/viewschemes.html",scheme=scheme)

@app.route("/showuserreport",methods=['GET','POST'])
def showuserreport():
	userlist = db.viewuserreport()
	return render_template("admin/userreport.html",userlist=userlist)

@app.route("/showclinicreport",methods=['GET','POST'])
def showclinicreport():
	cliniclist = db.viewclinicreport()
	return render_template("admin/clinicreport.html",cliniclist=cliniclist)

@app.route("/showpetreport",methods=['GET','POST'])
def showpetreport():
	petreportlist = db.viewpetreport()
	return render_template("admin/petreport.html",petreportlist=petreportlist)

@app.route("/showfarmreport",methods=['GET','POST'])
def showfarmreport():
	farmreportlist = db.viewfarmreport()
	return render_template("admin/farmreport.html",farmreportlist=farmreportlist)
	
@app.route("/showvaccnot")
def showvaccnot():
	#li_id = session["useremail"]#
	vaccination = db.getvaccdetails(session["useremail"])
	print(vaccination)
	return render_template("user/vaccnotification.html", vaccination = vaccination)


@app.route("/changedatef",methods=['GET','POST'])	
def changedatef():
	date=request.form["date"]
	time=request.form["time"]
	appointment_id = request.form["fpid"]
	print("zzzzz", time, appointment_id)
	db.changedatef(date,time, appointment_id)
	return "OK"

@app.route("/changedatep",methods=['GET','POST'])	
def changedatep():
	date=request.form["date"]
	time=request.form["time"]
	appointment_id = request.form["apid"]
	print("zzzzz", time, appointment_id)
	db.changedatep(date,time, appointment_id)
	return "OK"

@app.route("/changedatelip",methods=['GET','POST'])	
def changedatelip():
	date=request.form["date"]
	time=request.form["time"]
	appointment_id = request.form["apid"]
	print("zzzzz", time, appointment_id)
	db.changedatelip(date,time, appointment_id)
	return "OK"

@app.route("/changedatelif",methods=['GET','POST'])	
def changedatelif():
	date=request.form["date"]
	time=request.form["time"]
	appointment_id = request.form["fpid"]
	print("zzzzz", time, appointment_id)
	db.changedatelif(date,time, appointment_id)
	return "OK"

@app.route("/adminresponse",methods=['GET','POST'])	
def adminresponse():
	response=request.form["response"]
	comp_id = request.form["compid"]
	print(response,comp_id)
	db.adminresponse(response,comp_id)
	return "OK"

@app.route("/clinicresponse",methods=['GET','POST'])	
def clinicresponse():
	response=request.form["response"]
	comp_id = request.form["compid"]
	print(response,comp_id)
	db.clinicresponse(response,comp_id)
	return "OK"



@app.route("/lihome")
def lihome():
	return render_template("li/home.html")	

@app.route("/showreadmore")
def showreadmore():
	return render_template("single.html")	

@app.route("/acceptclinic",methods=['GET','POST'])	
def acceptclinic():
	c=request.form["b"]
	email=db.acceptcliniclist(c,session["useremail"])
	msg=Message("PET SAKE | Account Verification" ,sender="petsake123@gmail.com", recipients=[email])
	msg.body = "your account has been verified"
	mail.send(msg)
	return "OK"

@app.route("/rejectclinic",methods=['GET','POST'])	
def rejectclinic():
	c=request.form["b"]
	email=db.rejectcliniclist(c,session["useremail"])
	msg=Message("PET SAKE | Account Verification" ,sender="petsake123@gmail.com", recipients=[email])
	msg.body = "your account has been rejected"
	mail.send(msg)
	return "OK"	

@app.route("/accept1",methods=['GET','POST'])	
def accept1():
	c=request.form["b"]
	db.acceptappoint(c,session["useremail"])
	return "OK"

@app.route("/reject1",methods=['GET','POST'])	
def reject1():
	c=request.form["b"]
	db.rejectappoint(c,session["useremail"])
	return "OK"

@app.route("/accept2",methods=['GET','POST'])	
def accept2():
	c=request.form["b"]
	db.acceptfarmappoint(c,session["useremail"])
	return "OK"

@app.route("/reject2",methods=['GET','POST'])	
def reject2():
	c=request.form["b"]
	db.rejectfarmappoint(c,session["useremail"])
	return "OK"

@app.route("/acceptli2",methods=['GET','POST'])	
def acceptli2():
	c=request.form["b"]
	db.acceptlifarmappoint(c,session["useremail"])
	return "OK"

@app.route("/rejectli2",methods=['GET','POST'])	
def rejectli2():
	c=request.form["b"]
	db.rejectlifarmappoint(c,session["useremail"])
	return "OK"

@app.route("/acceptlip",methods=['GET','POST'])	
def acceptlip():
	c=request.form["b"]
	db.acceptliappoint(c,session["useremail"])
	return "OK"

@app.route("/rejectlip",methods=['GET','POST'])	
def rejectlip():
	c=request.form["b"]
	db.rejectliappoint(c,session["useremail"])
	return "OK"


@app.route("/saveattenderreg",methods=['GET','POST'])	
def saveattenderreg():
	name=request.form['txtname']
	gender=request.form['gender']
	state=request.form['state']
	district=request.form['district']
	place=request.form['txtplace']
	date=request.form['txtdate']
	phone=request.form['txtphn']
	email=request.form['txtemail']
	password=request.form['txtpswrd']
	db.saveattender(name,gender,state,district,place,date,phone,email,password,session["useremail"])
	return "Registration Successfull"

@app.route("/showattenderreg")
def showattenderreg():
	state=db.dbstate()
	return render_template("attenderregistration.html",state=state)	

@app.route("/savespecies",methods=['GET','POST'])	
def savespecies():
	name=request.form['sname']
	pdisease=request.form['distopet']
	hdisease=request.form['disfrompet']
	food=request.form['food']
	symptoms=request.form['symptoms']
	medicine=request.form['vacmed']
	db.savesp(name,pdisease,hdisease,food,symptoms,medicine)
	return render_template("message.html",message="Saved Successfull",route="/showadminhome")

@app.route("/showspecies")
def showspecies():
	return render_template("admin/species.html")	

@app.route("/saveschemes",methods=['GET','POST'])	
def saveschemes():
	stype=request.form['txttype']
	sname=request.form['txtname']
	sdetails=request.form['txtdetails']
	db.savescheme(stype,sname,sdetails)
	return render_template("message.html",message="Added Successfully",route="/showadminhome")

@app.route("/showschemes")
def showschemes():
	return render_template("admin/schemes.html")

@app.route("/savevacc",methods=['GET','POST'])	
def savevacc():
	sname=request.form['species']
	age=request.form['txtage']
	weekmonth=request.form['txtweekmonth']
	vacc=request.form['vacc']
	desc=request.form['desc']
	db.savevacc(sname,age,weekmonth,vacc,desc)
	return render_template("message.html",message="Added Successfully",route="/showadminhome")

@app.route("/showvaccination")
def showvaccination():
	species=db.dbspecies()
	return render_template("admin/vaccination.html",species=species)	


@app.route("/savebreed",methods=['GET','POST'])	
def savebreed():

	name=request.form['species']
	breed=request.form['breed']
	pdisease=request.form['distopet']
	hdisease=request.form['disfrompet']
	food=request.form['food']
	symptoms=request.form['symptoms']
	medicine=request.form['vacmed']
	db.savebr(name,breed,pdisease,hdisease,food,symptoms,medicine)
	return render_template("message.html",message="Added Successfully",route="/showadminhome")

@app.route("/showbreed")
def showbreed():
	species=db.dbspecies()
	return render_template("admin/breed.html",species=species)	

@app.route("/savecomplaint",methods=['GET','POST'])	
def savecomplaint():
	name=request.form['comps']
	compdesc=request.form['compd']
	comp=request.form['compto']
	cl=request.form['clinic']
	date=request.form['txtdate']
	if comp == 'admin':
		st="admin"
	else:
		st=cl
	db.savecomp(name,compdesc,date,st,session["useremail"])
	return render_template("message.html",message="complaint registration Successfull",route="/showuserhome")

@app.route("/showcomplaint")
def showcomplaint():
	clinic=db.dbcompclinic(session["useremail"])
	return render_template("user/complaint.html",clinic=clinic)	

@app.route("/savefcomplaint",methods=['GET','POST'])	
def savefcomplaint():
	name=request.form['comps']
	compdesc=request.form['compd']
	comp=request.form['compto']
	cl=request.form['clinic']
	date=request.form['txtdate']
	if comp == 'admin':
		st="admin"
	else:
		st=cl
	db.savecomp(name,compdesc,date,st,session["useremail"])
	return render_template("message.html",message="complaint registration Successfull",route="/showcattlefarmhome")

@app.route("/showfarmercomplaint")
def showfarmercomplaint():
	clinic=db.dbclinic()
	return render_template("cattlefarmer/complaint.html",clinic=clinic)	

@app.route("/showadmincomp")
def showadmincomp():
	complaint=db.viewadmincomp()
	print(complaint)
	return render_template("admin/viewcomplaint.html",complaint=complaint)

@app.route("/showcliniccomp")
def showcliniccomp():
	complaint=db.viewcliniccomp(session["useremail"])
	return render_template("clinic/viewcomplaint.html",complaint=complaint)

@app.route("/clinicreports",methods=['GET','POST'])
def clinicreports():
	doctorlist=db.getdoctorreports(session["useremail"])
	lilist=db.getlireports(session["useremail"])
	return render_template("clinic/report.html",doctorlist=doctorlist,lilist=lilist)

@app.route("/showclinicdetails")
def showclinicdetails():
	clinic=db.viewdetails(session["useremail"])
	return render_template("clinic/about.html",data=clinic)
	
@app.route("/getDistrict",methods=['GET','POST'])
def getDistrict():
	state=request.form["state"]
	district=db.dbdistrict(state)
	s="""<div class=form-group>
            <label for=sel1>District</label>

          <select required name=district class=form-control><option selected>------SELECT-----</option>"""
	for d in district:
		s=s+"<option value=" + str(d[0]) +">"+d[1]+"</option>"
	s=s+"</select></div>"
	return s

@app.route("/getBreed",methods=['GET','POST'])
def getBreed():
	selectedBreed=request.form.get("selectedBreed")
	species=request.form["species"]
	if selectedBreed == None : 
		breed=db.dbbreed(species)
		s="""<div class=form-group>
            <label for=sel1>Breed</label>

          <select required name=breed class=form-control><option selected>------SELECT-----</option>"""
		for b in breed:
			s=s+"<option value=" + str(b[1]) +">"+b[2]+"</option>"
		s=s+"</select></div>"
		return s
	else:
		breed=db.dbbreed(species)
		s="""<div class=form-group>
            <label for=sel1>Breed</label>

          <select required name=breed class=form-control><option selected>------SELECT-----</option>"""
		for b in breed:
			if str(selectedBreed) == str(b[1]):
				s=s+"<option  selected value=" + str(b[1]) +">"+b[2]+"</option>"
			else:
				s=s+"<option   value=" + str(b[1]) +">"+b[2]+"</option>"
		s=s+"</select></div>"
		return s

@app.route("/getStaff",methods=['GET','POST'])
def getStaff():
	clinic=request.form["clinic"]
	staff=db.dbstaff(clinic)
	s="""<div class=form-group>
            <label for=sel1>Staff</label>
          <select required name=staff class=form-control><option value=''>------SELECT-----</option>"""
	for d in staff:
		# print(str(s[1]))
		s=s+"<option value=" + str(d[0]) +">"+d[1]+"</option>"
	s=s+"</select></div>"
	return s


@app.route("/savedoctorreg",methods=['GET','POST'])	
def savedoctorreg():
	file = request.files['file']
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	name=request.form['txtdname']
	gender=request.form['gender']
	hname=request.form['txthname']
	state=request.form['state']
	district=request.form['district']
	place=request.form['txtplace']
	date=request.form['txtdate']
	phone=request.form['txtphn']
	email=request.form['txtemail']
	regnum=request.form['txtregnum']
	yor=request.form['yor']
	spec=request.form['spec']
	password=request.form['txtpswrd']
	ques=request.form['txtquestion']
	ans=request.form['txtans']
	# msg=message("Heloo your username is "+email+" and password is "+password ,sender="petsake123@gmail.com", recipient=[email])
	# Mail.send(msg)
	db.savedoctor(name,gender,hname,state,district,place,date,phone,email,regnum,yor,spec,password,ques,ans,filename,session["useremail"])
	msg=Message("PET SAKE | Login Credentials" ,sender="petsake123@gmail.com", recipients=[email])
	msg.body = "Hello welcome to PETSAKE,your username is "+email+" and password is "+password
	#temporarily disabled    mail.send(msg)
	return render_template("message.html",message="Registration Successfull",route="/showclinichome")

@app.route("/showdoctorreg")
def showdoctorreg():
	state=db.dbstate()
	return render_template("doctorreg.html",state=state)	

@app.route("/doctorhome")
def doctorhome():
	return render_template("doctor/home.html")	



@app.route("/savelireg",methods=['GET','POST'])	
def savelireg():
	file = request.files['file']
	if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            print(filename)
	name=request.form['txtlname']
	gender=request.form['gender']
	state=request.form['state']
	district=request.form['district']
	place=request.form['txtplace']
	date=request.form['txtdate']
	phone=request.form['txtphn']
	pen=request.form['txtpen']
	email=request.form['txtemail']
	password=request.form['txtpswrd']
	ques=request.form['txtquestion']
	ans=request.form['txtans']
	db.saveli(name,gender,state,district,place,date,phone,pen,email,password,ques,ans,filename,session["useremail"])
	msg=Message("PET SAKE | Login Credentials" ,sender="petsake123@gmail.com", recipients=[email])
	msg.body = "Hello welcome to PETSAKE,your username is "+email+" and password is "+password
	#mail.send(msg)
	return render_template("message.html",message="Registration Successfull",route="/showclinichome")

@app.route("/liinfoupload",methods=['GET','POST'])	
def liinfoupload():
	name=request.form['txtprgm']
	if request.method == 'POST':
		file = request.files['file1']
		print(file)
		if file:
			filename=secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			print(filename)
	datpgm=request.form['txtdatetime']
	description=request.form['description']
	postdat=request.form['txtpostdatetime']
	postperson=request.form['txtpostedperson']
	db.liinfo(name,filename,datpgm,description,postdat,postperson,session['useremail'])
	return render_template("message.html",message="Registration Successfull",route="/lihome")
	
@app.route("/liinfoupload1")
def liinfoupload1():
	return render_template("li/liinfo.html")

@app.route("/savechangepasswordu",methods=["GET","POST"])
def savechangepasswordu():
	print("hhghgggf")
	oldpassword=request.form['oldpassword']
	newpassword=request.form['newpassword']
	confirmpassword=request.form['confirmpassword']
	db.savechangepasswordc(session["useremail"],oldpassword,newpassword,confirmpassword)
	return render_template("message.html",message="Password Changed",route="/login1")


@app.route("/showchangepasswordu")
def showChangepasswordu():
	return render_template("user/changepwrd.html")

@app.route("/showchangepasswordc")
def showChangepasswordc():
	return render_template("cattlefarmer/changepwrd.html")

@app.route("/showchangepasswordd")
def showChangepasswordd():
	return render_template("doctor/changepwrd.html")

@app.route("/showchangepasswordli")
def showChangepasswordli():
	return render_template("li/changepwrd.html")

@app.route("/showchangepasswordcl")
def showChangepasswordcl():
	return render_template("clinic/changepswrd.html")

@app.route("/checkusername",methods=["GET","POST"])
def checkusername():
	email=request.form['email']
	r=db.checkusername(email)
	if(len(r) == 0):
		return "0"
	else:
		return r[0][0]

@app.route("/fetchpass",methods=["GET","POST"])
def fetchpass():
	email=request.form['email']
	seq=request.form['seq']
	ans=request.form['ans']


	r=db.fetchpass(email,seq,ans)
	if(len(r) == 0):
		return "0"
	else:
		return r[0][0]


@app.route("/shownot",methods=['GET','POST'])
def shownot():
	from_id =session["useremail"]
	print("fromid",from_id)
	to_id = request.args.get('to_id')
	print("toid",to_id)
	session['to_id'] = to_id
	print("====", from_id, to_id, "====")
	messages = db.fetch_messages(from_id, to_id)
	if len(messages)<=0:
		prev_msg = ""
		return render_template("doctor/chat.html", messages = messages, from_id=from_id, talking_to = to_id)
	prev_msg = messages[-1][4]
	return render_template("doctor/chat.html", messages = messages, from_id=from_id, talking_to = to_id)







@app.route("/showchat")
def showchat():
	chat=db.viewdoctors()
	return render_template("user/docchat.html",chat=chat)

@app.route("/showdocnotification")
def showdocnotification():
	notifications=db.viewdocnotification(session["useremail"])
	print(notifications)
	return render_template("doctor/notifications.html",chat=notifications)

prev_msg = ""
@app.route('/chat', methods=['GET', 'POST'])
def chat():
	global prev_msg
	from_id = session["useremail"]
	print("fromid",from_id)
	to_id = request.args.get('to_id')
	print("toid",to_id)
	session['to_id'] = to_id
	print("====", from_id, to_id, "====")
	messages = db.fetch_messages(from_id, to_id)
	if len(messages) ==0:
		prev_msg = ""
		# print(messages)
		return render_template("user/chat.html", messages = messages, from_id=from_id, talking_to = to_id)
	prev_msg = messages[-1][3]
	return render_template("user/chat.html", messages = messages, from_id=from_id, talking_to = to_id)
    
@app.route('/send1', methods=['GET', 'POST'])
def send1():
    message = request.form.get('message')
    print("sending :", message)
    from_id = session["useremail"]
    to_id = session['to_id']
    db.send_message(from_id, to_id, message)
    return 'success'




@app.route('/getnewmessage', methods=['GET', 'POST'])  
def getnewmessage():
	global prev_msg
	to_id = request.form["get_from"]
	from_id = request.form["from_id"]
	print("===",from_id, to_id)
	last_raw = db.get_last_message(to_id, from_id)
	# print(prev_msg)
	# print(from_id)
	# print("chatuserid " + last_raw[1])
	# print("fromid " + from_id)
	# if(from_id != last_raw[1]):
		# print(last_raw[1])
	
	if(last_raw != False):
		last_msg = last_raw[3]
		print(last_msg)
		print(prev_msg)
		if(last_msg!=prev_msg):
			prev_msg = last_msg
			retmsg={"id":last_raw[0],"message":last_raw[3],"from_id":last_raw[1],"to_id":last_raw[2]}
			return json.dumps(retmsg)
	return "no_msg"


@app.route("/showforgotpassword",methods=["GET","POST"])
def showforgotpassword():
	return render_template("forgotpassword.html")

@app.route("/showlireg")
def showlireg():
	state=db.dbstate()
	return render_template("lireg.html",state=state)	

@app.route("/showabout")
def showAbout():
	return render_template("about.html")	

@app.route("/showcontact")
def showContact():
	return render_template("contact.html")
@app.route("/showcontactli")
def showContactli():
	return render_template("li/contact.html")
@app.route("/showadminform")
def showadminform():
	return render_template("admin/adminform.html")	


if __name__=="__main__":
	app.run(debug=True)
