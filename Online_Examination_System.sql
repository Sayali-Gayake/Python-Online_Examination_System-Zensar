CREATE DATABASE online_exam;

USE online_exam;

CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE Exams (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    subject VARCHAR(100),
    exam_date DATE
);

CREATE TABLE Questions (
    question_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_id INT,
    question_text TEXT,
    marks INT,
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
);

CREATE TABLE Results (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    exam_id INT,
    total_marks INT,
    grade CHAR(2),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (exam_id) REFERENCES Exams(exam_id)
);

CREATE TABLE Notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    message TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id)
);

USE online_exam;

-- Insert sample data into Students table
INSERT INTO Students (name, email) VALUES 
('Arjun Sharma', 'arjun.sharma@example.com'),
('Sneha Patel', 'sneha.patel@example.com'),
('Rohan Gupta', 'rohan.gupta@example.com'),
('Priya Iyer', 'priya.iyer@example.com');

-- Insert sample data into Exams table
INSERT INTO Exams (subject, exam_date) VALUES 
('Mathematics', '2025-01-15'),
('Physics', '2025-01-20'),
('Chemistry', '2025-01-25'),
('Biology', '2025-01-30');

-- Insert sample data into Questions table
INSERT INTO Questions (exam_id, question_text, marks) VALUES 
(1, 'What is the square root of 144?', 5),
(1, 'Solve for x: 3x + 5 = 20.', 10),
(2, 'Explain the laws of motion.', 15),
(3, 'What is the molecular weight of water?', 5),
(4, 'Describe the structure of DNA.', 10);

-- Insert sample data into Results table
INSERT INTO Results (student_id, exam_id, total_marks, grade) VALUES 
(1, 1, 15, 'A'),
(2, 1, 12, 'B'),
(3, 2, 10, 'C'),
(4, 3, 20, 'A'),
(1, 4, 18, 'A');

-- Insert sample data into Notifications table
INSERT INTO Notifications (student_id, message) VALUES 
(1, 'Your Mathematics exam marks have been updated.'),
(2, 'Your Mathematics exam marks have been updated.'),
(3, 'Your Physics exam marks have been updated.'),
(4, 'Your Chemistry exam marks have been updated.'),
(1, 'Your Biology exam marks have been updated.');
