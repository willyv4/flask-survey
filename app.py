from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey
from jinja2 import Environment


app = Flask(__name__)

app.config['SECRET_KEY'] = "IAMCOOL1234"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
print(responses)


@app.route("/")
def root():

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("base.html", title=title, instructions=instructions)


@app.route("/questions/<int:num>", methods=["GET", "POST"])
def question(num):
    if request.method == "POST":
        # Process the user's response and store it
        # in a database or session variable, if necessary
        pass
    env = Environment()
    env.globals.update(enumerate=enumerate)

    question = satisfaction_survey.questions[num].question
    options = satisfaction_survey.questions[num].choices

    if num == 0:
        return render_template("q_one.html", question=question, options=options)
    elif num == 1:
        return render_template("q_two.html", question=question, options=options)
    elif num == 2:
        return render_template("q_three.html", question=question, options=options)
    elif num == 3:
        return render_template("q_four.html", question=question, options=options)
    else:
        return "Invalid question number"


@app.route("/answer", methods=["POST"])
def answers():
    response = request.form.get('answer')
    responses.append(response)
    print(response)
    print(responses)

    num = len(responses)
    if num == len(satisfaction_survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{num}")
