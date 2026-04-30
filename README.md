# School Trip Management System

## Overview
This project was developed to assist teachers in managing a school trip for 6th-grade students.

The system allows:
- Managing students and teachers
- Tracking real-time locations
- Displaying locations on a map
- Detecting students who are too far from their teacher

---

## Project Structure

project/
|
|---backend/ # FastAPI server
|
|---frontend/ # UI (HTML, CSS, JavaScript)
|
|---README.md
|
|---screenshots
|
|---.gitignore


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

📸 Screenshot:  
![Register](screenshots/register.png)

---

### 2. Teacher Login
- Enter teacher details
- Click Verify

Only verified teachers can access data

📸 Screenshot:  
![Login](screenshots/login.png)

---

### 3. Teacher Actions
After login:
- View all teachers
- View all students
- Search by ID
- View students in class
- Detect far students

📸 Screenshot:  
![Actions](screenshots/actions.png)

---

### 4. Update Location
- Select Student / Teacher
- Enter ID
- Enter coordinates (Degrees / Minutes / Seconds)
- Click Update

📸 Screenshot:  
![Location](screenshots/location.png)

---

### 5. Map Visualization
- Students appear on the map
- Colors:
  - Green → regular student
  - Red → far student (>3 km)
  - Blue → teacher

📸 Screenshot:  
![Map](screenshots/map.png)

---

### 6. Safety Feature
- Click "Far Students"
- System highlights students farther than 3 km

📸 Screenshot:  
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

## Notes

- Only teachers can access system data after verification
- Each location update overwrites the previous one
- Distance is calculated using the Haversine formula
- The system focuses on clarity and functionality

---

## Summary

This project demonstrates:
- Client-server architecture
- REST API development
- Database integration
- Real-time data handling
- Map-based visualization
- Basic geospatial calculations