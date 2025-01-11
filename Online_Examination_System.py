import http.server
import socketserver
import json
import mysql.connector

# RESTful API Handler
class OnlineExamHandler(http.server.BaseHTTPRequestHandler):

    def _connect_db(self):
        return mysql.connector.connect(
            host="localhost",   # Replace with your MySQL host
            user="root",        # Replace with your MySQL username
            password="root", # Replace with your MySQL password
            database="online_exam" # Replace with your MySQL database name
        )

    def _send_response(self, response_data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_GET(self):
        try:
            if self.path.startswith('/students'):
                self.handle_get_students()
            elif self.path.startswith('/exams'):
                self.handle_get_exams()
            elif self.path.startswith('/results'):
                self.handle_get_results()
            else:
                self._send_response({'error': 'Invalid endpoint'}, status_code=404)
        except Exception as e:
            self._send_response({'error': str(e)}, status_code=500)

    def handle_get_students(self):
        connection = self._connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Students')
        students = cursor.fetchall()
        response = [{'student_id': s[0], 'name': s[1], 'email': s[2]} for s in students]
        connection.close()
        self._send_response(response)

    def handle_get_exams(self):
        connection = self._connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Exams')
        exams = cursor.fetchall()
        response = [{'exam_id': e[0], 'subject': e[1], 'exam_date': str(e[2])} for e in exams]
        connection.close()
        self._send_response(response)

    def handle_get_results(self):
        connection = self._connect_db()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Results')
        results = cursor.fetchall()
        response = [{'result_id': r[0], 'student_id': r[1], 'exam_id': r[2], 'total_marks': r[3], 'grade': r[4]} for r in results]
        connection.close()
        self._send_response(response)

    def do_POST(self):
        try:
            if self.path.startswith('/students'):
                self.handle_post_students()
            elif self.path.startswith('/results'):
                self.handle_post_results()
            elif self.path.startswith('/exams'):
                self.handle_post_exams()
            else:
                self._send_response({'error': 'Invalid endpoint'}, status_code=404)
        except Exception as e:
            self._send_response({'error': str(e)}, status_code=500)

    def handle_post_students(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        connection = self._connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO Students (name, email) VALUES (%s, %s)', 
                           (post_data['name'], post_data['email']))
            connection.commit()
            self._send_response({'message': 'Student added successfully'}, status_code=201)
        except mysql.connector.Error as e:
            self._send_response({'error': str(e)}, status_code=400)
        finally:
            connection.close()

    def handle_post_exams(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        connection = self._connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO Exams (subject, exam_date) VALUES (%s, %s)', 
                           (post_data['subject'], post_data['exam_date']))
            connection.commit()
            self._send_response({'message': 'Exam added successfully'}, status_code=201)
        except mysql.connector.Error as e:
            self._send_response({'error': str(e)}, status_code=400)
        finally:
            connection.close()

    def handle_post_results(self):
        content_length = int(self.headers['Content-Length'])
        post_data = json.loads(self.rfile.read(content_length))
        connection = self._connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO Results (student_id, exam_id, total_marks, grade) VALUES (%s, %s, %s, %s)', 
                           (post_data['student_id'], post_data['exam_id'], post_data['total_marks'], post_data['grade']))
            connection.commit()
            self._send_response({'message': 'Result added successfully'}, status_code=201)
        except mysql.connector.Error as e:
            self._send_response({'error': str(e)}, status_code=400)
        finally:
            connection.close()

    def do_DELETE(self):
        try:
            if self.path.startswith('/students/'):
                self.handle_delete_student()
            elif self.path.startswith('/results/'):
                self.handle_delete_result()
            elif self.path.startswith('/exams/'):
                self.handle_delete_exam()
            else:
                self._send_response({'error': 'Invalid endpoint'}, status_code=404)
        except Exception as e:
            self._send_response({'error': str(e)}, status_code=500)

    def handle_delete_student(self):
        student_id = self.path.split('/')[-1]
        connection = self._connect_db()
        cursor = connection.cursor()
        try:
            cursor.execute('DELETE FROM Students WHERE student_id = %s', (student_id,))
            connection.commit()
            self._send_response({'message': 'Student deleted successfully'})
        except mysql.connector.Error as e:
            self._send_response({'error': str(e)}, status_code=400)
        finally:
            connection.close()

    # Implement similar DELETE handlers for Results and Exams...

# Main execution
if __name__ == '__main__':
    PORT = 8000
    with socketserver.TCPServer(('', PORT), OnlineExamHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()
