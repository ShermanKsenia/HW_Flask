from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func
from collections import Counter
from models import Users, Questions, Answers, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)

@app.route("/")
def instruction():
    return render_template('index.html')

@app.route('/survey')
def survey():
    questions = Questions.query.all()
    return render_template('survey.html', questions=questions)

@app.route("/thank_you")
def thank_you():
    return render_template('thank_you.html')

@app.route('/process', methods=['get'])
def answer_process():
    if not request.args:
        return redirect(url_for('survey'))
    gender = request.args.get('gender')
    zodiac_sign = request.args.get('zodiac_sign')
    age = request.args.get('age')
    languages = request.args.get('languages')
    student = request.args.get('student')
    user = Users(
        age=age,
        gender=gender,
        zodiac_sign=zodiac_sign,
        languages=languages,
        student=student
    )
    db.session.add(user)
    db.session.commit()
    db.session.refresh(user)
    q1 = request.args.get('q1')
    q2 = request.args.get('q2')
    q3 = request.args.get('q3')
    answer = Answers(id=user.id, q1=q1, q2=q2, q3=q3)
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('thank_you'))

@app.route("/statistics")
def statistics():
    all_info = {}
    age_stats = db.session.query(
        func.avg(Users.age),
        func.min(Users.age),
        func.max(Users.age)
    ).one()
    all_info['age_mean'] = round(age_stats[0], 2)
    all_info['age_min'] = age_stats[1]
    all_info['age_max'] = age_stats[2]
    all_info['total_count'] = Users.query.count()
    funny_people = db.session.\
                    query(Users).\
                    join(Answers, Users.id==Answers.id).\
                    filter(Answers.q1 > 3, Answers.q2 > 3, Answers.q3 > 3).all()
    funniest = [f.zodiac_sign for f in funny_people]
    all_info['sign'] = Counter(funniest).most_common(1)[0][0]
    all_info['students_count'] = Users.\
                                query.\
                                filter_by(student='is_student').\
                                count()
    all_languages = db.session.query(Users.languages).all()
    lang = []
    for l in all_languages:
        lang.extend(l[0].split(' '))
    all_info['languages'] = Counter(lang).most_common(3)
    all_info['q1'] = round(db.session.query(func.avg(Answers.q1)).\
                            one()[0], 2)
    all_info['q2'] = round(db.session.query(func.avg(Answers.q2)).\
                            one()[0], 2)
    all_info['q3'] = round(db.session.query(func.avg(Answers.q3)).\
                            one()[0], 2)
    return render_template('statistics.html', all_info=all_info)

if __name__ == "__main__":
    app.run()
