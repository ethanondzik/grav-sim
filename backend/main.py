from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sim import simulate, create_three_body_problem, create_pluto_charon
import json

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from frontend directory
app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")

#dashboard
@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    with open("../frontend/dashboard.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/simulate/{scenario}")
def get_simulation(scenario: str, dt: float = None, steps: int = 1000):
    if scenario == "three_body":
        bodies = create_three_body_problem()
        if dt is None:
            dt = 0.01
    elif scenario == "pluto_charon":
        bodies = create_pluto_charon()
        if dt is None:
            dt = 100  # seconds, since real units
    else:
        return {"error": "Unknown scenario"}

    history = simulate(bodies, dt, steps)
    return {"history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)