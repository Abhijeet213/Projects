from flask import Flask,request,render_template,redirect
from flask import session, make_response
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
import random 
import pymysql


def pass_validate(password: str):
    if len(password) >= 8:
        lower = 0
        upper = 0
        number = 0
        special = 0

        for i in password:
            if i.islower():
                lower += 1

            elif i.isupper():
                upper += 1

            elif i.isnumeric():
                number += 1

            elif i in "~!@#$%^&*()_+":
                special += 1

        if lower >= 1 and upper >= 1 and number >= 1 and special >= 1:
            return True
        return False
    return False


otpa=0
def send_email(otpa,email):
 login="techabissa@gmail.com"
 password="ozkuzhsdghotuacz"
 res = [email]
 msg=MIMEText(f"Otp For Email Verification Is -> {otpa}")
 msg['subject']=Header("Email Verification")
 msg['From']=login
 msg['To']=" ,".join(res)
 s=SMTP_SSL('smtp.gmail.com', 465)
 s.set_debuglevel(1)
 try:
    s.login(login,password)
    s.sendmail(msg['From'],res,msg.as_string())
 finally:
    s.quit()

def dbcon():
   db = pymysql.connect(user="root", password="",database="users",port=3306)
   return db
   
   

app= Flask(__name__)

app.secret_key="bankit"


data=["","",""]

@app.route('/login/',methods=['POST','GET'])
def login():
    email=request.form.get('emai')
    password=request.form.get('pas')
    print(email,password)
    cm=dbcon().cursor()
    cm.execute(f'select * from user where email="{email}" and password="{password}"')
    dat=cm.fetchall()
    if dat:
        session['islogin']=True
        session['email']=email
        return render_template('verified.html')
    else:
        return render_template('main.html',msgforl="Email Or Password Invalid")
  

@app.route('/account/')
def account():
    s = dbcon().cursor()
    s.execute(f"SELECT * FROM account WHERE email='{session.get('email')}'")
    dat=s.fetchall()[0]
    print(dat)
    if dat:
        return render_template('account.html',depo=dat[3],witah=dat[4],cur=dat[2],accno=dat[1],msg="")
#    a.execute(f'insert into account values("{session.get('email')}",{int(lte)+1},{dm},0,0,"{cholder}",{pin})')
    
    else:
        return render_template('newaccount.html')
@app.route('/acc/',methods=['POST','GET'])
def acc():
 cholder=request.form.get('chn')
 pin=request.form.get('pin')
 dm = request.form.get('def')
 j = dbcon()
 a = j.cursor()
 a.execute("select * from account;")
 lte=10001
 exe=0
 for x in a.fetchall():
     lte=x[1]
     exe=exe+1
 try:
  if exe == 0:
    a.execute(f'insert into account values("{session.get('email')}",10001,{dm},0,0,"{cholder}",{pin})')
    j.commit()
    return render_template('account.html',depo=0,witah=0,cur=dm,accno=10001,msg="")
  else:
    a.execute(f'insert into account values("{session.get('email')}",{int(lte)+1},{dm},0,0,"{cholder}",{pin})')
    j.commit()
    return render_template('account.html',depo=0,witah=0,cur=dm,accno=int(lte)+1,msg="")
 except:
   return render_template('account.html',depo=0,witah=0,cur=dm,accno=int(lte),msg="")

     

@app.route('/')
def index():
    if session.get('islogin'):
      return render_template('verified.html')
    else:
      return render_template('main.html',msgfors="")
@app.route('/signup/' ,methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('main.html',msgfors="")
    else:
        global data
        if not pass_validate(request.form.get('pass')):
            return render_template('main.html',msgfors="Password Not Meet Requirement")
        data[0]=request.form.get('fn')
        data[1]=request.form.get('email')
        data[2]=request.form.get('pass')
        global otpa
        ot = random.randint(1000,9999)
        otpa=ot
        send_email(ot,data[1])
        return render_template('otp.html')


@app.route('/logout/')
def logout():
      session['islogin']=False
      session['email']=""
      return render_template('main.html')  
   


@app.route('/otpcheck/',methods=['GET','POST'])
def check_otp():
   otp = request.form.get('otp')
   global otpa
   global data
   if int(otp) == otpa:
      session['islogin']=True
      session['email']=data[1]
      otpa=0
      
      dba = dbcon()
      db=dba.cursor()
      try:
       db.execute(f"insert into user values('{data[0]}','{data[1]}','{data[2]}')")
      except:
         return render_template('main.html', msgfors="Email already exists",msgforl="")
      dba.commit()
      db.close()
      data=["","",""]
      return render_template('verified.html')
   else:
      otpa=0
      data=["","",""]
      return render_template('main.html',msgfors="Otp Is In Correct")


@app.route('/depo/', methods=['POST','GET'])
def depo():
   pin = request.form.get('pn')
   mfd=request.form.get('mfd')
   a = dbcon()
   j = a.cursor()
   j.execute(f"select * from account where pin={int(pin)} and email='{session.get("email")}'")
   dat=j.fetchall()[0]
   print(dat)
   if dat:
      j.execute(f"update account set totdepo={int(dat[3])+int(mfd)},curmoney={int(dat[2])+int(mfd)} where pin={int(pin)} and email='{session.get("email")}'")
      a.commit()
      return redirect('/account/')
      
   else:
      j.execute(f"SELECT * FROM account WHERE email='{session.get('email')}'")
      dat=j.fetchall()[0]
      return render_template('account.html',depo=dat[3],witah=dat[4],cur=dat[2],accno=dat[1],msg="Pin Incorrect")

@app.route('/witha/',methods=['GET','POST'])
def witha():
   mfw = request.form.get('mfw')
   pina= request.form.get('pina')
   a = dbcon()
   j = a.cursor()
   j.execute(f"select * from account where pin={int(pina)} and email='{session.get("email")}'")
   dat=j.fetchall()[0]
   print(dat)
   if dat:
      if int(dat[2])>int(mfw):
       j.execute(f"update account set totwidr={int(dat[3])+int(mfw)},curmoney={int(dat[2])-int(mfw)} where pin={int(pina)} and email='{session.get("email")}'")
       a.commit()
       return redirect('/account/')
      else:
        j.execute(f"SELECT * FROM account WHERE email='{session.get('email')}'")
        dat=j.fetchall()[0]
        return render_template('account.html',depo=dat[3],witah=dat[4],cur=dat[2],accno=dat[1],msg="Money Is Grater")  
   else:
      j.execute(f"SELECT * FROM account WHERE email='{session.get('email')}'")
      dat=j.fetchall()[0]
      return render_template('account.html',depo=dat[3],witah=dat[4],cur=dat[2],accno=dat[1],msg="Pin Incorrect")   
   

@app.route('/about/')
def about():
   return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)