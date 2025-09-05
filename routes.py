from flask import Blueprint, request, jsonify
import travel_service
from config import Config
import requests

travels_bp = Blueprint('travels_bp', __name__)

@travels_bp.route('/create', methods=['POST'])
def create_travel():
    data = request.json
    try:
        destination = data.get('destination')
        visit_date = data.get('visit_date')
        country = data.get('country')
        notes = data.get('notes')
        rating = data.get('rating')

        travel_service.create_travel(destination, visit_date, country, notes, rating)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Travel created successfully."}), 201

@travels_bp.route('/get-all-records', methods=['GET'])
def get_all_travels():
    all_travels = travel_service.get_all_travels()
    return jsonify(all_travels), 200

@travels_bp.route('/get-record/<int:travel_id>', methods=['GET'])
def get_travel_by_id(travel_id):
    travel = travel_service.get_travel_by_id(travel_id)
    if not travel:
        return jsonify({"error": "travel id not found"}), 404
    return jsonify(travel), 200

@travels_bp.route('/delete-record/<int:travel_id>', methods=['DELETE'])
def delete_travel_by_id(travel_id):
    deleted = travel_service.delete_travel_by_id(travel_id)
    if not deleted:
        return jsonify({"error": "travel id not found"}), 404
    
    return jsonify({"message": "travel record deleted"}), 200

@travels_bp.route('/update-record/<int:travel_id>', methods=['PUT'])
def update_travel_by_id(travel_id):
    data = request.json

    try:
        updated = travel_service.update_travel_by_id(
            travel_id=travel_id,
            destination=data.get('destination'),
            visit_date=data.get('visit_date'),
            country = data.get('country'),
            notes=data.get('notes'),
            rating=data.get('rating')
            )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    if not updated:
        return jsonify({"error": "travel id not found"}), 404
    
    return jsonify({"message": "record updated successfully."}), 200

@travels_bp.route('/entry/<int:travel_id>/photo', methods=['GET'])
def create_photo(travel_id):
    travel = travel_service.get_travel_by_id(travel_id)
    if not travel:
        return jsonify({"error": "travel id not found"})
    destination = travel.get('destination')

    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": destination,
        "client_id": Config.UNSPLASH_ACCESS_KEY,
        "per_page": 1
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return jsonify({"error": "could not find image for destination"})
    
    data = response.json()
    if not data['results']:
        return jsonify({"message": "No image found for this destination"}), 404

    image_url = data['results'][0]['urls']['regular']

    return jsonify({
        "destination": destination,
        "image_url": image_url,
    }), 200

@travels_bp.route('/stats/average-ratings', methods=['GET'])
def average_ratings_by_country():
    stats = travel_service.get_average_ratings_by_country()
    return jsonify(stats), 200


    