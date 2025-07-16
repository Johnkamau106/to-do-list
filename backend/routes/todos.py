from flask import Blueprint, request, jsonify
from models import Todo, db
from flask_jwt_extended import jwt_required, get_jwt_identity

todos_bp = Blueprint('todos', __name__)

@todos_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    current_user_id = get_jwt_identity()
    todos = Todo.query.filter_by(user_id=current_user_id).all()
    return jsonify([
        {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'due_date': todo.due_date.isoformat() if todo.due_date else None,
            'priority': todo.priority,
            'completed': todo.completed
        } for todo in todos
    ])

@todos_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    
    new_todo = Todo(
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        user_id=current_user_id
    )
    
    db.session.add(new_todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo created successfully'}), 201

@todos_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    current_user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first_or_404()
    
    return jsonify({
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'due_date': todo.due_date.isoformat() if todo.due_date else None,
        'priority': todo.priority,
        'completed': todo.completed
    })

@todos_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first_or_404()
    
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.due_date = data.get('due_date', todo.due_date)
    todo.priority = data.get('priority', todo.priority)
    todo.completed = data.get('completed', todo.completed)
    
    db.session.commit()
    
    return jsonify({'message': 'Todo updated successfully'})

@todos_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    current_user_id = get_jwt_identity()
    todo = Todo.query.filter_by(id=todo_id, user_id=current_user_id).first_or_404()
    
    db.session.delete(todo)
    db.session.commit()
    
    return jsonify({'message': 'Todo deleted successfully'})