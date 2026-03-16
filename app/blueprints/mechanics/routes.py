from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select, func
from app.models import Mechanic, ticket_mechanic, db
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


# CREATE MECHANIC
@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(new_mechanic), 201


# GET ALL MECHANICS
@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics)


# GET MECHANICS ORDERED BY MOST TICKETS WORKED
@mechanics_bp.route("/most-worked", methods=['GET'])
def most_worked_mechanics():
    query = (
        select(Mechanic)
        .outerjoin(ticket_mechanic, Mechanic.id == ticket_mechanic.c.mechanic_id)
        .group_by(Mechanic.id)
        .order_by(func.count(ticket_mechanic.c.ticket_id).desc())
    )
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200


# UPDATE MECHANIC
@mechanics_bp.route("/<int:id>", methods=['PUT'])
def update_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


# DELETE MECHANIC
@mechanics_bp.route("/<int:id>", methods=['DELETE'])
def delete_mechanic(id):
    mechanic = db.session.get(Mechanic, id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic id: {id} successfully deleted"}), 200
