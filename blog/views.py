from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry


PAGINATE_BY = 10 # Constant (by convenion)

@app.route("/")
@app.route("/page/<int:page>")
def entries(page=1):
    # Zero-indexed page
    page_index = page - 1
    
    count = session.query(Entry).count()
    
    start = page_index * PAGINATE_BY
    end = start + PAGINATE_BY
    
    total_pages = (count-1) // PAGINATE_BY + 1 # dividing the total records by 10, will give us the total page
    has_next = page_index < total_pages - 1 # checking whether it has next, if the indexed page is less that total pages. 
    has_prev = page_index > 0 # checking whether it has prev, if the indexed page is greater than 0.
    
    entries = session.query(Entry).order_by(Entry.datetime.desc())
    entries = entries[start:end]
    
    return render_template("entries.html", 
        entries = entries,
        page = page,
        total_pages = total_pages,
        has_prev = has_prev,
        has_next = has_next
    )
    
    
@app.route("/entry/add", methods=["GET"])
def add_entry_get():
    return render_template("add_entry.html")
    
    
@app.route("/entry/add", methods=["POST"])
def add_entry_post():
    entry = Entry(
        title = request.form["title"],
        content = request.form["content"],
    )
    session.add(entry)
    session.commit()
    
    return redirect(url_for("entries"))