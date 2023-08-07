

from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector


# Initialize FastAPI app
app = FastAPI()

# Initialize MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="admin123",
  database="school"
)

# Create table for teachers
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS teachers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), subject VARCHAR(255))")

# Create table for students
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS students (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), grade INT)")

# models for CRUD operations
class Teacher(BaseModel):
    name: str
    subject: str

class Student(BaseModel):
    name: str
    grade: int

# API to print "Hello World"
@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

# API for CRUD operations for teachers
@app.get("/teachers")
async def read_teachers():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM teachers")
    result = mycursor.fetchall()
    return {"teachers": result}

@app.post("/teachers")
async def create_teacher(teacher: Teacher):
    mycursor = mydb.cursor()
    sql = "INSERT INTO teachers (name, subject) VALUES (%s, %s)"
    val = (teacher.name, teacher.subject)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Teacher created successfully"}

@app.put("/teachers/{teacher_id}")
async def update_teacher(teacher_id: int, teacher: Teacher):
    mycursor = mydb.cursor()
    sql = "UPDATE teachers SET name = %s, subject = %s WHERE id = %s"
    val = (teacher.name, teacher.subject, teacher_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Teacher updated successfully"}

@app.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: int):
    mycursor = mydb.cursor()
    sql = "DELETE FROM teachers WHERE id = %s"
    val = (teacher_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Teacher deleted successfully"}

# API for CRUD operations for students
@app.get("/students")
async def read_students():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM students")
    result = mycursor.fetchall()
    return {"students": result}

@app.post("/students")
async def create_student(student: Student):
    mycursor = mydb.cursor()
    sql = "INSERT INTO students (name, grade) VALUES (%s, %s)"
    val = (student.name, student.grade)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student created successfully"}

@app.put("/students/{student_id}")
async def update_student(student_id: int, student: Student):
    mycursor = mydb.cursor()
    sql = "UPDATE students SET name = %s, grade = %s WHERE id = %s"
    val = (student.name, student.grade, student_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student updated successfully"}

@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    mycursor = mydb.cursor()
    sql = "DELETE FROM students WHERE id = %s"
    val = (student_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student deleted successfully"}

# API to assign students to a particular teacher
@app.post("/teachers/{teacher_id}/students/{student_id}")
async def assign_student(teacher_id: int, student_id: int):
    mycursor = mydb.cursor()
    sql = "INSERT INTO teachers_students (teacher_id, student_id) VALUES (%s, %s)"
    val = (teacher_id, student_id)
    mycursor.execute(sql, val)
    mydb.commit()
    return {"message": "Student assigned to teacher successfully"}



