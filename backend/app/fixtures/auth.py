from app.models import StudentCreate, TeacherCreate

STUDENT_CREATE_EXAMPLE = StudentCreate(
    email="student@example.com",
    password="123456",
    first_name="Иванов",
    last_name="Иван",
    middle_name="Иванович",
    role="student",
    group="ИКБО-01-20",
    course=3,
)

TEACHER_CREATE_EXAMPLE = TeacherCreate(
    email="teacher@example.com",
    password="123456",
    first_name="Матчин",
    last_name="Василий",
    middle_name="Тимофеевич",
    role="teacher",
    departament="Кафедра тест",
    position="Старший преподаватель",
)
