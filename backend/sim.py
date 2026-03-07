import numpy as np
import math

G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2

class Body:
    def __init__(self, mass, position, velocity, name=""):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.name = name

def gravitational_acceleration(body, bodies):
    """Calculate the total gravitational acceleration on a body due to other bodies."""
    acceleration = np.zeros(2)
    for other in bodies:
        if other is not body:
            r_vector = other.position - body.position
            r = np.linalg.norm(r_vector)
            if r > 0:
                acceleration += G * other.mass / r**3 * r_vector
    return acceleration

def simulate(bodies, dt, steps):
    """Simulate using Velocity Verlet integrator for better energy conservation."""
    history = []
    accelerations = [gravitational_acceleration(body, bodies) for body in bodies]

    for step in range(steps):
        state = {
            "time": step * dt,
            "bodies": [
                {
                    "name": body.name,
                    "position": body.position.tolist(),
                    "velocity": body.velocity.tolist(),
                    "mass": body.mass
                } for body in bodies
            ]
        }
        history.append(state)

        # Velocity Verlet: update positions
        for i, body in enumerate(bodies):
            body.position += body.velocity * dt + 0.5 * accelerations[i] * dt**2

        # Compute new accelerations
        new_accelerations = [gravitational_acceleration(body, bodies) for body in bodies]

        # Update velocities
        for i, body in enumerate(bodies):
            body.velocity += 0.5 * (accelerations[i] + new_accelerations[i]) * dt

        accelerations = new_accelerations

    return history

def create_three_body_problem():
    bodies = [
        Body(1.0, [0.9700436, -0.24308753], [0.466203685, 0.43236573], "Body1"),
        Body(1.0, [-0.9700436, 0.24308753], [0.466203685, 0.43236573], "Body2"),
        Body(1.0, [0.0, 0.0], [-0.93240737, -0.86473146], "Body3")
    ]
    return bodies

def create_pluto_charon():
    pluto_mass = 1.0e23
    charon_mass = 1.2e22
    distance = 20000.0
    total_mass = pluto_mass + charon_mass
    v_orbital = np.sqrt(G * total_mass / distance)
    bodies = [
        Body(pluto_mass, [0, 0], [0, 0], "Pluto"),
        Body(charon_mass, [distance, 0], [0, v_orbital], "Charon")
    ]
    return bodies

def create_pluto_system():
    """Full Pluto system: Pluto + Charon + Nix + Styx + Kerberos + Hydra.
    All bodies in the barycenter frame with circular orbit velocities."""
    M_pluto = 1.303e22
    M_charon = 1.586e21
    M_nix = 4.5e16
    M_styx = 7.5e15
    M_kerberos = 1.65e16
    M_hydra = 4.8e16

    M_total = M_pluto + M_charon

    # Pluto-Charon orbital distance
    d_pc = 1.9571e7  # 19,571 km in meters

    # Barycenter distances
    r_pluto = M_charon * d_pc / M_total
    r_charon = M_pluto * d_pc / M_total

    # Orbital velocity
    v_orbital = math.sqrt(G * M_total / d_pc)
    v_pluto = M_charon / M_total * v_orbital
    v_charon = M_pluto / M_total * v_orbital

    # Small moon semi-major axes (m)
    r_styx = 4.2656e7
    r_nix = 4.8694e7
    r_kerberos = 5.7783e7
    r_hydra = 6.4738e7

    # Circular orbit velocities
    v_styx = math.sqrt(G * M_total / r_styx)
    v_nix = math.sqrt(G * M_total / r_nix)
    v_kerberos = math.sqrt(G * M_total / r_kerberos)
    v_hydra = math.sqrt(G * M_total / r_hydra)

    # Starting angles (spread moons around orbits)
    a_styx = math.radians(45)
    a_nix = math.radians(135)
    a_kerberos = math.radians(225)
    a_hydra = math.radians(315)

    bodies = [
        Body(M_pluto, [-r_pluto, 0], [0, -v_pluto], "Pluto"),
        Body(M_charon, [r_charon, 0], [0, v_charon], "Charon"),
        Body(M_styx,
             [r_styx * math.cos(a_styx), r_styx * math.sin(a_styx)],
             [-v_styx * math.sin(a_styx), v_styx * math.cos(a_styx)],
             "Styx"),
        Body(M_nix,
             [r_nix * math.cos(a_nix), r_nix * math.sin(a_nix)],
             [-v_nix * math.sin(a_nix), v_nix * math.cos(a_nix)],
             "Nix"),
        Body(M_kerberos,
             [r_kerberos * math.cos(a_kerberos), r_kerberos * math.sin(a_kerberos)],
             [-v_kerberos * math.sin(a_kerberos), v_kerberos * math.cos(a_kerberos)],
             "Kerberos"),
        Body(M_hydra,
             [r_hydra * math.cos(a_hydra), r_hydra * math.sin(a_hydra)],
             [-v_hydra * math.sin(a_hydra), v_hydra * math.cos(a_hydra)],
             "Hydra"),
    ]
    return bodies