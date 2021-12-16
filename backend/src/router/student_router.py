from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from model.student import StudentModel, UpdateStudentModel

router = APIRouter()


@router.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(request: Request, student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    new_student = await request.app.db["students"].insert_one(student)
    created_student = await request.app.db["students"].find_one(
        {"_id": new_student.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)


@router.get(
    "/", response_description="List all students", response_model=list[StudentModel]
)
async def list_students(request: Request):
    students = await request.app.db["students"].find().to_list(1000)
    return students


@router.get(
    "/{id}", response_description="Get a single student", response_model=StudentModel
)
async def show_student(request: Request, id: str):
    if (student := await request.app.db["students"].find_one({"_id": id})) is not None:
        return student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")


@router.get(
    "/email/{email}",
    response_description="Get a single student",
    response_model=StudentModel,
)
async def show_student_by_email(request: Request, email: str):
    if (
        student := await request.app.db["students"].find_one({"email": email})
    ) is not None:
        return student
    raise HTTPException(status_code=404, detail=f"Student {email} not found")


@router.put(
    "/{id}", response_description="Update a student", response_model=StudentModel
)
async def update_student(
    request: Request, id: str, student: UpdateStudentModel = Body(...)
):
    student = {k: v for k, v in student.dict().items() if v is not None}
    if student:
        update_result = await request.app.db["students"].update_one(
            {"_id": id}, {"$set": student}
        )
        if (
            update_result.modified_count == 1
            and (
                updated_student := await request.app.db["students"].find_one(
                    {"_id": id}
                )
            )
            is not None
        ):
            return updated_student
    if (
        existing_student := await request.app.db["students"].find_one({"_id": id})
    ) is not None:
        return existing_student
    raise HTTPException(status_code=404, detail=f"Student {id} not found")
