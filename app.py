from flask import Flask, request, render_template, redirect, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "IAMCOOL1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []


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

    if num == 0:
        return render_template("q_one.html", question=q1, options=c1)
    elif num == 1:
        return render_template("q_two.html", question=q2, options=c2)
    elif num == 2:
        return render_template("q_three.html", question=q3, options=c3)
    elif num == 3:
        return render_template("q_four.html", question=q4, options=c4)
    elif num == 4:
        return redirect("/thanks")

    else:
        flash('invalid question')
        print("workeddddd")
        return redirect(f"/questions/{len(responses)}")


@app.route("/thanks")
def thanks():
    title = satisfaction_survey.title
    return render_template("thanks.html", title=title)


@app.route("/answer", methods=["POST"])
def answers():
    response = request.form.get('answer')
    responses.append(response)
    print(responses)

    num = len(responses)
    if num >= len(satisfaction_survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{num}")
