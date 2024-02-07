from flask import Blueprint,render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data=request.form
    print(data)
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return('kijelentkezes')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        if len(email) < 3:
            flash('Email cím nem lehet rövidebb mint 3 karakter', category='error')
        elif len(username) < 4:
            flash('A felhasználónév nem lehet rövidebb mint 4 karakter', category='error')
        elif password1 != password2:
            flash('Nem egyeznek a jelszavak', category='error')
        elif len(password1) < 6:
            flash('Jelszó nem lehet rövidebb mint 6 karakter', category='error')
        else:
            flash('A fiók sikeresen létrehozva', category='success')
        
    return render_template('register.html')