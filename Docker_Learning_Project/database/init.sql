-- Initialize the Todo database with sample data

CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample todo items
INSERT INTO todos (title, description, completed) VALUES 
    ('Learn Docker Compose', 'Complete the Docker Compose tutorial with React, FastAPI, and PostgreSQL', false),
    ('Setup Database Connection', 'Configure PostgreSQL connection with FastAPI backend', true),
    ('Create Frontend Components', 'Build React components for todo list functionality', false),
    ('Implement API Endpoints', 'Create CRUD endpoints for todo operations', false),
    ('Test Container Communication', 'Verify that all containers can communicate properly', false);

-- Create an updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_todos_updated_at 
    BEFORE UPDATE ON todos 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();
