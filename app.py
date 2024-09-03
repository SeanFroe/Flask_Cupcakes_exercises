"""Flask app for Cupcakes"""
from flask import Flask, url_for, render_template, request, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake
# from forms import AddCupcakeForm, EditCupcakeForm


app = Flask(__name__)

app.config['SECRET_KEY'] = 'cupcake'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcake"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():

    connect_db(app)
    

app.config['DEBUG_TB_ENABLED'] = True
app.config['DEBUG_TB)_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)
# ####################################################################

@app.route("/")
def root():
    """Render Homepage."""

    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)

# #####################################################################

# /api/cupcakes routes

#  ------------------------ GET REQUEST ---------------------------

@app.route("/api/cupcakes", methods=["GET"])
def list_cupcake():
    """Return all cupcakes in system.
    
    Return JSON like:
    {cupcakes: [{id, flavor, rating, size, image}, ...]}
    """

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)


@app.route("/api/cupcakes/<int:cupcake_id>")
def get_cupcake(cupcake_id):
    """Return data on specific cupcake
    
    Returns JSON like:
    {cupcake: [{ id, flavor, rating, size, image}]}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

# --------------------------- POST REQUEST --------------------------

@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """Add cupcake, and return data about new cupcake
    
    Returns JSON like:
    {cupcake: [{id, flavor, rating, size, image}]}
    """
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] if data.get('image') else None
    )

    db.session.add(cupcake)
    db.session.commit()
    new_cupcake =jsonify(cupcake=cupcake.to_dict())
    # POST requests should return HTTP status of 201 CREATED
    return (new_cupcake, 201)

#  --------------------------- PATCH REQUEST --------------------------

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update cupcake from data in request. Return update data
    
    Return JSON like:
    {cupcake: [{id, flavor, rating, size, image}]}  
    """
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.rating = data['rating']
    cupcake.size = data['size']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def remove_cupcake(cupcake_id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

# ###########################################################
