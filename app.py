from urllib import response
from flask import Flask, session, flash, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "IAMCOOL1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
q_len = len(satisfaction_survey.questions)


@app.route('/sesh', methods=["POST"])
def sesh_response():

    session['responses'] = []
    sesh_len = len(session['responses'])
    print(session['responses'])
    return redirect(f'/questions/{sesh_len}')


@app.route("/")
def root():

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("base.html", title=title, instructions=instructions)


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def view(num):

    q = [item.question for item in satisfaction_survey.questions]
    q1, q2, q3, q4 = q[:4]

    c = [item.choices for item in satisfaction_survey.questions]
    c1, c2, c3, c4 = c[:4]

    sesh_len = len(session['responses'])

    if sesh_len == 0:
        return render_template("q_one.html", question=q1, options=c1)
    elif sesh_len == 1:
        return render_template("q_two.html", question=q2, options=c2)
    elif sesh_len == 2:
        return render_template("q_three.html", question=q3, options=c3)
    elif sesh_len == 3:
        return render_template("q_four.html", question=q4, options=c4)
    elif sesh_len == 4:
        return redirect("/thanks")
    elif sesh_len > 4 or sesh_len < 0:
        flash('invalid question')
        return redirect(request.referrer)
    else:
        flash('invalid question')
        print("workeddddd")
        return redirect(request.referrer)


@app.route("/thanks")
def thanks():
    title = satisfaction_survey.title
    return render_template("thanks.html", title=title)


@app.route("/answer", methods=["POST"])
def answers():
    answer = request.form['answer']
    responses = session.get('responses', [])
    responses.append(answer)
    session['responses'] = responses
    print(session['responses'])

    num = len(responses)
    if num >= q_len:
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{num}")
