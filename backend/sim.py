import numpy as np

G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

class Body:
    def __init__(self, mass, position, velocity, name=""):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.name = name

def gravitational_acceleration(body, bodies):
    """Calculate the total gravitational acceleration on a body due to other bodies."""
    acceleration = np.zeros(2)  # Assuming 2D for simplicity
    for other in bodies:
        if other is not body:
            r_vector = other.position - body.position
            r = np.linalg.norm(r_vector)
            if r > 0:
                acceleration += G * other.mass / r**3 * r_vector
    return acceleration

def simulate(bodies, dt, steps):
    """Simulate the system for given steps with time step dt."""
    history = []
    for step in range(steps):
        # Record current state
        state = {
            "time": step * dt,
            "bodies": [
                {
                    "name": body.name,
                    "position": body.position.tolist(),
                    "velocity": body.velocity.tolist()
                } for body in bodies
            ]
        }
        history.append(state)

        # Update velocities and positions using Euler method
        for body in bodies:
            acceleration = gravitational_acceleration(body, bodies)
            body.velocity += acceleration * dt
            body.position += body.velocity * dt

    return history

# Example: 3-body problem (figure-eight or something simple)
def create_three_body_problem():
    # Masses in kg, positions in AU, velocities in AU/day (simplified units)
    # For simplicity, use astronomical units
    bodies = [
        Body(1.0, [0.9700436, -0.24308753], [0.466203685, 0.43236573], "Body1"),
        Body(1.0, [-0.9700436, 0.24308753], [0.466203685, 0.43236573], "Body2"),
        Body(1.0, [0.0, 0.0], [-0.93240737, -0.86473146], "Body3")
    ]
    return bodies

# Pluto-Charon system
def create_pluto_charon():
    # Masses in kg
    pluto_mass = 1.309e22
    charon_mass = 1.586e21
    distance = 19571e3  # meters
    total_mass = pluto_mass + charon_mass
    # Distance from CM to Pluto
    r_pluto = charon_mass / total_mass * distance
    r_charon = pluto_mass / total_mass * distance
    # Velocities
    mu = G * total_mass
    v_orbital = np.sqrt(G * pluto_mass * charon_mass / distance) / (distance / 2)  # approx
    # Better: v = sqrt(G M / r) for reduced mass
    v_pluto = np.sqrt(G * charon_mass / distance)
    v_charon = np.sqrt(G * pluto_mass / distance)

    bodies = [
        Body(pluto_mass, [-r_pluto, 0], [0, v_pluto], "Pluto"),
        Body(charon_mass, [r_charon, 0], [0, -v_charon], "Charon")
    ]
    return bodies