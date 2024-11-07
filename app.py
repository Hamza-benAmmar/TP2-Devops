from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
users = []

@app.route("/")
def home():
    return "Welcome to the Task Management API!"

@app.route("/tasks", methods=["POST"])
def create_task():
    task_data = request.json
    if not task_data or "title" not in task_data:
        return jsonify({"error": "Task title is required!"}), 400
    
    task_id = len(tasks) + 1
    task = {"id": task_id, "title": task_data["title"], "completed": False}
    tasks.append(task)
    return jsonify(task), 201

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    try:
        task = next((task for task in tasks if task["id"] == task_id), None)
        if task is None:
            return jsonify({"error": "Task not found!"}), 404

        task["completed"] = request.json.get("completed", task["completed"])
        return jsonify(task), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

@app.route("/users", methods=["POST"])
def register_user():
    user_data = request.json
    if "username" not in user_data:
        return jsonify({"error": "Username is required!"}), 400
    
    user_id = len(users) + 1
    user = {"id": user_id, "username": user_data["username"]}
    users.append(user)
    return jsonify(user), 201

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
