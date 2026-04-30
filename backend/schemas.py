from pydantic import BaseModel, field_validator


class TeacherCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    class_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value):
       return validate_9_digit_id(value)


class TeacherResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    class_name: str

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    id: str
    first_name: str
    last_name: str
    class_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value):
        return validate_9_digit_id(value)


class StudentResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    class_name: str

    class Config:
        from_attributes = True


class TeacherAccess(BaseModel):
    id: str
    first_name: str
    last_name: str

    @field_validator("id")
    @classmethod
    def validate_id(cls, value):
        return validate_9_digit_id(value)


class FindTeacherRequest(BaseModel):
    requesting_teacher: TeacherAccess
    teacher_id: str


class FindStudentRequest(BaseModel):
    requesting_teacher: TeacherAccess
    student_id: str


class TeacherStudentsRequest(BaseModel):
    requesting_teacher: TeacherAccess
    teacher_id: str


class FarStudentsRequest(BaseModel):
    requesting_teacher: TeacherAccess
    teacher_id: str


class CoordinatePart(BaseModel):
    Degrees: str
    Minutes: str
    Seconds: str


class Coordinates(BaseModel):
    Longitude: CoordinatePart
    Latitude: CoordinatePart


class StudentLocationCreate(BaseModel):
    ID: str
    Coordinates: Coordinates
    Time: str

    @field_validator("ID")
    @classmethod
    def validate_id(cls, value):
        return validate_9_digit_id(value)


class StudentLocationResponse(BaseModel):
    student_id: str
    latitude: float
    longitude: float
    timestamp: str

    class Config:
        from_attributes = True


class TeacherLocationCreate(BaseModel):
    ID: str
    Coordinates: Coordinates
    Time: str

    @field_validator("ID")
    @classmethod
    def validate_id(cls, value):
        return validate_9_digit_id(value)


class TeacherLocationResponse(BaseModel):
    teacher_id: str
    latitude: float
    longitude: float
    timestamp: str

    class Config:
        from_attributes = True


class FarStudentResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    class_name: str
    distance_km: float


class TeacherLocationRequest(BaseModel):
    requesting_teacher: TeacherAccess
    teacher_id: str


def validate_9_digit_id(value):
    if not value.isdigit() or len(value) != 9:
        raise ValueError("ID must contain exactly 9 digits")
    return value