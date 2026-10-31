from flask import Flask, render_template

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'frontend', 'static')
)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/admin')
def admin():
    return render_template('admin_dashboard.html')
@app.route('/student')
def student():
    return render_template('student_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)