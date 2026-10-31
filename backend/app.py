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
@app.route('/faculty')
def faculty():
    return render_template('faculty_dashboard.html')
@app.route('/subjects')
def subjects():
    return render_template('manage_subjects.html')
@app.route('/mark-attendance')
def mark_attendance():
    return render_template('mark_attendance.html')
@app.route('/attendance-records')
def attendance_records():
    return render_template('attendance_records.html')
@app.route('/attendance-history')
def attendance_history():
    return render_template('attendance_history.html')


if __name__ == '__main__':
    app.run(debug=True)