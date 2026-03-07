from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sim import simulate, create_three_body_problem, create_pluto_charon, create_pluto_system
import json

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #specify the frontend URL in prod
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
def get_simulation(scenario: str, dt: float = None, steps: int = 500):
    try:
        if scenario == "three_body":
            bodies = create_three_body_problem()
            if dt is None:
                dt = 0.01
        elif scenario == "pluto_charon":
            bodies = create_pluto_charon()
            if dt is None:
                dt = 0.1
        elif scenario == "pluto_system":
            bodies = create_pluto_system()
            if dt is None:
                dt = 1000
            if steps == 500:
                steps = 4000
        else:
            return {"error": "Unknown scenario"}

        history = simulate(bodies, dt, steps)
        return {"history": history, "steps": len(history), "scenario": scenario}
    except Exception as e:
        return {"error": str(e), "scenario": scenario}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)