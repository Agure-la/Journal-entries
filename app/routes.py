from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from app.models import JournalEntry

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/entries', methods=['POST'])
@jwt_required()
def create_entry():
    data = request.get_son()
    current_user = get_jwt_identity()

    new_entry = JournalEntry(
        title = data['title'],
        content=data['content'],
        category=data['category'],
        date=data['date'],
        user_id=current_user.id
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(message='Journal entry created'), 201

@app.route('/entries/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_entry(entry_id):
    entry = JournalEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify(message='Journal entry deleted'), 200

@app.route('/entries/<int:entry_id>', methods=['PUT'])
@jwt_required()
def edit_entry(entry_id):
    data = request.get_json()
    current_user = get_jwt_identity()

    entry = JournalEntry.query.filter_by(id=entry_id, user_id=current_user.id).first()
    if not entry:
        return jsonify({"msg": "Entry not found for this Id"})

    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.category = data.get('category', entry.category)
    entry.date = data.get('date', entry.date)

    db.session.commit()

    return jsonify({
        "message": "Journal entry updated successfully",
        "entry": {
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "category": entry.category,
            "date": entry.date.strftime('%Y-%m-%d')
        }
    }), 200

@app.route('/entries', methods=['GET'])
@jwt_required()
def get_entries():
    current_user = get_jwt_identity()
    entries = JournalEntry.query.filter_by(user_id=current_user.id).all()

    entries_list = []
    for entry in entries:
        entries_list.append({
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "category": entry.category,
            "date": entry.date.strftime('%Y-%m-%d')
        })

    return jsonify(entries_list), 200

@app.route('/entries/category/<string:category>', methods=['GET'])
@jwt_required()
def get_entries_by_category(category):
    current_user = get_jwt_identity()
    entries = JournalEntry.query.filter_by(user_id=current_user.id, category=category).all()

    entries_list = []
    for entry in entries:
        entries_list.append({
            "id": entry.id,
            "title": entry.title,
            "content": entry.content,
            "category": entry.category,
            "date": entry.date.strftime('%Y-%m=%d')
        })

    return jsonify(entries_list), 200
