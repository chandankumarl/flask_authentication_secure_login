from flask import Flask,render_template,redirect,request,abort,session , url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.secret_key="your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)


# Database Model
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(25),unique=True,nullable=False)
    password_hash=db.Column(db.String(150),unique=True,nullable=False)

    def set_password(self,password):
        self.password_hash=generate_password_hash(password)

    def check_password(self,password):
        return  check_password_hash(self.password_hash,password)


# login
@app.route('/login',methods=['POST'])
def login():
    # collect info from db
    username=request.form['username']
    password=request.form['password']
    # check if it is present in db/login
    user=User.query.filter_by(username=username).first()  
    print(user)
    if user and user.check_password(password):
        session['username']=username
        return redirect(url_for('dashboard'))
    else: # otherwise show home page
        return render_template('index.html')
    


   

    


# register

@app.route('/register',methods=['POST'])
def register():
    # collect info from db
    username=request.form['username']
    password=request.form['password']
    user=User.query.filter_by(username=username).first()  # check if it is present in db/login
    if user:
        return render_template('index.html',error="user already here")
    else:
        new_user=User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username']=username
        return redirect(url_for('dashboard'))


# dashboard
@app.route('/dashboard')
def dashboard():
    if "username" in session:
        return render_template('dashboard.html',username=session['username'])
    return redirect(url_for('home'))


# logout
# eg. session=['bob','chandan']
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('home'))


# Routes
@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

