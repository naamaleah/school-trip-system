# School Trip Management System

## Overview
This project was developed to assist teachers in managing a school trip for 6th-grade students.

The system allows:
- Managing students and teachers
- Tracking real-time locations
- Displaying locations on a map
- Detecting students who are too far from their teacher
---

## How to Run

### 1. Backend

Open terminal:
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


Server will run on:
http://127.0.0.1:8000


---

### 2. Frontend

Open:

frontend/index.html


(No installation required)

---

## How to Use

### 1. Register Users
- Choose Teacher or Student
- Fill in details
- Click Register

![Register](screenshots/register.png)

---

### 2. Teacher Login
- Enter teacher details
- Click Verify

Only verified teachers can access data


![Login](screenshots/login.png)

---

### 3. Teacher Actions
After login:
- View all teachers
- View all students
- Search by ID
- View students in class
- Detect far students

 
![Actions](screenshots/actions.png)

---

### 4. Update Location
- Select Student / Teacher
- Enter ID
- Enter coordinates (Degrees / Minutes / Seconds)
- Click Update

 
![Location](screenshots/location.png)

---

### 5. Map Visualization
- Students appear on the map
- Colors:
  - Green → regular student
  - Red → far student (>3 km)
  - Blue → teacher


![Map](screenshots/map.png)

---

### 6. Safety Feature
- Click "Far Students"
- System highlights students farther than 3 km

![Far Students](screenshots/far.png)

---

## External Dependencies

### Backend
- FastAPI
- SQLAlchemy
- Uvicorn

Install:

pip install -r requirements.txt


---

### Frontend
- HTML
- CSS
- JavaScript
- Leaflet (map library via CDN)

No installation required

---

### Database
- SQLite
- Created automatically on first run

---



## Info for tutorial:

id="222222222", first_name="Leah", last_name="Levi"

