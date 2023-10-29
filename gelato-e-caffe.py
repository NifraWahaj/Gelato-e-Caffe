from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/menu')
def menu():
    return render_template('Menu.html')

@app.route('/reviews')
def reviews():
    return render_template('Reviews.html')

@app.route('/signup')
def signup():
    return render_template('SignUp.html')

@app.route('/login')
def login():
    return render_template('LogIn.html')

if __name__ == '__main__':
    app.run(debug=True)
