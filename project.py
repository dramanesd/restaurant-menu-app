from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', poolclass=SingletonThreadPool)
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

#Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
  return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
  menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
  return jsonify(MenuItem=menuItem.serialize)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
  return render_template('menu.html', restaurant=restaurant, items=items)

# Task 1: Create route for newMenuItem function here

@app.route('/newMenuItem/<int:restaurant_id>/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
    session.add(newItem)
    session.commit()
    flash("new menu item created!")
    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
  else:
    return render_template('newmenuitem.html', restaurant_id=restaurant_id)


# Task 2: Create route for editMenuItem function here

@app.route('/editMenuItem/<int:restaurant_id>/<menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    if request.form['name']:
      editedItem.name = request.form['name']
    session.add(editedItem)
    session.commit()
    flash("Menu Item has been edited!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
    # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
    return render_template(
      'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)



# Task 3: Create a route for deleteMenuItem function here

@app.route('/deleteMenuItem/<int:restaurant_id>/<menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()
    flash("Menu Item has been deleted!")
    return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
  else:
    return render_template('deleteMenuItem.html', i = itemToDelete)


if (__name__) == __name__:
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)