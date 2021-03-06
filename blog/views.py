from flask import render_template, request, redirect, url_for, flash, g
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import check_password_hash

from . import app
from .database import session, Entry, User


PAGINATE_BY = 10 # Constant (by convenion)

@app.before_request
def before_request():
    g.user = current_user


@app.route("/")
@app.route("/page/<int:page>")
@app.route("/<int:limit>")
@app.route("/page/<int:page>/<int:limit>")
def entries(limit=10, page=1):
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    limit = request.args.get('limit', limit)
    
    try:
        limit = int(limit)
        print(limit)
        if limit > 0 and limit < 21:
            start = page_index * limit
            end = start + limit
            total_pages = (count-1) // limit + 1 # dividing the total records by 10, will give us the total page
            
            has_next = page_index < total_pages - 1 # checking whether it has next, if the indexed page is less that total pages. 
            has_prev = page_index > 0 # checking whether it has prev, if the indexed page is greater than 0.
            
            entries = session.query(Entry).order_by(Entry.datetime.desc())
            entries = entries[start:end]
            
            return render_template("entries.html", 
                entries = entries,
                page = page,
                total_pages = total_pages,
                has_prev = has_prev,
                has_next = has_next,
                limit = limit
            )
            
        else:
            limit = 'Please use from the dropdown list for your search on entries per page'
            return render_template("entries.html", limit = limit)
        
    except ValueError:
        print ('value error occured')
        limit = 'Float numbers and Text are not allowed in the search!! kindly stick with the dropdown list'
        return render_template("entries.html", limit = limit)
    

@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")
    
    
@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title = request.form["title"],
        content = request.form["content"],
        author = current_user
    )
    session.add(entry)
    session.commit()
    
    return redirect(url_for("entries"))
    
   
@app.route("/entry/<id>")
def entry(id):
    entry = session.query(Entry).get(id)
    return render_template("entry.html", entry=entry)
    

@app.route("/entry/<id>/edit", methods=["GET"])
@login_required
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("edit_entry.html", entry=entry)

    
@app.route("/entry/<id>/edit", methods=["POST"])
@login_required
def edit_entry_put(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"],
    entry.content = request.form["content"],
    entry.author = current_user
    session.commit()
    return redirect(url_for("entry", id=id))
    
    
@app.route("/entry/<id>/delete", methods=['GET'])
@login_required
def delete_entry(id):
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))
    
    
@app.route("/login", methods=['GET'])
def login_get():
    return render_template("login.html")
    
    
@app.route("/login", methods=['POST'])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect Username or Password", "danger")
        return redirect(url_for("login_get"))
        
    login_user(user)
    flash("Logged in successfully.", "success")
    
    return redirect(request.args.get("next") or url_for("entries"))
    
    
@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for("entries"))