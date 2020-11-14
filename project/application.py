# CS50 Fall 2020
# Final Project
# Author: kkphd

from flask import Flask, redirect, render_template, request, session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import math


# Configure an instance of the Flask class
application = Flask(__name__)


# Ensure responses aren't cached
@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@application.route('/', methods=["GET", "POST"])
def cpt_calc():
    """Calculate the CPT codes based on user input"""

    if request.method == "POST":
            testmin = float(request.form.get("techTestMin"))
            scoremin = float(request.form.get("techScoreMin"))
            computerTestCheckBox = request.form.get("computer-test-checkbox")

            # If the "Computer Testing" prompt is selected, indicate as such
            if computerTestCheckBox:
                compCheckBox = "✓"
            else:
                compCheckBox = ""

            testhr = testmin / 60
            scorehr = scoremin / 60
            totalmin = testmin + scoremin
            totalhr = totalmin / 60

            # Calculate time for 96138 ("eight") and work towards calculating 96139 ("nine")
            eight_min = 30
            remaining = totalmin - 30

            # Calcuate the technician's remaining time divided by 30 to determine whether the person meets the cutoff for >50% of unit 96138
            remaining_30 = remaining / 30

            # Round the whole number down
            remaining_floor = math.floor(remaining_30)
            fractional, whole = math.modf(remaining_30)

            # Cutoff is set at 16 out of 30 minutes
            cutoff = 0.53

            # Add an extra unit to 96139 if user input meets the cutoff
            if fractional >= cutoff:
                extra = 1
            else:
                extra = 0

            if eight_min == 30:
                eight = 1

            nine = remaining_floor + extra

            return render_template('/index.html', techTestMin=testmin, techScoreMin=scoremin, techTestHr=round(testhr, 2),
                                   testScoreHr=round(scorehr, 2),techTotalHr=round(totalhr, 2), techTotalMin=round(totalmin, 2),
                                   eight=eight, nine=nine, neurCheckBox=compCheckBox)
    else:
        return render_template("index.html")


def apology(message, code=400):
    """Error message"""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    application.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    application.run()
