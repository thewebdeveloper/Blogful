from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Entry


PAGINATE_BY = 10 # Constant (by convenion)

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
    
   
@app.route("/entry/<id>")
def entry(id):
    entry = session.query(Entry).get(id)
    return render_template("entry.html", entry=entry)
    

@app.route("/entry/<id>/edit", methods=["GET"])
def edit_entry_get(id):
    entry = session.query(Entry).get(id)
    return render_template("edit_entry.html", entry=entry)

    
@app.route("/entry/<id>/edit", methods=["POST"])
def edit_entry_put(id):
    entry = session.query(Entry).get(id)
    entry.title = request.form["title"],
    entry.content = request.form["content"]
    session.commit()
    return redirect(url_for("entry", id=id))
    
    
@app.route("/entry/<id>/delete", methods=['GET'])
def delete_entry(id):
    entry = session.query(Entry).get(id)
    session.delete(entry)
    session.commit()
    return redirect(url_for("entries"))