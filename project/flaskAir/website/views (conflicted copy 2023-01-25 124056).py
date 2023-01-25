from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from .models import User, Seat
import json


'''defines routes for "home", "help" and functionality for the website itself'''

# create Blueprint for views
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    TODO: change to include personal info of current_user OR directly go to 'reserve Seats' view!
    """

    return render_template("home.html", user=current_user)


@views.route('/export2file', methods=['POST'])
def export2file():
    all_users = User.query.all(),
    all_seats = Seat.query.all(),
    free_seats = Seat.query.filter_by(user_id=None).all()
    number_of_seats = len(all_seats)
    number_free_seats = len(free_seats)
    if current_user.is_admin:
        with open('./seatinfo.txt', 'a+') as seatinfo:
            timeinfo = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if number_of_seats != 0:
                seatinfo.write(f"{timeinfo}:\tseats available: {number_free_seats}\tall seats: {number_of_seats}\t{(number_free_seats / number_of_seats) * 100} % available\n")
                flash('sucessfully written seatinfo', category='success')
            else:
                seatinfo.write(f"{timeinfo}:\t \
                                    seats available: {number_free_seats}\t \
                                    all seats: {number_of_seats}\t ")
        return render_template("admin.html", user=current_user, all_seats=all_seats, free_seats=free_seats, all_users=all_users)
    else:
        flash("This functionality is for admins only!", category='error')
        return redirect(url_for('views.home'))


''' 
TODO: Take this as an example how functionality in Flask can be constructed with jsonify

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
'''


@views.route('/help')
def help():
    return render_template("help.html", user=current_user)
