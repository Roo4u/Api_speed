# .\venv\scripts\activate
#python -m flask run

from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]


data = {
    "ID": [1, 2, 3, 4],
    "Name": ["Alice", "Bob", "Charlie", "David"],
    "Age": [25, 30, 35, 40],
    "City": ["New York", "Los Angeles", "Chicago", "Houston"]
}
integercolumnlist = ["ID", "Age"]
df = pd.DataFrame(data)

def split_string(text):
    separator = "/"
    result = str.split(text, separator)
    return result

@app.route("/")
def home():

    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route('/query')
def sec():

    query_params = request.args.to_dict()
    print(query_params)
    # Initialize the DataFrame with all rows
    filtered_df = df.copy()
    print(filtered_df)

    # Iterate through query parameters and filter the DataFrame
    print(query_params.items())
    query = filtered_df
    for key, value in query_params.items():
        print(key)
        print(value)
        if key in integercolumnlist:
            query = query[query[str(key)] == int(value)]
        else:
            query = query[query[str(key)] == value]
        print(query)
    """
    filtered_df = filtered_df.loc[(filtered_df[list(query_params)] == pd.Series(query_params)).all(axis=1)]
    """
    # Convert the filtered DataFrame to a list of dictionaries
    result = query.to_dict(orient='records')
    print(result)
    print("here")

    return jsonify(result)



@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    new_task = {"id": len(tasks) + 1, "title": data["title"], "completed": False}
    tasks.append(new_task)
    return jsonify({"message": "Task created", "task": new_task}), 201

# Endpoint to update an existing task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    task['title'] = data.get('title', task['title'])
    task['completed'] = data.get('completed', task['completed'])
    return jsonify({"message": "Task updated", "task": task})

# Endpoint to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    tasks.remove(task)
    return jsonify({"message": "Task deleted"})

"""
if __name__ == '__main__':
    app.run(debug=True)
"""


"""
if __name__=='__main__':
    app.run()
    """
    
if __name__=='__main__':
    from waitress import serve
    if os.getenv("EAR_PRODUCTION")  == None:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        app.run(host="0.0.0.0", port=5000, load_dotenv=True)
    else:
        serve(app, host="0.0.0.0", port=5000)