from flask import Flask, jsonify, request, abort, render_template
from models import db, Cupcake

# Initialize the Flask application
app = Flask(__name__)

# Application configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

# Initialize the SQLAlchemy instance with the app
db.init_app(app)

@app.route('/')
def index():
    """Return the homepage."""
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Get data about all cupcakes."""
    cupcakes = Cupcake.query.all()
    cupcakes_data = [
        {"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image}
        for cupcake in cupcakes
    ]
    return jsonify(cupcakes=cupcakes_data)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get data about a single cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake_data = {
        "id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a new cupcake."""
    data = request.json

    if not data or 'flavor' not in data or 'size' not in data or 'rating' not in data:
        abort(400, "Missing required fields: flavor, size, rating.")

    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=float(data['rating']),
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')  # Use default if image is not provided
    )
    db.session.add(cupcake)
    db.session.commit()

    cupcake_data = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data), 201

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update an existing cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = float(data.get('rating', cupcake.rating))
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()

    cupcake_data = {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }
    return jsonify(cupcake=cupcake_data)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake."""
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
