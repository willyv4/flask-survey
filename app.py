from flask import Flask, session, flash, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "IAMCOOL1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/sesh', methods=["POST"])
def sesh_response():
    """ create an empty session list of responses 
    and redirect user to first question """

    session['responses'] = []
    sesh_len = len(session['responses'])
    return redirect(f'/questions/{sesh_len}')


@app.route("/")
def root():
    """ define root route pass survey title and instructions
    for base.html to display """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("base.html", title=title, instructions=instructions)


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def view(num):
    """ define each path for each question"""

    q = [item.question for item in satisfaction_survey.questions]
    q1, q2, q3, q4 = q[:4]

    c = [item.choices for item in satisfaction_survey.questions]
    c1, c2, c3, c4 = c[:4]

    sesh_res = session.get('responses', [])
    len_sesh = len(sesh_res)

    if len_sesh >= 4:
        return redirect("/thanks")
    elif num == 0 and len_sesh == 0:
        return render_template("q_one.html", question=q1, options=c1)
    elif num == 1 and len_sesh == 1:
        return render_template("q_two.html", question=q2, options=c2)
    elif num == 2 and len_sesh == 2:
        return render_template("q_three.html", question=q3, options=c3)
    elif num == 3 and len_sesh == 3:
        return render_template("q_four.html", question=q4, options=c4)
    else:
        flash('invalid question')
        return redirect(f"/questions/{len_sesh}")


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

    q_len = len(satisfaction_survey.questions)
    num = len(responses)
    if num >= q_len:
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{num}")
