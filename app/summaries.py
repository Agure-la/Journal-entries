from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app
from app.models import JournalEntry
from sqlalchemy import func

@app.route('/summary/daily', methods=['GET'])
@jwt_required()
def daily_summary():
    current_user = get_jwt_identity()
    summary = JournalEntry.query \
    .filter_by(user_id=current_user.id) \
    .group_by(JournalEntry.date) \
    .with_entries(JournalEntry.date, func.count(JournalEntry.id).label('count')) \
    .all()

    return jsonify(summary), 200