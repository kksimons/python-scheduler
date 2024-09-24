from fastapi import FastAPI
from pydantic import BaseModel
from scripts.scheduler import create_shift_scheduling_model, solve_shift_scheduling
import uvicorn

app = FastAPI()

# python -m uvicorn main:app --reload   
# Define the Pydantic model to accept the input JSON
class ShiftScheduleInput(BaseModel):
    num_employees: int
    shifts_per_day: int
    total_days: int
    employee_types: list[str]  # List of employee types ('full_time' or 'part_time')

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Employee Shift Scheduler is up!"}

# Scheduler endpoint
@app.post("/api/v1/scheduler")
def scheduler(data: ShiftScheduleInput):
    # Create the model based on the input data
    model, shifts = create_shift_scheduling_model(
        data.num_employees,
        data.shifts_per_day,
        data.total_days,
        data.employee_types
    )

    # Solve the model and return the results
    results = solve_shift_scheduling(
        model, shifts, data.num_employees, data.shifts_per_day, data.total_days
    )
    
    return {"schedules": results}

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8502, reload=True)
