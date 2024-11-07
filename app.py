from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
users = []

@app.route("/")
def home():
    return "Welcome to the Task Management API!"

# BUG: Unrestricted route allows any data, no validation on "description" or other attributes
@app.route("/tasks", methods=["POST"])
def create_task():
    task_data = request.json
    if not task_data or "title" not in task_data:
        return jsonify({"error": "Task title is required!"}), 400
    
    # SECURITY VULNERABILITY: Task IDs are predictable and can lead to IDOR attacks
    task_id = len(tasks) + 1  
    task = {
        "id": task_id,
        "title": task_data["title"],
        "completed": False,
        "description": task_data.get("description")  # SMELL: Description may be None and needs validation
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        # BUG: No check if `task_id` is valid; may lead to KeyError if not in tasks
        task = next((task for task in tasks if task["id"] == task_id), None)
        if task is None:
            return jsonify({"error": "Task not found!"}), 404

        # SECURITY VULNERABILITY: Unrestricted data update (e.g., adding unknown fields)
        task.update(request.json)  # SMELL: Not checking fields that can be updated
        return jsonify(task), 200
    except Exception as e:
        # SMELL: Catching all exceptions may hide actual errors
        return jsonify({"error": str(e)}), 500

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    # BUG: Deletes task without confirmation, and it can break ID consistency
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

# BUG: No input validation, allowing creation of duplicate usernames or empty strings
@app.route("/users", methods=["POST"])
def register_user():
    user_data = request.json
    if "username" not in user_data:
        return jsonify({"error": "Username is required!"}), 400

    # SECURITY VULNERABILITY: Duplicate usernames allowed, could allow user enumeration
    user_id = len(users) + 1
    user = {"id": user_id, "username": user_data["username"]}
    users.append(user)
    return jsonify(user), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users}), 200

if __name__ == "__main__":
    # SECURITY VULNERABILITY: Debug mode reveals sensitive information, avoid in production
    app.run(host="0.0.0.0", port=5000, debug=True)
