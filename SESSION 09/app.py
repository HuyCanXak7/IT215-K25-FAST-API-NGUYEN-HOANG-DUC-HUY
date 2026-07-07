from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(title="Team Task Manager API")

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

def get_timestamp():
    return datetime.now(timezone.utc).isoformat()


def build_response(
    status_code: int,
    message: str,
    data,
    error,
    path: str
):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": get_timestamp(),
        "path": path
    }


class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)

    @field_validator("title", "description", "assignee")
    @classmethod
    def remove_space(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(...)

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value = value.strip().lower()

        allow = [
            "todo",
            "in_progress",
            "done"
        ]

        if value not in allow:
            raise ValueError(
                "Status must be todo, in_progress or done"
            )

        return value


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content=build_response(
            422,
            "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
            None,
            "ERR-VAL-422: Validation error at Request Body fields constraint layout.",
            request.url.path
        )
    )


@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content=build_response(
            500,
            "Lỗi hệ thống nội bộ!",
            None,
            "ERR-500: Internal Server Error.",
            request.url.path
        )
    )


def calculate_team_metrics():

    total_tasks = len(tasks_db)

    completed_tasks = sum(
        1
        for task in tasks_db
        if task["status"] == "done"
    )

    if total_tasks == 0:
        completion_rate = 0

    else:
        completion_rate = round(
            completed_tasks / total_tasks * 100,
            2
        )

    return (
        total_tasks,
        completed_tasks,
        completion_rate
    )
    
@app.get("/tasks", status_code=status.HTTP_200_OK)
async def get_all_tasks(
    request: Request,
    status: Optional[str] = None
):

    if status:
        data = [
            task
            for task in tasks_db
            if task["status"] == status.lower()
        ]
    else:
        data = tasks_db

    return build_response(
        200,
        "Lấy danh sách công việc thành công!",
        data,
        None,
        request.url.path
    )


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(
    request: Request,
    task_in: TaskCreateSchema
):

    for task in tasks_db:
        if task["title"].lower() == task_in.title.lower():
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                    "error": "ERR-TASK-01: Task conflict: Title field duplicates an existing record."
                }
            )

    new_id = (
        max(task["id"] for task in tasks_db) + 1
        if tasks_db
        else 1
    )

    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": get_timestamp()
    }

    tasks_db.append(new_task)

    return build_response(
        201,
        "Khởi tạo công việc mới thành công!",
        new_task,
        None,
        request.url.path
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    detail = exc.detail

    if isinstance(detail, dict):
        message = detail.get("message", "Lỗi")
        error = detail.get("error", "Unknown Error")
    else:
        message = str(detail)
        error = None

    return JSONResponse(
        status_code=exc.status_code,
        content=build_response(
            exc.status_code,
            message,
            None,
            error,
            request.url.path
        )
    )
@app.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def update_task_status(
    task_id: int,
    status_in: TaskStatusUpdateSchema,
    request: Request
):

    for task in tasks_db:

        if task["id"] == task_id:

            if task["status"] == "done":
                raise HTTPException(
                    status_code=400,
                    detail={
                        "message": "Lỗi: Công việc đã hoàn thành, không thể cập nhật!",
                        "error": "ERR-TASK-04: Task already completed."
                    }
                )

            task["status"] = status_in.status

            return build_response(
                200,
                "Cập nhật tiến độ công việc thành công!",
                task,
                None,
                request.url.path
            )

    raise HTTPException(
        status_code=404,
        detail={
            "message": "Lỗi: Không tìm thấy công việc!",
            "error": "ERR-TASK-03: Task not found."
        }
    )


@app.get(
    "/tasks/analytics/dashboard",
    status_code=status.HTTP_200_OK
)
async def get_dashboard_analytics(request: Request):

    total_tasks, completed_tasks, completion_rate = calculate_team_metrics()

    data = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate_percentage": completion_rate
    }

    return build_response(
        200,
        "Lấy số liệu thống kê hiệu suất nhóm thành công!",
        data,
        None,
        request.url.path
    )