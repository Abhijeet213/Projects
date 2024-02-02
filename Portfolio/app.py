from flask import Flask,render_template,redirect,request
from flask_mail import Mail
from jinja2 import escape 
app = Flask(__name__)

app.config.update(
 MAIL_SERVER='smtp.gmail.com',
 MAIL_PORT=465,
 MAIL_USE_SSL=True,
 MAIL_USERNAME='techabissa@gmail.com',
 MAIL_PASSWORD='mvuy gxla lobi zmxt',
)
mail=Mail(app)
def send_email(sendto,tit,mes,fn):
 mail.send_message(tit,sender=f"techabissa@gmail.com",recipients=[f'{sendto}'],
                   body=mes+"\n\n"+f"Thanks For Contacting Us - {fn}")
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/conta/',methods=['GET','POST'])
def conta():
    if request.method == 'GET':
        return render_template('conta.html')
    elif request.method == 'POST':
        fn = request.form.get('fn')
        email = request.form.get('email')
        desc = request.form.get('desc')
        send_email(email,"Thanks For Contacting Us","Your Message Has Been Sended To Our Costumer Service\nWait 2-3 Days From Now For Replay",fn)
        send_email("techabissa@gmail.com",f"Query From {fn}",desc+f"\nEmail -> {email}",fn)
        return render_template('conta.html')
    
@app.route('/about/')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)