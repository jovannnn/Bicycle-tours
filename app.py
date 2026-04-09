from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# Конфигурација за база на податоци со MySQL и SQLite кога се работи локално и во реална продукција
if os.getenv("FLASK_ENV") == "production":
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registrations.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модел за регистрација
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    ime_tura = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Registration {self.first_name} {self.last_name}>'

# Креирање на базата и табелите ако не постојат
with app.app_context():
    db.create_all()

# Почетна страница
@app.route('/')
def index():
    return render_template('index.html')

# Почетна страница на англиски јазик
@app.route('/index_en')
def index_en():
    return render_template('index_en.html')    

# Галерија на англиски јазик
@app.route('/gallery_en')
def gallery_en():
    return render_template('gallery_en.html')    

# Соопштение на англиски јазик
@app.route('/soop_en')
def soop_en():
    return render_template('soop_en.html') 

# Рута за процесирање на формата за пријава
@app.route('/register', methods=['POST'])
def register():
    jazik = request.form.get('jazik', 'mk')

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    ime_tura = request.form['ime_tura']

    try:
        new_registration = Registration(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            ime_tura=ime_tura
        )
        db.session.add(new_registration)
        db.session.commit()

        if jazik == 'en':
            flash(
                f"Thank you {first_name}! Your registration was successful.",
                "success"
            )
            return redirect(url_for('index_en') + '#registration')
        else:
            flash(
                f"Благодарам {first_name}! Успешно се пријавивте.",
                "success"
            )
            return redirect(url_for('index') + '#registration')

    except Exception as e:
        db.session.rollback()

        if jazik == 'en':
            flash(
                "An error occurred. Please try again.",
                "error"
            )
            return redirect(url_for('index_en') + '#registration')
        else:
            flash(
                "Настана грешка. Обидете се повторно.",
                "error"
            )
            return redirect(url_for('index') + '#registration')

# Рута за прикажување на сите пријавени учесници
@app.route('/registrations')
def show_registrations():
    registrations = Registration.query.all()
    return render_template('registrations.html', registrations=registrations)

# Рута за логирање
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        admin_password = os.getenv('ADMIN_PASSWORD') 
        if password == admin_password:
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            return 'Невалидна лозинка!'
    return render_template('login.html')

# Заштитена рута за административниот панел
@app.route('/admin')
def admin_panel():
    if not session.get('admin'):  
        return redirect(url_for('login'))  
    registrations = Registration.query.all()
    return render_template('admin_panel.html', registrations=registrations)

# Рута за бришење на запис
@app.route('/delete/<int:id>')
def delete_registration(id):
    registration = Registration.query.get(id)
    if registration:
        db.session.delete(registration)
        db.session.commit()
    return redirect(url_for('admin_panel'))

# Рута за одјава
@app.route('/logout')
def logout():
    session.pop('admin', None)  
    return redirect(url_for('login'))

# Рута за страната соопштение
@app.route('/soop')
def soop():
    return render_template('soop.html')

# Рута за страната галерија
@app.route('/gallery')
def gallery():
    return render_template('galerija.html')

if __name__ == '__main__':
    app.run(debug=True)


