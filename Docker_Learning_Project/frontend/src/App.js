import React, { useState, useEffect } from "react";
import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    title: "",
    description: "",
  });

  // Fetch todos from backend
  const fetchTodos = async () => {
    try {
      const response = await axios.get(`${API_URL}/todos`);
      setTodos(response.data);
      setError("");
    } catch (err) {
      setError("Failed to fetch todos. Make sure the backend is running.");
      console.error("Error fetching todos:", err);
    } finally {
      setLoading(false);
    }
  };

  // Create new todo
  const createTodo = async (e) => {
    e.preventDefault();
    if (!formData.title.trim()) return;

    try {
      const response = await axios.post(`${API_URL}/todos`, formData);
      setTodos([...todos, response.data]);
      setFormData({ title: "", description: "" });
      setError("");
    } catch (err) {
      setError("Failed to create todo");
      console.error("Error creating todo:", err);
    }
  };

  // Toggle todo completion
  const toggleTodo = async (id, completed) => {
    try {
      const response = await axios.put(`${API_URL}/todos/${id}`, {
        completed: !completed,
      });
      setTodos(todos.map((todo) => (todo.id === id ? response.data : todo)));
      setError("");
    } catch (err) {
      setError("Failed to update todo");
      console.error("Error updating todo:", err);
    }
  };

  // Delete todo
  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API_URL}/todos/${id}`);
      setTodos(todos.filter((todo) => todo.id !== id));
      setError("");
    } catch (err) {
      setError("Failed to delete todo");
      console.error("Error deleting todo:", err);
    }
  };

  // Check backend health
  const checkHealth = async () => {
    try {
      await axios.get(`${API_URL}/health`);
      return true;
    } catch (err) {
      return false;
    }
  };

  useEffect(() => {
    fetchTodos();

    // Check health every 30 seconds
    const healthInterval = setInterval(async () => {
      const isHealthy = await checkHealth();
      if (!isHealthy && !error) {
        setError("Backend connection lost");
      }
    }, 30000);

    return () => clearInterval(healthInterval);
  }, []);

  if (loading) {
    return (
      <div className="app">
        <div className="loading">Loading todos...</div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🐳 Docker Compose Todo App</h1>
        <div className="status">
          ✅ Frontend (React) → Backend (FastAPI) → Database (PostgreSQL)
        </div>
      </header>

      {error && <div className="error">{error}</div>}

      <form className="todo-form" onSubmit={createTodo}>
        <input
          type="text"
          placeholder="Todo title..."
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
        />
        <textarea
          placeholder="Description (optional)..."
          value={formData.description}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
          rows={3}
        />
        <button type="submit">Add Todo</button>
      </form>

      <div className="todo-list">
        {todos.length === 0 ? (
          <div className="loading">No todos yet. Create your first one!</div>
        ) : (
          todos.map((todo) => (
            <div
              key={todo.id}
              className={`todo-item ${todo.completed ? "completed" : ""}`}
            >
              <div className="todo-content">
                <div className="todo-title">{todo.title}</div>
                {todo.description && (
                  <div className="todo-description">{todo.description}</div>
                )}
              </div>
              <div className="todo-actions">
                <button
                  className="btn btn-complete"
                  onClick={() => toggleTodo(todo.id, todo.completed)}
                >
                  {todo.completed ? "↶ Undo" : "✓ Done"}
                </button>
                <button
                  className="btn btn-delete"
                  onClick={() => deleteTodo(todo.id)}
                >
                  🗑 Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
