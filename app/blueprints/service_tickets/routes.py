from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Ticket, Mechanic, Inventory, db
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema


# CREATE SERVICE TICKET
@service_tickets_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket = Ticket(**ticket_data)
    db.session.add(new_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_ticket), 201


# GET ALL SERVICE TICKETS
@service_tickets_bp.route("/", methods=['GET'])
def get_service_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets)


# ASSIGN MECHANIC TO SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic is already assigned to this ticket"}), 400

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# REMOVE MECHANIC FROM SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404

    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket"}), 400

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# EDIT MECHANICS ON A TICKET (bulk add/remove)
@service_tickets_bp.route("/<int:ticket_id>/edit", methods=['PUT'])
def edit_ticket_mechanics(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404

    data = request.json or {}
    add_ids = data.get('add_ids', [])
    remove_ids = data.get('remove_ids', [])

    for mechanic_id in add_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)

    for mechanic_id in remove_ids:
        mechanic = db.session.get(Mechanic, mechanic_id)
        if mechanic and mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)

    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200


# ADD PART TO SERVICE TICKET
@service_tickets_bp.route("/<int:ticket_id>/add-part/<int:part_id>", methods=['PUT'])
def add_part_to_ticket(ticket_id, part_id):
    ticket = db.session.get(Ticket, ticket_id)
    part = db.session.get(Inventory, part_id)

    if not ticket:
        return jsonify({"error": "Service ticket not found"}), 404
    if not part:
        return jsonify({"error": "Part not found"}), 404

    if part in ticket.parts:
        return jsonify({"message": "Part is already added to this ticket"}), 400

    ticket.parts.append(part)
    db.session.commit()
    return service_ticket_schema.jsonify(ticket), 200
