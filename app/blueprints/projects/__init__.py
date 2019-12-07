from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from flask_login import login_required, current_user
from app import app, db, login
from app.blueprints.projects.stripe import stripeProductsList, convert_price
import math, statistics, mysql.connector, os, stripe

bp = Blueprint('projects', __name__, template_folder='templates')

def checkCartSession():
    try:
        return session['cart']
    except:
        session['cart'] = []

@bp.route('/ecommerce')
@login_required
def ecommerce():
    try:
        if not session['cart']:
            pass
    except:
        session['cart'] = list()
    context = {
        'products': stripeProductsList
    }
    return render_template('projects/ecommerce.html', **context)


@bp.route('/ecommerce/cart')
@login_required
def ecommerceCart():
    checkCartSession()
    shallowCart = []
    for i in session['cart']:
        if i not in shallowCart:
            shallowCart.append(i)
    session['grandTotal'] = 0
    for i in session['cart']:
        session['grandTotal'] += i['price']
    context = {
        'products': stripeProductsList,
        'cart': session['cart'],
        'displayCart': shallowCart,
        'grandTotal': round(session['grandTotal'], 2),
    }
    return render_template('projects/ecommerce-cart.html', **context)


@bp.route('/ecommerce/cart/add/product/<id>', methods=['GET', 'POST'])
@login_required
def ecommerceCartAdd(id):
    p = stripe.SKU.retrieve(id)
    product = dict(
        id=p.id,
        prod_id=p.product,
        name=p.attributes.name,
        image=p.image,
        price=convert_price(p.price)
    )
    if request.form.get('modal-product-quantity'):
        select = request.form.get('modal-product-quantity')
        for i in range(0, int(select)):
            session['cart'].append(product)
    else:
        session['cart'].append(product)
    session['cart-count'] = 0
    session['cart-count'] = len(session['cart'])
    flash(f"[{product['name']}] added to cart", "info")
    return redirect(url_for('projects.ecommerce'))


@bp.route('/ecommerce/cart/clear')
@login_required
def ecommerceCartClear():
    if session['cart']:
        session['cart'] = list()
        flash("Cart emptied successfully", "info")
    else:
        flash("Your cart is already empty", "warning")
    return redirect(url_for('projects.ecommerce'))

@bp.route('/ecommerce/cart/remove/<id>')
@login_required
def ecommerceCartRemove(id):
    for p in session['cart']:
        if p['id'] == id:
            session['cart'].remove(p)
    flash(f"[{p['name']}] removed from cart", "info")
    return redirect(url_for('projects.ecommerce'))



@bp.route('/databases')
@login_required
def databases():
    context = {}
    return render_template('projects/databases.html', **context)
