from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "kodland"

# Database oluşturma
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Score {self.username}: {self.score}>'

with app.app_context():
    db.create_all()

#en yüksek skoru alır
def get_best_score(username=None):

    # Genel en yüksek skor
    general_best_score = Score.query.order_by(Score.score.desc()).first()
    if general_best_score:
        general_best = general_best_score.score
    else:
        general_best = 0
    
    # Kişisel en yüksek skor
    personal_best = None
    if username:
        personal_best_score = Score.query.filter_by(username=username).order_by(Score.score.desc()).first()
        if personal_best_score:
            personal_best = personal_best_score.score
        else:
            personal_best = None
    
    return general_best, personal_best

@app.route('/', methods=['GET'])
def index():
    username = request.args.get('username', '') 

    #quiz sayfası için en yüksek skor alınır
    general_best, personal_best = get_best_score(username)

    return render_template('index.html', username=username, general_best=general_best, personal_best=personal_best)

#Kullanıcı adı alınır
@app.route('/username', methods=['GET'])
def username():
    username = request.args.get('username', '')
    return redirect(url_for('index', username=username))

#Soruların cevapları alınır
@app.route('/quiz', methods=['POST'])
def quiz():
    username = request.form.get('username')
    
    soru1 = request.form.get('soru1')
    soru2 = request.form.get('soru2')
    soru3 = request.form.get('soru3')
    soru4 = request.form.get('soru4')
    soru5 = request.form.get('soru5')

#puan hesaplaması
    score = 0
    if soru1 == "b":
        score += 20
    if soru2 == "c":
        score += 20
    if soru3 == "b":
        score += 20
    if soru4 == "c":
        score += 20
    if soru5 == "d":
        score += 20

    # skoru db'ye kaydet
    newScore = Score(username=username, score=score)
    db.session.add(newScore)
    db.session.commit()

    #sonuç sayfası için en yüksek skor alınır.
    general_best, personal_best = get_best_score(username)
    
    if personal_best is None:
        personal_best = score

    return render_template('result.html', username=username, score=score, personal_best=personal_best, general_best=general_best)

if __name__ == '__main__':
    app.run(debug=True)