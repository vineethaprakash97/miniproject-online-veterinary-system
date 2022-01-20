import pymysql
import datetime
from datetime import timedelta
db=pymysql.connect("localhost","root","","petsake")
def dblogsel(username,password):
	sql = "select usertype from tbl_login where Email='"+username+"' and password='"+password+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	if len(result)==1:
		return list(result)
	else:
		return False
def getclinicstatus(email):
	sql="select c.status from tbl_clinicreg c where c.Clinic_Email_id='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchone()
	return(result[0])

def saveuser(name,hname,state,district,place,pincode,dob,phone,email,password,category,ques,ans):
	sql="""insert into tbl_userreg(name,hname,state,district,place,pincode,dob,phone,email,pswd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	val=(name,hname,state,district,place,pincode,dob,phone,email,password)
	cursor=db.cursor()
	cursor.execute(sql,val)
	sql = """INSERT INTO tbl_login(Email,password,usertype,securityque,securityans) VALUES ( %s,%s,%s, %s,%s)"""
	val = (email,password,category,ques,ans)
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()
	return True

	
def saveclinic(name,reg,place,district,state,phone,pincode,email,govform,txtname,address,txtphn,password,ques,ans,filename):
	sql1="""insert into tbl_clinicreg(Clinic_name,Clinic_reg_no,state,district,place,pincode,phone,Clinic_Email_id,Govt_no,form,Name,address,phno) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	val1=(name,reg,state,district,place,pincode,phone,email,govform,filename,txtname,address,txtphn)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	sql = """INSERT INTO tbl_login(Email,password,usertype,securityque,securityans) VALUES ( %s,%s,%s, %s,%s)"""
	val = (email,password,'clinic',ques,ans) 
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()
	return True

def savefarm(name,state,district,place,year,regno,phone,email,filename,userid):
	sql1="""insert into tbl_farmreg(farmname,photo,year,fregno,state,district,place,contactno,usermailid,userid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	val1=(name,filename,year,regno,state,district,place,phone,email,userid)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	sql2="select farmid from tbl_farmreg where userid='"+ str(userid) +"'"
	cursor=db.cursor()
	cursor.execute(sql2)
	result=cursor.fetchall()
	return result[0][0]






def savefarmanimal(species,breed,no,datee,farmid):
	sql1="""insert into tbl_animal(species,breed,noofanimal,dateofbuy,farmid) VALUES (%s,%s,%s,%s,%s)"""
	val1=(species,breed,no,datee,farmid)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def getfarmid(useremail):
	sql1="select farmid from tbl_farmreg where userid='"+ str(useremail) +"'"
	print(sql1)
	cursor=db.cursor()
	cursor.execute(sql1)
	result=cursor.fetchall()
	if len(result) > 1:
		print(result[0][0])
		return result[0][0]


def saveuserpetdetails(pname,name,breed,other,gender,age,weekmonth,description,filename,email):
	sql1="""insert into tbl_userpetdetails(pname,name,breed,other,gender,dateofreg,age,weekmonth,description,email,photo) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
	val1=(pname,name,breed,other,gender,datetime.date.today(),age,weekmonth,description,email,filename)
	# d=datetime.datetime.today()-timedelta(days=(age*7))
	# print(d)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def getpetlist(email):
	sql="select * from tbl_userpetdetails where email='"+ str(email) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	res=list(result)
	temp=[]
	for r in res:
		sp=r[3]
		br=r[4]
		print(sp)
		print(br)
		sql="select spname from tbl_species where spid='"+str(sp)+"'"
		cursor=db.cursor()
		cursor.execute(sql)
		result=cursor.fetchall()
		print(result)
		spname=result[0][0]
		sql="select breedname from tbl_breed where breedid='"+str(br)+"'"
		cursor=db.cursor()
		cursor.execute(sql)
		result=cursor.fetchall()
		brname=result[0][0]
		print(result)
		rtemp=list(r)
		rtemp[3]=spname
		rtemp[4]=brname
		temp.append(rtemp)
	return temp

def delpets(petid):
	print(petid)
	sql="DELETE FROM tbl_userpetdetails WHERE pid="+str(petid);
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def editpets(petid,pname,name,breed,other,gender,age,weekmonths,description,email,filename=""):
	sql1="select * from tbl_userpetdetails WHERE pid='"+petid+"' and ( age='"+str(age)+"' and weekmonth='"+str(weekmonths)+"' )"
	cursor=db.cursor()
	cursor.execute(sql1)
	r=cursor.fetchall()
	date=datetime.date.today()
	date=str(date)
	if(len(r) == 0 ):
		if(filename == ""):
			sql="UPDATE tbl_userpetdetails SET pname='"+pname+"',name='"+name+"',breed='"+breed+"',other='"+other+"',gender='"+gender+"',age='"+age+"',weekmonth='"+weekmonths+"',dateofreg='"+date+"',description='"+description+"' WHERE pid='"+petid+"'"
		else:
			sql="UPDATE tbl_userpetdetails SET pname='"+pname+"',name='"+name+"',breed='"+breed+"',other='"+other+"',gender='"+gender+"',age='"+age+"',weekmonth='"+weekmonths+"',dateofreg='"+date+"',description='"+description+"',photo='"+filename+"' WHERE pid='"+petid+"'"
	else:
		if(filename == ""):
			sql="UPDATE tbl_userpetdetails SET pname='"+pname+"',name='"+name+"',breed='"+breed+"',other='"+other+"',gender='"+gender+"',age='"+age+"',weekmonth='"+weekmonths+"',description='"+description+"' WHERE pid='"+petid+"'"
		else:
			sql="UPDATE tbl_userpetdetails SET pname='"+pname+"',name='"+name+"',breed='"+breed+"',other='"+other+"',gender='"+gender+"',age='"+age+"',weekmonth='"+weekmonths+"',description='"+description+"',photo='"+filename+"' WHERE pid='"+petid+"'"

	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def editfarm(fname,state,district,place,yearr,regnum,phone,email,filename=""):
	if(filename == ""):
		sql="UPDATE tbl_farmreg SET farmname='"+fname+"',state='"+state+"',district='"+district+"',place='"+place+"',year='"+yearr+"',fregno='"+regnum+"',contactno='"+phone+"' WHERE userid='"+email+"'"
	else:
		sql="UPDATE tbl_farmreg SET farmname='"+fname+"',state='"+state+"',district='"+district+"',place='"+place+"',year='"+yearr+"',fregno='"+regnum+"',contactno='"+phone+"',photo='"+filename+"' WHERE userid='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def edituser(name,hname,state,district,place,pincode,dob,phone,email):
	sql="UPDATE tbl_userreg SET name='"+name+"',hname='"+hname+"',state='"+state+"',district='"+district+"',place='"+place+"',pincode='"+pincode+"',dob='"+dob+"',phone='"+phone+"' WHERE email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def editdoc(dname,hname,state,district,place,dob,phone,regnum,yearr,specification,email,filename=""):
	if(filename == ""):
		sql="UPDATE tbl_docreg SET name='"+dname+"',hname='"+hname+"',state='"+state+"',district='"+district+"',place='"+place+"',datee='"+dob+"',phone='"+phone+"',regno='"+regnum+"',regyear='"+yearr+"',specialisation='"+specification+"' WHERE email='"+email+"'"
	else:
		sql="UPDATE tbl_docreg SET name='"+dname+"',hname='"+hname+"',state='"+state+"',district='"+district+"',place='"+place+"',datee='"+dob+"',phone='"+phone+"',regno='"+regnum+"',regyear='"+yearr+"',specialisation='"+specification+"',photo='"+filename+"' WHERE email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def editli(lname,state,district,place,dob,phone,pen,email,filename=""):
	if(filename == ""):
		sql="UPDATE tbl_lireg SET name='"+lname+"',state='"+state+"',district='"+district+"',place='"+place+"',datee='"+dob+"',phone='"+phone+"',pen='"+pen+"' WHERE email='"+email+"'"
	else:
		sql="UPDATE tbl_lireg SET name='"+lname+"',state='"+state+"',district='"+district+"',place='"+place+"',datee='"+dob+"',phone='"+phone+"',pen='"+pen+"',photo='"+filename+"' WHERE email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()



def getpetdetails(petid):
	print(petid)
	sql="select * from tbl_userpetdetails where pid="+str(petid)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	return(result)

def petdetails(petid,email):
	print(petid)
	sql="select * from tbl_userpetdetails where email='"+email+"' and pid="+str(petid)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def userdetails(email):
	sql="select * from tbl_userreg where email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def farmdetails(email):
	sql="select * from tbl_farmreg where userid='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def docdetails(email):
	sql="select * from tbl_docreg where email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def lidetails(email):
	sql="select * from tbl_lireg where email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)


def getviewmore(petid):
	print(petid)
	sql="select s.pdisease,s.hdisease,s.food,s.symptoms,s.medicine from tbl_species s,tbl_breed b,tbl_userpetdetails u where u.name=s.spid and u.breed=b.breedid and u.pid="+str(petid)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	# print(result)
	return list(result)
	# speciesid=result[0][0]
	# breedid=result[0][1]

def getviewmoreb(petid):
	print(petid)
	sql="select b.pdisease,b.hdisease,b.food,b.symptoms,b.medicine from tbl_species s,tbl_breed b,tbl_userpetdetails u where u.name=s.spid and u.breed=b.breedid and u.pid="+str(petid)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	# print(result)
	return list(result)
	# speciesid=result[0][0]
	# breedid=result[0][1]

def getdoctorreports(email):
	sql="select DISTINCT d.name,d.hname,d.place,d.phone,d.email,d.specialisation,d.regyear from tbl_docreg d,tbl_clinicreg c where d.clinicemailid='"+ str(email) +"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def getlireports(email):
	sql="select DISTINCT l.name,l.place,l.phone,l.email,l.pen from tbl_lireg l,tbl_clinicreg c where l.clinicemailid='"+ str(email) +"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewdetails(email):
	sql="select * from tbl_clinicreg c where c.Clinic_Email_id='"+str(email)+"' "
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	print(result)
	return(result)



def getvaccdetails(email):
	sql="select u.name,u.age,u.weekmonth,u.dateofreg from tbl_userpetdetails u WHERE u.email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	res=list(result) 
	print(res)
	v=[]
	for r in res:
		var=r[3]
		a=datetime.datetime.strptime(var, '%Y-%m-%d')
		d=""
		if(r[2] == "weeks"):
			d = a - timedelta(days=(r[1]*7))
		elif(r[2] == "months"):
			d = a - timedelta(days=(r[1]*30))
		# print(d)
		b=datetime.datetime.today()-d
		# print(b)
		# print(abs(b.days))
		sql1="select u.pname,s.spname,v.age,v.weekmonth,v.vacc,v.description from tbl_vacc v,tbl_userpetdetails u,tbl_species s where u.name=s.spid and u.email='"+email+"' and v.sname='"+str(r[0])+"' and v.sname= u.name "
		print(sql1)
		c=abs(b.days)
		cursor=db.cursor()
		cursor.execute(sql1)
		result=cursor.fetchall()
		# print(result)
		data=list(result)
		for d in data:
			age=""
			if(d[3] == "weeks"):
				age=int(d[2])*7
			elif(d[3] == "months"):
				age=int(d[2])*30
			# print(age)
			if(age-c <= 14 and age-c >= 0):
				v.append(d)
	return v	
				






def savefarmappointment(clinic,staffid,stafftype,reason,date,time,email,farmid):
	sql1="""insert into tbl_farmappointment(clinic,staff,stafftype,reason,datee,time,usermail,farmid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
	val1=(clinic,staffid,stafftype,reason,date,time,email,farmid)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True


def saveappointment(pname,reason,date,time,clinic,staffid,stafftype):
	sql1="""insert into tbl_appointment(pname,reason,datee,time,clinic,staff,stafftype) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
	val1=(pname,reason,date,time,clinic,staffid,stafftype)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def savescheme(stype,sname,sdetails):
	sql1="""insert into tbl_scheme(type,name,details)VALUES(%s,%s,%s)"""
	val1=(stype,sname,sdetails)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def savevacc(sname,age,weekmonth,vacc,desc):
	sql1="""insert into tbl_vacc(sname,age,weekmonth,vacc,description)VALUES(%s,%s,%s,%s,%s)"""
	val1=(sname,age,weekmonth,vacc,desc)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def fetchcliniclist():
	sql = "select c.Clinic_name,c.Clinic_reg_no,c.Govt_no,c.Clinic_Email_id,c.phone,c.Clinic_id from tbl_clinicreg c where status='Requested'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)


def fetchAppointments(dr_id):
	sql = "select u.pname,u.age,v.name,v.phone,v.email,a.datee,a.time,a.reason,a.apid from tbl_appointment a, tbl_docreg d, tbl_userpetdetails u,tbl_userreg v where a.staff=d.docid and u.email=v.email and u.pid=a.pname and d.email='"+dr_id+"' and  status='Requested'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def fetchfarmAppointments(dr_id):
	sql = "select v.name,v.phone,v.email,fa.farmname,fa.contactno,fa.usermailid,f.reason,f.datee,f.time,f.fpid from tbl_farmappointment f, tbl_docreg d, tbl_animal a,tbl_userreg v,tbl_farmreg fa where f.staff=d.docid and fa.farmid=f.farmid and f.usermail=v.email and fa.farmid=a.farmid and d.email='"+dr_id+"' and  status='Requested'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def fetchfarmliAppointments(li_id):
	sql = "select v.name,v.phone,v.email,fa.farmname,fa.contactno,fa.usermailid,f.reason,f. datee,f.time,f.fpid from tbl_farmappointment f, tbl_lireg l,tbl_userreg v,tbl_farmreg fa where f.staff=l.liid and fa.farmid=f.farmid and f.usermail=v.email and l.email ='"+li_id+"' and  status='Requested'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)


def fetchliAppointments(li_id):
	sql = "select u.pname,v.name,v.phone,v.email,a.datee,a.time,a.apid from tbl_appointment a, tbl_lireg l, tbl_userpetdetails u,tbl_userreg v where a.staff=l.liid and u.email=v.email and u.pid=a.pname and l.email='"+li_id+"' and  status='Requested'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def acceptcliniclist(b,email):
	sql="update tbl_clinicreg set status='Accept' where Clinic_id= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()
	sql1="select c.Clinic_Email_id from tbl_clinicreg c where Clinic_id= '"+str(b)+"'"
	print(sql1)
	cursor=db.cursor()
	cursor.execute(sql1)
	result=cursor.fetchone()
	print(result)
	return(result[0])

def rejectcliniclist(b,email):
	sql="update tbl_clinicreg set status='Reject' where Clinic_id= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()
	sql1="select c.Clinic_Email_id from tbl_clinicreg c where Clinic_id= '"+str(b)+"'"
	print(sql1)
	cursor=db.cursor()
	cursor.execute(sql1)
	result=cursor.fetchone()
	print(result)
	return(result[0])

def acceptappoint(b,email):
	sql="update tbl_appointment set status='Accept' where apid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select u.email from tbl_userpetdetails u,tbl_appointment a where u.pid=a.pname and apid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'Doctor',uemail,'user',datetime.datetime.now(),'Appointment','Accepted' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()
	
def rejectappoint(b,email):
	sql="update tbl_appointment set status='Reject' where apid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select u.email from tbl_userpetdetails u,tbl_appointment a where u.pid=a.pname and apid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'Doctor',uemail,'user',datetime.datetime.now(),'Appointment','Rejected' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def acceptliappoint(b,email):
	sql="update tbl_appointment set status='Accept' where apid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select u.email from tbl_userpetdetails u,tbl_appointment a where u.pid=a.pname and apid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'li',uemail,'user',datetime.datetime.now(),'Appointment','Accepted' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()
	
def rejectliappoint(b,email):
	sql="update tbl_appointment set status='Reject' where apid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select u.email from tbl_userpetdetails u,tbl_appointment a where u.pid=a.pname and apid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'li',uemail,'user',datetime.datetime.now(),'Appointment','Rejected' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def adminresponse(response,comp_id):
	sql="update tbl_complaint set response='"+str(response)+"',status='closed' where cmpid='"+str(comp_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def clinicresponse(response,comp_id):
	sql="update tbl_complaint   set clresponse='"+str(response)+"',status='closed' where cmpid='"+str(comp_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()



def changedatep(date,new_time,appointment_id):
	sql="update tbl_appointment set Doctor_response='Requested time slot is not available, please come at "+str(date)+" "+str(new_time) +"',datee='"+str(date)+"',time='"+str(new_time)+"' where apid= '"+str(appointment_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def changedatef(date,new_time,appointment_id):
	sql="update tbl_farmappointment set Doctor_response='Requested time slot is not available, please come at "+str(date)+" "+str(new_time) +"',datee='"+str(date)+"',time='"+str(new_time)+"' where fpid= '"+str(appointment_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def changedatelip(date,new_time,appointment_id):
	sql="update tbl_appointment set li_response='Requested time slot is not available, please come at "+str(date)+" "+str(new_time) +"',datee='"+str(date)+"',time='"+str(new_time)+"' where apid= '"+str(appointment_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def changedatelif(date,new_time,appointment_id):
	sql="update tbl_farmappointment set li_response='Requested time slot is not available, please come at "+str(date)+" "+str(new_time) +"',datee='"+str(date)+"',time='"+str(new_time)+"' where fpid= '"+str(appointment_id)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()


def close(nid):
	# str(id)
	sql="update tbl_notification set seen=1 where nid='"+str(nid)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def closecomp(nid):
	# str(id)
	sql="update tbl_complaint set seen=1 where cmpid='"+str(nid)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def getnotification(userid):
	sql="select d.name,n.from_id,n.fromusertype,n.to_id,n.tousertype,n.timeofsend,n.subject,n.message,nid from tbl_notification n,tbl_docreg d where n.from_id=d.email and n.to_id= '"+userid+"' and n.seen=0"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return result

def viewappointments(userid):
	sql="select u.pname,a.time,a.datee,a.reason,CONCAT(c.Clinic_name,' ,',c.place,',',c.phone,',',c.Clinic_Email_id),CONCAT(d.name,',',d.phone,',',d.email),a.status,a.Doctor_response from tbl_appointment a,tbl_userpetdetails u,tbl_clinicreg c,tbl_docreg d where a.clinic=c.Clinic_Email_id and u.pid=a.pname and  a.staff = d.docid  and u.email= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewlappointments(userid):
	sql="select u.pname,a.time,a.datee,a.reason,CONCAT(c.Clinic_name,' ,',c.place,',',c.phone,',',c.Clinic_Email_id),CONCAT(l.name,',',l.phone,',',l.email),a.status,a.li_response from tbl_appointment a,tbl_userpetdetails u,tbl_clinicreg c,tbl_lireg l where a.clinic=c.Clinic_Email_id and u.pid=a.pname and  a.staff = l.liid  and u.email= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewadminresponse(userid):
	sql="select c.status,c.compsub,c.compdesc,c.compto,c.response,c.clresponse,c.cmpid from tbl_complaint c where c.email= '"+userid+"' and c.seen=0"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewfadminresponse(userid):
	sql="select * from tbl_complaint c where c.email= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

'''def viewclinicresponse(userid):
	sql="select c.compsub,c.compdesc,c.clinic,c.response from tbl_complaint c where c.email= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)'''

def viewfarmappointments(userid):
	sql="select fa.farmname,f.time,f.datee,f.reason,CONCAT(c.Clinic_name,' ,',c.place,',',c.phone,',',c.Clinic_Email_id),CONCAT(d.name,',',d.phone,',',d.email),f.status,f.Doctor_response,f.li_response from tbl_farmappointment f,tbl_farmreg fa,tbl_animal a,tbl_clinicreg c,tbl_docreg d where f.clinic=c.Clinic_Email_id and f.farmid=a.farmid and c.Clinic_Email_id=d.clinicemailid and f.staff=d.docid and f.farmid=fa.farmid and f.usermail= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewfarmlappointments(userid):
	sql="select fa.farmname,f.time,f.datee,f.reason,CONCAT(c.Clinic_name,' ,',c.place,',',c.phone,',',c.Clinic_Email_id),CONCAT(l.name,',',l.phone,',',l.email),f.status,f.li_response from tbl_farmappointment f,tbl_farmreg fa,tbl_animal a,tbl_clinicreg c,tbl_lireg l where f.clinic=c.Clinic_Email_id and f.farmid=a.farmid and c.Clinic_Email_id=l.clinicemailid and f.staff=l.liid and f.farmid=fa.farmid and f.usermail= '"+userid+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def acceptfarmappoint(b,email):
	sql="update tbl_farmappointment set status='Accept' where fpid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select fa.usermail from tbl_farmappointment fa,tbl_animal a where fa.farmid=a.farmid and fpid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'Doctor',uemail,'user',datetime.datetime.now(),'Appointment','Accepted' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def rejectfarmappoint(b,email):
	sql="update tbl_farmappointment set status='Reject' where fpid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select fa.usermail from tbl_farmappointment fa,tbl_animal a where fa.farmid=a.farmid and fpid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'Doctor',uemail,'user',datetime.datetime.now(),'Appointment','Rejected' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def acceptlifarmappoint(b,email):
	sql="update tbl_farmappointment set status='Accept' where fpid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select fa.usermail from tbl_farmappointment fa,tbl_farmreg fr where fr.farmid = fa.farmid and fpid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'li',uemail,'user',datetime.datetime.now(),'Appointment','Accepted' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def rejectlifarmappoint(b,email):
	sql="update tbl_farmappointment set status='Reject' where fpid= '"+str(b)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	sql="select fa.usermail from tbl_farmappointment fa,tbl_farmreg fr where fr.farmid = fa.farmid and fpid='"+str(b)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	uemail=result[0][0]
	sql="insert into tbl_notification(from_id,fromusertype,to_id,tousertype,timeofsend,subject,message) VALUES (%s,%s,%s,%s,%s,%s,%s)"
	val1=(email,'li',uemail,'user',datetime.datetime.now(),'Appointment','Rejected' )
	cursor=db.cursor()
	cursor.execute(sql,val1)
	db.commit()

def viewschemes(userid):
	sql1="""select s.type,s.name,s.details from tbl_scheme s"""
	print(sql1)
	cursor=db.cursor()
	cursor.execute(sql1)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewuserreport():
	sql="select u.name,u.hname,u.place,u.phone,u.email,l.usertype from tbl_userreg u,tbl_login l where  u.email=l.Email"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewclinicreport():
	sql="select c.Clinic_name,c.Clinic_reg_no,c.place,c.phone,c.pincode,c.Clinic_Email_id from tbl_clinicreg c where  c.status='Accept'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def	viewpetreport():
	sql="select v.name,v.phone,u.email,a.reason,a.datee,a.time,a.clinic,a.stafftype from tbl_userreg v,tbl_userpetdetails u,tbl_appointment a where v.email=u.email"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def	viewfarmreport():
	sql="select fa.farmname,fa.contactno,fa.usermailid,f.usermail,f.reason,f.datee,f.time,f.clinic,f.stafftype from tbl_farmreg fa,tbl_farmappointment f where fa.userid=f.usermail"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def savesp(name,pdisease,hdisease,food,symptoms,medicine):
	sql1="""insert into tbl_species(spname,pdisease,hdisease,food,symptoms,medicine) VALUES (%s,%s,%s,%s,%s,%s)"""
	val1=(name,pdisease,hdisease,food,symptoms,medicine)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def savebr(name,breed,pdisease,hdisease,food,symptoms,medicine):
	sql1="""insert into tbl_breed(spid,breedname,pdisease,hdisease,food,symptoms,medicine) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
	val1=(name,breed,pdisease,hdisease,food,symptoms,medicine)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def savecomp(name,compdesc,date,st,email):
	sql1="""insert into tbl_complaint(compsub,compto,compdesc,compdate,email) VALUES (%s,%s,%s,%s,%s)"""
	val1=(name,st,compdesc,date,email)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def savefcomp(name,compdesc,date,st,email):
	sql1="""insert into tbl_complaint(compsub,compto,compdesc,compdate,email) VALUES (%s,%s,%s,%s,%s)"""
	val1=(name,st,compdesc,date,email)
	cursor=db.cursor()
	cursor.execute(sql1,val1)
	db.commit()
	return True

def viewadmincomp():
	sql="select c.email,c.compsub,c.compdesc,c.compdate,c.cmpid from tbl_complaint c where c.compto='admin' and c.seen=0 "
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def viewcliniccomp(email):
	sql="select c.email,c.compsub,c.compdesc,c.compdate,c.cmpid from tbl_complaint c, tbl_clinicreg r where  c.compto='"+email+"' and r.Clinic_Email_id= c.compto and c.seen=0 "
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	print(result)
	return(result)



def dbstate():
	sql="select * from tbl_state"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbdistrict(state):
	sql="select * from tbl_district where stateid='"+ str(state) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	return(result)
	print(list(result))
	return result

def dbspecies():
	sql="select * from tbl_species"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)
	
def dbbreed(species):
	sql="select * from tbl_breed where spid='"+ str(species) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	return(result)
	print(list(result))
	return result

def dbpname(email):
	sql="select pid,pname from tbl_userpetdetails where email='"+ str(email) +"'"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbquestion(email):
	sql="select securityque from tbl_login where Email='"+ str(email) +"'"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbclinic(email):
	sql="select c.Clinic_Email_id,c.Clinic_name from tbl_clinicreg c,tbl_userreg u where u.pincode=c.pincode and u.place=c.place and u.email='"+str(email)+"'"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbcompclinic(email):
	sql="select DISTINCT c.Clinic_Email_id,c.Clinic_name from tbl_clinicreg c,tbl_appointment a,tbl_userpetdetails u  where c.Clinic_Email_id=a.clinic and u.email='"+ str(email) +"'"
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	return(result)

def dbstaff(clinic):
	sql="select docid,name from tbl_docreg where clinicemailid='"+ str(clinic) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	temp=list(result)
	doc=[]
	for t in temp:
		doc.append(list(t))
	for i in range(len(doc)):
		doc[i][0]=str(doc[i][0]) + "-Doctor"
		doc[i][1]=str(doc[i][1]) + " - Doctor"
	print(doc)
	sql="select liid,name from tbl_lireg where clinicemailid='"+ str(clinic) +"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	temp =list(result)
	li=[]
	for t in temp:
		li.append(list(t))
	for i in range(len(li)):
		li[i][0]=str(li[i][0]) + "-LI"
		li[i][1]=str(li[i][1]) + " - Livestock Inspector"
	print(doc)
	res=doc+li
	# print(res)

	'''return a'''
	return res

	


def saveattender(name,gender,state,district,place,date,phone,email,password,clinicemailid):
	sql = """INSERT INTO tbl_attenderreg(Name,Gender,state,district,place,datee,phone,Emailid,clinicemailid) VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s)"""
	val = (name,gender,state,district,place,date,phone,email,clinicemailid)
	cursor=db.cursor()
	cursor.execute(sql,val)
	sql = """INSERT INTO tbl_login(Email,password,usertype) VALUES ( %s, %s,%s)"""
	val = (email,password,'attender')
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()


def savedoctor(name,gender,hname,state,district,place,date,phone,email,regnum,yor,spec,password,ques,ans,filename,clinicemailid):
	sql = """INSERT INTO tbl_docreg(name,gender,hname,state,district,place,datee,phone,email,regno,regyear,specialisation,photo,clinicemailid) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s, %s, %s,%s,%s,%s)"""
	val = (name,gender,hname,state,district,place,date,phone,email,regnum,yor,spec,filename,clinicemailid)
	cursor=db.cursor()
	cursor.execute(sql,val)
	sql = """INSERT INTO tbl_login(Email,password,usertype,securityque,securityans) VALUES ( %s,%s,%s, %s,%s)"""
	val = (email,password,'doctor',ques,ans)
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()

def saveli(name,gender,state,district,place,date,phone,pen,email,password,ques,ans,filename,clinicemailid):
	sql = """INSERT INTO tbl_lireg(name,gender,state,district,place,datee,phone,pen,email,photo,clinicemailid) VALUES ( %s, %s, %s,%s,%s,%s,%s,%s,%s, %s,%s)"""
	val = (name,gender,state,district,place,date,phone,pen,email,filename,clinicemailid)
	cursor=db.cursor()
	cursor.execute(sql,val)
	sql = """INSERT INTO tbl_login(Email,password,usertype,securityque,securityans) VALUES ( %s,%s,%s, %s,%s)"""
	val = (email,password,'li',ques,ans)
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()

def liinfo(name,file,datpgm,description,postdat,postperson,emailid):
	sql="INSERT INTO tbl_liinfo(Program_name,photo,program_date,description,posted_date,posted_person_detail,emailid)VALUES(%s,%s,%s,%s,%s,%s,%s)"
	val=(name,file,datpgm,description,postdat,postperson,emailid)
	print(sql,val)
	print(file)
	cursor=db.cursor()
	cursor.execute(sql,val)
	db.commit()

def viewnotifications():
	sql="select * from tbl_liinfo "
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	print(result)
	return(result)

def savechangepasswordc(email,oldpassword,newpassword,confirmpassword):
	sql="UPDATE tbl_login set password='"+newpassword+"' WHERE Email='"+email+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql)
	db.commit()

def checkusername(email):
	sql = "select securityque from tbl_login where Email='"+email+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def fetchpass(email,seq,ans):
	sql = "select password from tbl_login where Email='"+email+"' and securityque='"+str(seq)+"' and securityans='"+str(ans)+"'"
	cursor=db.cursor()
	cursor.execute(sql)
	result=cursor.fetchall()
	print(result)
	return(result)

def viewdoctors():
	sql="select * from tbl_docreg "
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	print(result)
	return(result)

def viewdocnotification(email):
	sql="select distinct u.name,u.email from tbl_chat c,tbl_userreg u where u.email=c.from_id  and c.to_id='"+str(email)+"'"
	print(sql)
	cursor=db.cursor()
	cursor.execute(sql) 
	result=cursor.fetchall()
	print(result)
	return(result)

def fetch_messages(from_id, to_id):
	sql = "select * from tbl_chat where (from_id='"+from_id+"' and to_id = '"+to_id+"') or (to_id='"+from_id+"' and from_id='"+to_id+"')"
	print(sql)
	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	print(result)
	# if(len(result) == 0):
	# 	False
	# else:
	return result
def send_message(from_id, to_id, message):
	dt = datetime.datetime.now()
	# dt="324354657"
	print(dt)
	sql = "insert into tbl_chat(from_id,to_id,datetime,message) values('"+str(from_id)+"', '"+str(to_id)+"', '"+str(dt)+"', '"+str(message)+"')"
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()
	return 

def get_last_message(from_id, to_id):
	sql = "select * from tbl_chat where from_id='"+from_id+"' and to_id='"+to_id+"' order by id desc"
	# print(sql)
	cursor = db.cursor()
	cursor.execute(sql)
	result = cursor.fetchall()
	# print(result)
	if len(result)>0:
		return result[0]
	else:
		return False
	# return ['','','','','']