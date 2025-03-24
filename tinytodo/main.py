from flask import Flask, request

app = Flask(__name__)

# let's pretend for now this is the stored data, to keep it simple
tasks = [
        {"id": 1, "title": "buy milk"},
        {"id": 2, "title": "study flask"}
]

@app.get("/tasks")
def get_tasks():
    return tasks

@app.post('/tasks')
def post_tasks():
    # error handling unsupported formats
    try:
        data = request.json
        tasks.append({"id": data['id'], "title": data['title']})
        return f"Task {data} created!"
    except:
        return "format not supported. please send data in the JSON format."

"""
Out of the top of my mind, there are some improvements that this code should have.
Of course this is still a very baby step project, but this is what could be improved:
    1. error handling - instead of using a generic except to catch it all, have specific exceptions.
    2. input sanitization. For now we are using a local array to represent our storage, but in a real API, we will be storing this data in a database! this introduces multiple injection risks.
    3. writing tests
"""
