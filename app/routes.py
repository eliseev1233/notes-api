from flask import Blueprint, request, jsonify
from .models import db, User, Note

bp = Blueprint('api', __name__)

# --- Пользователи ---
@bp.post('/users')
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('email'):
        return jsonify({'error': 'Invalid input'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409

    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# --- Заметки (с фильтрацией и пагинацией) ---
@bp.get('/notes')
def get_notes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    category = request.args.get('category', type=str)
    user_id = request.args.get('user_id', type=int)

    query = Note.query
    if category:
        query = query.filter_by(category=category)
    if user_id:
        query = query.filter_by(user_id=user_id)

    pagination = query.order_by(Note.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'notes': [note.to_dict() for note in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

@bp.post('/notes')
def create_note():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('content') or not data.get('user_id'):
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    note = Note(
        title=data['title'],
        content=data['content'],
        category=data.get('category', 'general'),
        user_id=data['user_id']
    )
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@bp.get('/notes/<int:note_id>')
def get_note(note_id):
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@bp.put('/notes/<int:note_id>')
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    data = request.get_json()
    
    note.title = data.get('title', note.title)
    note.content = data.get('content', note.content)
    note.category = data.get('category', note.category)
    
    db.session.commit()
    return jsonify(note.to_dict())

@bp.delete('/notes/<int:note_id>')
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})
