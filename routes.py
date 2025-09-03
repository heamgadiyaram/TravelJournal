from flask import Blueprint, request, jsonify
import travel_service

travels_bp = Blueprint('travels_bp', __name__, url_prefix="/api")

@travels_bp.route('/travels', methods=['POST'])
def create_travel():
    data = request.json
    try:
        destination = data.get('destination')
        visit_date = data.get('visit_date')
        notes = data.get('notes')
        rating = data.get('rating')

        travel_service.create_travel(destination, visit_date, notes, rating)

    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Travel created successfully."}), 201

@travels_bp.route('/travels', methods=['GET'])
def get_all_travels():
    all_travels = travel_service.get_all_travels()
    return jsonify(all_travels), 200

@travels_bp.route('/travels/<int:travel_id>', methods=['GET'])
def get_travel_by_id(travel_id):
    travel = travel_service.get_travel_by_id(travel_id)
    if not travel:
        return jsonify({"error": "travel id not found"}), 404
    return jsonify(travel), 200

@travels_bp.route('/travels/<int:travel_id>', methods=['DELETE'])
def delete_travel_by_id(travel_id):
    deleted = travel_service.delete_travel_by_id(travel_id)
    if not deleted:
        return jsonify({"error": "travel id not found"}), 404
    
    return jsonify({"message": "travel record deleted"}), 200

@travels_bp.route('/travels/<int:travel_id>', methods=['PUT'])
def update_travel_by_id(travel_id):
    data = request.json

    try:
        updated = travel_service.update_travel_by_id(
            travel_id=travel_id,
            destination=data.get('destination'),
            visit_date=data.get('visit_date'),
            notes=data.get('notes'),
            rating=data.get('rating')
            )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    if not updated:
        return jsonify({"error": "travel id not found"}), 404
    
    return jsonify({"message": "record updated successfully."}), 200
    