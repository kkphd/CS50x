# CS50 Fall 2020
# Problem Set 8
# Author: kkphd

import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd
from collections import defaultdict
import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Streamline the active transaction database
    rows = db.execute("SELECT symbol, SUM(shares), SUM(total) FROM active WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares)>0", user_id=session["user_id"])

    # Make an empty dictionary object to store the stock information and a total_funds variable set to zero (to avoid 'reference before assignment' error)
    table = []
    total_funds = 0

    # Iterate through each row and add it to the 'table' dictionary
    for row in rows:
        result = lookup(row["symbol"])
        new_row = [row['symbol'], result['name'], row['SUM(shares)'], usd(round(result['price'], 2)), usd(round(row['SUM(total)'], 2))]
        table.append(new_row)
        total_funds += row["SUM(total)"]

    # Calculate total funds (stock + cash reserve)
    transactions = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash = transactions[0]["cash"]
    total_funds += cash

    return render_template("index.html", table=table, cash=usd(cash), total_funds=usd(total_funds))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = int(request.form.get("shares"))
        result = lookup(symbol)

        if not result:
            return apology("Invalid stock symbol", 403)
        elif amount <= 0:
            return apology("Invalid number of shares", 403)

        price=result["price"]
        cost=price * amount

        # Determine the available cash
        rows=db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash=rows[0]["cash"]

        # Determine the date
        time=datetime.datetime.utcnow()

        if cost < cash:
            remaining = cash - cost
            db.execute("UPDATE users SET cash = :remaining WHERE id = :id", remaining=remaining, id=session["user_id"])

            # Update the active table with the new transaction ('active' previously established using phpliteadmin)
            db.execute("INSERT INTO active(user_id, symbol, shares, price, total, date) VALUES(:user_id, :symbol, :shares, :price, :total, :date)", user_id=session["user_id"], symbol=symbol, shares=amount, price=price, total=cost, date=time)
            flash("Purchased " + str(amount) + " share(s) of " + symbol + " stock")
        else:
            return apology("Not enough cash", 403)

        return redirect("/")
    else:
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT symbol, shares, price, total, date FROM active WHERE user_id = :user_id", user_id=session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        result = lookup(symbol)

        name=result['name']
        price=usd(result['price'])
        symbol=result['symbol']

        if not result:
            return apology("Invalid stock symbol", 403)
        return render_template("quoted.html", name=name, price=price, symbol=symbol)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmed_pw = request.form.get("confirmation")

        if username == None:
            return apology("Enter username", 403)
        elif password == None:
            return apology("Enter password", 403)
        elif password != confirmed_pw:
            return apology("Passwords must match", 403)


        # Make sure the username is unique (i.e., there should be no record of it in the database)
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)

        if len(rows) != 0:
            return apology("Input a new username", 403)

        hashed_pw = generate_password_hash(password)
        new_user = db.execute("INSERT INTO users(username, hash) VALUES(:username, :hash)", username=username, hash=hashed_pw)

        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = int(request.form.get("shares"))
        result = lookup(symbol)

        if not result:
            return apology("Invalid stock symbol", 403)
        elif amount <= 0:
            return apology("Invalid number of shares", 403)

        # Determine the price of each stock
        price=result["price"]

        # Determine the expected increase in funds based on the sale
        cost=price*amount

        # Determine updated balance based on sale
        current_cash=db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])[0]["cash"]
        updated_cash=current_cash + cost

        # If user does not have enough money, issue a warning
        if updated_cash < 0:
            return apology("Out of funds", 403)

        rows = db.execute("SELECT SUM(shares) FROM active WHERE symbol = :symbol AND user_id = :user_id", symbol=symbol, user_id=session["user_id"])

        # If user desires to sell more shares than what is possessed, issue a warning
        if amount > rows[0]["SUM(shares)"]:
            return apology("Sell count exceeds available amount", 403)

        # Date of sale
        time=datetime.datetime.utcnow()

        # Update master and active databases
        db.execute("UPDATE users SET cash=:updated_cash WHERE id = :user_id", updated_cash=updated_cash, user_id=session["user_id"])
        db.execute("INSERT INTO active(user_id, symbol, shares, price, total, date) VALUES (:user_id, :symbol, :shares, :price, :total, :date)", user_id=session["user_id"], symbol=symbol, shares=-amount, price=price, total=cost, date=time)

        flash("Sold " + str(amount) + " share(s) of " + symbol + " stock")

        return redirect("/")
    else:
        # Iterate through database to select symbols for dropdown menu (if shares > 0)
        rows = db.execute("SELECT DISTINCT symbol FROM active WHERE user_id = :user_id HAVING shares > 0", user_id=session["user_id"])

        symbols = []
        for row in rows:
            symbols.append(row['symbol'])

        return render_template("sell.html", symbols=symbols)

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

@app.route("/changepw", methods=["GET", "POST"])
@login_required
def change_pw():
    """Allow users to change their password"""

    hashed_current_pw = db.execute("SELECT hash FROM users WHERE id = :id", id=session["user_id"])[0]["hash"]

    if request.method == "POST":
        entered_old_pw = request.form.get("oldpw")
        entered_new_pw = request.form.get("newpw")
        confirmed = request.form.get("confirmation")

        correct = check_password_hash(hashed_current_pw, entered_old_pw)
        print(correct)

        if correct == False:
            return apology("Password is incorrect", 403)
        elif entered_new_pw != confirmed:
            return apology("New passwords do not match", 403)

        hashed_new_pw = generate_password_hash(entered_new_pw)

        db.execute("UPDATE users SET hash = :new_password WHERE id = :id", new_password=hashed_new_pw, id=session["user_id"])
        flash("Changed password!")

        return redirect("/")
    else:
        return render_template("changepw.html")




