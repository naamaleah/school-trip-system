from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from math import radians, sin, cos, sqrt, atan2

import models
import schemas
from database import engine, SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_teacher_access(requesting_teacher: schemas.TeacherAccess, db: Session):
    teacher = db.query(models.Teacher).filter(
        models.Teacher.id == requesting_teacher.id,
        models.Teacher.first_name == requesting_teacher.first_name,
        models.Teacher.last_name == requesting_teacher.last_name
    ).first()

    if not teacher:
        raise HTTPException(
            status_code=403,
            detail="Access denied: only registered teachers can access this data"
        )

    return teacher


def dms_to_decimal(degrees: str, minutes: str, seconds: str) -> float:
    return float(degrees) + float(minutes) / 60 + float(seconds) / 3600


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


@app.get("/")
def root():
    return {"message": "Server is running"}

def create_person(db, model, data, exists_message):
    existing = db.query(model).filter(model.id == data.id).first()
    if existing:
        raise HTTPException(status_code=400, detail=exists_message)

    new_item = model(**data.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@app.post("/teachers", response_model=schemas.TeacherResponse)
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    return create_person(db, models.Teacher, teacher, "Teacher with this ID already exists")


@app.post("/students", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return create_person(db, models.Student, student, "Student with this ID already exists")

@app.post("/teacher-access")
def teacher_access(access: schemas.TeacherAccess, db: Session = Depends(get_db)):
    teacher = verify_teacher_access(access, db)

    return {
        "message": "Teacher verified successfully",
        "id": teacher.id,
        "first_name": teacher.first_name,
        "last_name": teacher.last_name,
        "class_name": teacher.class_name
    }


@app.post("/teachers/all", response_model=list[schemas.TeacherResponse])
def get_all_teachers(access: schemas.TeacherAccess, db: Session = Depends(get_db)):
    verify_teacher_access(access, db)
    return db.query(models.Teacher).all()


@app.post("/students/all", response_model=list[schemas.StudentResponse])
def get_all_students(access: schemas.TeacherAccess, db: Session = Depends(get_db)):
    verify_teacher_access(access, db)
    return db.query(models.Student).all()


@app.post("/teachers/find", response_model=schemas.TeacherResponse)
def get_teacher(request: schemas.FindTeacherRequest, db: Session = Depends(get_db)):
    verify_teacher_access(request.requesting_teacher, db)

    teacher = db.query(models.Teacher).filter(models.Teacher.id == request.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@app.post("/students/find", response_model=schemas.StudentResponse)
def get_student(request: schemas.FindStudentRequest, db: Session = Depends(get_db)):
    verify_teacher_access(request.requesting_teacher, db)

    student = db.query(models.Student).filter(models.Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.post("/teachers/students", response_model=list[schemas.StudentResponse])
def get_students_by_teacher_class(
    request: schemas.TeacherStudentsRequest,
    db: Session = Depends(get_db)
):
    verify_teacher_access(request.requesting_teacher, db)

    teacher = db.query(models.Teacher).filter(models.Teacher.id == request.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return db.query(models.Student).filter(
        models.Student.class_name == teacher.class_name
    ).all()


def save_location(
    db: Session,
    location,
    person_model,
    location_model,
    id_field_name: str,
    response_id_name: str
):
    person = db.query(person_model).filter(person_model.id == location.ID).first()

    if not person:
        raise HTTPException(status_code=404, detail="Person not found")

    longitude = dms_to_decimal(
        location.Coordinates.Longitude.Degrees,
        location.Coordinates.Longitude.Minutes,
        location.Coordinates.Longitude.Seconds
    )

    latitude = dms_to_decimal(
        location.Coordinates.Latitude.Degrees,
        location.Coordinates.Latitude.Minutes,
        location.Coordinates.Latitude.Seconds
    )

    id_column = getattr(location_model, id_field_name)

    existing_location = db.query(location_model).filter(
        id_column == location.ID
    ).first()

    if existing_location:
        existing_location.latitude = latitude
        existing_location.longitude = longitude
        existing_location.timestamp = location.Time
        db.commit()
        db.refresh(existing_location)
        return existing_location

    new_location = location_model(
        **{
            response_id_name: location.ID,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": location.Time
        }
    )

    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location

@app.post("/locations/student", response_model=schemas.StudentLocationResponse)
def update_student_location(location: schemas.StudentLocationCreate, db: Session = Depends(get_db)):
    return save_location(
        db=db,
        location=location,
        person_model=models.Student,
        location_model=models.StudentLocation,
        id_field_name="student_id",
        response_id_name="student_id"
    )


@app.post("/locations/teacher", response_model=schemas.TeacherLocationResponse)
def update_teacher_location(location: schemas.TeacherLocationCreate, db: Session = Depends(get_db)):
    return save_location(
        db=db,
        location=location,
        person_model=models.Teacher,
        location_model=models.TeacherLocation,
        id_field_name="teacher_id",
        response_id_name="teacher_id"
    )

@app.get("/locations/students", response_model=list[schemas.StudentLocationResponse])
def get_all_student_locations(db: Session = Depends(get_db)):
    return db.query(models.StudentLocation).all()


@app.post("/teachers/far-students", response_model=list[schemas.FarStudentResponse])
def get_far_students(
    request: schemas.FarStudentsRequest,
    db: Session = Depends(get_db)
):
    verify_teacher_access(request.requesting_teacher, db)

    teacher = db.query(models.Teacher).filter(models.Teacher.id == request.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    teacher_location = db.query(models.TeacherLocation).filter(
        models.TeacherLocation.teacher_id == request.teacher_id
    ).first()

    if not teacher_location:
        raise HTTPException(status_code=404, detail="Teacher location not found")

    students = db.query(models.Student).filter(
        models.Student.class_name == teacher.class_name
    ).all()

    far_students = []

    for student in students:
        student_location = db.query(models.StudentLocation).filter(
            models.StudentLocation.student_id == student.id
        ).first()

        if not student_location:
            continue

        distance = haversine_distance(
            teacher_location.latitude,
            teacher_location.longitude,
            student_location.latitude,
            student_location.longitude
        )

        if distance > 3:
            far_students.append({
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "class_name": student.class_name,
                "distance_km": round(distance, 2)
            })

    return far_students


@app.post("/locations/teacher/current", response_model=schemas.TeacherLocationResponse)
def get_teacher_current_location(
    request: schemas.TeacherLocationRequest,
    db: Session = Depends(get_db)
):
    verify_teacher_access(request.requesting_teacher, db)

    teacher_location = db.query(models.TeacherLocation).filter(
        models.TeacherLocation.teacher_id == request.teacher_id
    ).first()

    if not teacher_location:
        raise HTTPException(status_code=404, detail="Teacher location not found")

    return teacher_location
