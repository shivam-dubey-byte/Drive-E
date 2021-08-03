from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import json


with open('config.json','r') as c:
    params = json.load(c)['params']
    #photos = json.load(c)['photos'] ,photos=photos

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-password']
)
app.config['UPLOAD_FOLDER']= params['upload_location']
mail = Mail(app)



if (local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri'] #'sqlite:///nighthowler.sqlite3'
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = params['pro_uri']  # 'sqlite:///nighthowler.sqlite3'


db = SQLAlchemy(app)

'''class Tourney(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=False,nullable=False)
    phone_num= db.Column(db.String(12),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    country = db.Column(db.String(50), unique=False,nullable=False)
    date = db.Column(db.String(10), unique=False, nullable=True)
    tourney_date = db.Column(db.String(10), unique=False, nullable=False)'''
class Tournamnets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=False, nullable=False)
    title = db.Column(db.String(120),unique=False,nullable=False)
    time = db.Column(db.String(6),unique=False,nullable=False)
    date = db.Column(db.String(11),unique=False,nullable=False)

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),unique=False,nullable=False)
    pass_word = db.Column(db.String(50),unique=False,nullable=False)
    phone_num= db.Column(db.String(12),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)
    country = db.Column(db.String(50), unique=False,nullable=False)

##def pagination():
#    page = request.args.get('page')
#    if (not str(page).isnumeric()):
#        page = 0
#    if (page==1):


@app.route('/',methods= ['GET','POST'])
def hello_world():
    return render_template('index.html',join_us='/sign_up',params=params,login='sign_in',tourney='/tournament')
@app.route('/tournament')
def tourney():
    return render_template('tournament.html',params=params)
@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    #if (request.method == 'POST'):
    return render_template('sign_in.html',form_submit="/form-sign_in",params=params,join_us='/sign_up')
@app.route('/form-sign_in',methods=['POST'])
def form_sign_in_validation():
    user = request.form.get('eamil')
    pass_Key = request.form.get('pass')
    
@app.route('/sign_up')
def sign_up_form():
    return render_template('sign_up.html',sign_up_action='/form-sign_up',params=params,login='sign_in')
@app.route('/form-sign_up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pass')
        phone = request.form.get('phone')
        country = request.form.get('country')

        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients=[params['gmail-user']],
                          body= name + ' : ' + email + ' : ' + country + ' : ' + phone + ' : ' + password
                          )
        '''entry = Users(name=name,phone_num = phone,email=email,country=country,pass_word=password)
        db.session.add(entry)
        db.session.commit()'''

        return render_template('index.html',params=params,join_us='/sign_up')
@app.route('/n-h/<string:post_slug>',methods=['GET'])
def tournament(post_slug):
    team = Tournamnets.query.filter_by(slug = post_slug).first()
    #list = (user.sno,user.name,user.email,user.country,user.phone_num)
    return render_template('dashboard.html',post=team,params=params)

@app.route("/dashboard-admin", methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin-user']:
        datas = Tournamnets.query.all()[-5:]
        return render_template('dashboard.html', login_admin='/admin-login-form',users_joined='/users-joined-admin', params=params,datas =datas)

    if request.method == 'POST':
        username = request.form.get('email')
        userpass = request.form.get('pass')

        if username == params['admin-user'] and userpass == params['admin-password']:
            # set the session variable
            session['user'] = username
            datas = Tournamnets.query.all()[-5:]
            print(datas)
            return render_template('dashboard.html', login_admin='/admin-login-form',users_joined='/users-joined-admin', params=params,datas=datas)

    return render_template('sign_in.html',form_submit='/dashboard-admin',params=params)
@app.route("/edit/<string:id>",methods = ['GET','POST'])
def edit(id):
    if ('user' in session and session['user']== params['admin-user']):
        if request.method =='POST':
            title = request.form.get('title')
            date = request.form.get('date')
            time = request.form.get('time')
            slug = request.form.get('slug')
            if id == '0':
                data = Tournamnets(title = title, date= date, time = time, slug = slug)
                db.session.add(data)
                db.session.commit()
            else:
                data = Tournamnets.query.filter_by(id=id).first()
                data.title = title
                data.date = date
                data.time = time
                data.slug = slug
                db.session.commmit()
                return redirect('/edit/'+id)
        data = Tournamnets.query.filter_by(id=id).first()
        return render_template('edit.html',params=params,data = data)

@app.route('/delete/<string:id>')
def delete_tourny(id):
    if ('user' in session and session['user']== params['admin-user']):
        id = int(id)
        data = Tournamnets.query.filter_by(id = id).first()
        db.session.delete(data)
        db.session.commit()
    return redirect('/dashboard-admin')

 #   if ('user' in session and session['user'] == params['admin-user']):
 #       if request.method == 'POST':
 #           box_title = request.form.get('title')
 #           tline = request.form.get('date')
 #           slug = request.form.get('slug')
 #           content = request.form.get('content')
 #           img_file = request.form.get('img')
 #           if id =='0':
 #               sno.


                #return render_template('dashboard.html', login_admin='/admin-login-form',users_joined='/users-joined-admin', params=params)
#@app.route("/uploader",methodes = ['GET','POST'])
#def uploader():
#    if('uesr' in session and session['user']):
#        if(request.method == 'POST'):
#            f = request.files['file1']
#            f.save(os.path.join(app.config['UPLOAD_FOALDER'],secure_filename(f.filename) ))
#            return 'UPLOAD SUCCESSFULY'
@app.route('/logout')
def log_out():
    session.pop('user')
    return redirect('/dashboard-admin')


@app.route('/admin-login-form')
def admin_login_form_():
    return render_template('sign_in.html',form_submit='/dashboard-admin',params=params)
@app.route('/users-joined-admin')
def users_joined_only_admin():
    return render_template('users_joined.html',params=params)
@app.route('/users-products-admin')
def users_products_only_admin():
    return render_template('products.html',params=params)
@app.route('/users-buyed-product')
def users_ordered_only_admin():
    return render_template('users_ordered.html',params=params)


#@app.route('/form-sign_in', methods="GET"/"POST")
#def accept_form_request_for_sign_in():


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
