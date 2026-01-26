import flask
import json
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# ---------------- Global cars data ----------------
cars = []

def load_cars():
    """Load cars from JSON file into global cars list"""
    global cars
    try:
        with open('cars.json', 'r') as f:
            cars = json.load(f)
            # Trim spaces and normalize case for all brands/models
            for car in cars:
                car['Brand'] = car.get('Brand', '').strip()
                car['Model'] = car.get('Model', '').strip()
    except FileNotFoundError:
        cars = []

def save_cars_to_file():
    """Save cars back to JSON file"""
    with open('cars.json', 'w') as f:
        json.dump(cars, f, indent=4)

# Initialize cars data on startup
load_cars()

# ---------------- Root Route ----------------
@app.route("/")
def index():
    return render_template('index.html')

# ---------------- Car Details Page ----------------
@app.route("/car.html")
def car_page():
    return render_template('car.html')

# ---------------- API Routes ----------------
@app.route("/api/cars")
def get_cars():
    return jsonify(cars)

@app.route("/api/cars/<id>")
def get_car_by_id(id):
    for car in cars:
        if car['ID'] == id:
            return jsonify(car)
    return jsonify({"error": "Car not found"}), 404

@app.route("/api/cars/save", methods=['POST'])
def save_car():
    new_car = request.get_json()
    car_id = new_car.get('ID')
    
    for i, car in enumerate(cars):
        if car['ID'] == car_id:
            cars[i] = new_car
            save_cars_to_file()
            return jsonify({"message": "Car updated successfully"}), 200 
            
    return jsonify({"error": "Car not found"}), 404

# ---------------- Search Cars ----------------
@app.route("/api/cars/search", methods=['POST'])
def search_cars():
    data = request.get_json()
    term = data.get('term', '').strip().lower()

    filtered_cars = []
    for car in cars:
        brand = car.get('Brand', '').strip().lower()
        model = car.get('Model', '').strip().lower()
        if term in brand or term in model:  # Match partial or full text
            filtered_cars.append(car)
    
    print("Filtered:", filtered_cars)  # debug

    return jsonify(filtered_cars)

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
