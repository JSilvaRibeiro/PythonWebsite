from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from sqlalchemy import func
from flask_login import login_required, current_user
from .models import Note, WorkOrder
from . import db
from .forms import CreateWorkOrderForm
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category ='error')
        else:
            new_note = Note(data = note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note was added!', category='success')



    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id :
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/create_work_order', methods=['GET', 'POST'])
@login_required
def create_work_order():
    form = CreateWorkOrderForm()
    if form.validate_on_submit():
        work_order_number = WorkOrder.query.with_entities(func.max(WorkOrder.work_order_number)).scalar() or 0
        new_work_order = WorkOrder(
            work_order_number=work_order_number + 1,
            client_name=form.client_name.data,
            job_address=form.job_address.data,
            start_date=form.start_date.data,
            floor_prep=form.floor_prep.data,
            floor_type=form.floor_type.data,
            baseboards=form.baseboards.data,
            materials=form.materials.data,
            user_id=current_user.id
        )
        db.session.add(new_work_order)
        db.session.commit()
        flash('Work order created successfully!', category='success')
        return redirect(url_for('views.orders'))
    return render_template('create_work_order.html', user=current_user, form=form)


@views.route('/orders')
@login_required
def orders():
    user = current_user
    orders = WorkOrder.query.filter_by(user_id=user.id).all()
    return render_template('orders.html', orders=orders, user=user)


@views.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    user = current_user
    order = WorkOrder.query.get_or_404(order_id)
    form = CreateWorkOrderForm(obj=order)
    if form.validate_on_submit():
        form.populate_obj(order)
        db.session.commit()
        flash('Order updated successfully.', 'success')
        return redirect(url_for('views.orders'))
    return render_template('edit_order.html', form=form, user=user)


@views.route('/orders/delete/<int:order_id>', methods=['POST'])
@login_required
def delete_order(order_id):
    order = WorkOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order deleted successfully.', 'success')
    return redirect(url_for('views.orders'))
