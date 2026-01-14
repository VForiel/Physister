import numpy as np
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist (though it should)
output_dir = os.path.dirname(os.path.abspath(__file__))

# Parameters
R = 0.1 # m
g = 10  # m/s^2
t_star = 0.8 # s

# Time vector for Q4
t_q4 = np.linspace(0, 3.2, 500)

# Q4: No Electric Field
# --------------------
# After t_star:
# Ball 1 (Big): z1 = 3R (at rest on ground) -> z1 - 3R = 0
# Ball 2 (Small): z2(t') = z2(t_star) + v2+ * t' - 0.5 * g * t'^2
# z2(t_star) = 7R = 0.7 m
# v2+ = 16 m/s
# t' = t - t_star

z1_q4 = np.zeros_like(t_q4)
z2_q4 = np.zeros_like(t_q4)

for i, t in enumerate(t_q4):
    t_prime = t - t_star
    if t < t_star:
        # Before rebound, falling together (not requested but for completeness?)
        # z(t) = h - 0.5 * g * t^2
        # z1 = h - 0.5gt^2 (center at 3.2?) No, center 1 was at 3.2?
        # Let's stick to the requested plot interval or just after rebound as implied
        # Usually curves start at t=0.
        # Initial positions at t=0:
        # z1(0) = h = 3.2 m (Wait, h=3.2 is from bottom? No, "lâche les deux balles d'une hauteur h=3.2m". Usually means bottom ball height or center of mass?
        # Let's assume h is height of contact point or lowest point?
        # Re-reading: "En t=0, Thomas lâche les deux balles d'une hauteur h=3.2m."
        # "En t=t*, la grosse balle atteint le sol."
        # h = 0.5 * g * t*^2 = 0.5 * 10 * 0.64 = 3.2 m.
        # So at t=0, lowest point of big ball was at 3.2m?
        # If z1(t*) = R1 = 0.3m (radius). Then z1(0) = 0.3 + 3.2 = 3.5m?
        # Let's assume standard free fall distance h=3.2m traveled.
        # Fall distance = 3.2m.
        # z1(t*) = 3R = 0.3m. So z1(0) = 3.5m.
        # z2(t*) = 7R = 0.7m. So z2(0) = 3.9m.
        
        z1_q4[i] = (3.5 - 0.5 * g * t**2) - 3*R
        z2_q4[i] = (3.9 - 0.5 * g * t**2) - 7*R
    else:
        # After rebound
        # Big ball (1): at rest -> z1 = 3R
        z1_q4[i] = 3*R - 3*R # 0
        
        # Small ball (2): Rebound
        # z2(t') = 0.7 + 16t' - 5t'^2
        z2_val = 0.7 + 16*t_prime - 0.5*g*t_prime**2
        z2_q4[i] = z2_val - 7*R

# Plot Q4
plt.figure(figsize=(10, 6))
plt.plot(t_q4, z1_q4, label=r'$z_1(t) - 3R$ (Grosse balle)', linewidth=2)
plt.plot(t_q4, z2_q4, label=r'$z_2(t) - 7R$ (Petite balle)', linewidth=2)
plt.axvline(x=t_star, color='k', linestyle='--', alpha=0.5, label='$t_*$ (Rebond)')
plt.title("Question 4: Trajectoires sans champ électrique")
plt.xlabel("Temps (s)")
plt.ylabel("Position relative (m)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, 'trajectory_q4.png'))
plt.close()


# Q5: With Electric Field
# ---------------------
# Field starts at t_star = 0.8s
# Catch up at t_double_star approx 1.87s

t_q5 = np.linspace(0, 2.0, 500) # Plot slightly past catch up
z1_q5 = np.zeros_like(t_q5)
z2_q5 = np.zeros_like(t_q5)

def pos_q5(t):
    t_prime = t - t_star
    
    # Pre-rebound (same as Q4)
    if t < t_star:
        z1 = 3.5 - 0.5 * g * t**2
        z2 = 3.9 - 0.5 * g * t**2
        return z1 - 3*R, z2 - 7*R
    
    # Post-rebound (t > t_star) WITH Field
    else:
        # Big ball (1): a1 = -10 m/s^2 (up), v1+ = 0
        # z1(t') = 0.3 + 5 t'^2
        z1 = 0.3 + 5 * t_prime**2
        
        # Small ball (2): a2 = 20 m/s^2 (down), v2+ = 16 m/s (up)
        # z2(t') = 0.7 + 16 t' - 10 t'^2
        z2 = 0.7 + 16 * t_prime - 10 * t_prime**2
        
        return z1 - 3*R, z2 - 7*R

for i, t in enumerate(t_q5):
    z1_q5[i], z2_q5[i] = pos_q5(t)

# Calculate exact catch up time for marking
# 15 t'^2 - 16 t' + 0.3 = 0 -> t' approx 1.067 -> t** approx 1.867
t_catch = 1.867

plt.figure(figsize=(10, 6))
plt.plot(t_q5, z1_q5, label=r'$z_1(t) - 3R$ (Grosse balle)', linewidth=2)
plt.plot(t_q5, z2_q5, label=r'$z_2(t) - 7R$ (Petite balle)', linewidth=2)
plt.axvline(x=t_star, color='k', linestyle='--', alpha=0.5, label='$t_*$ (Rebond/Champ ON)')
plt.axvline(x=t_catch, color='r', linestyle='--', alpha=0.5, label='$t_{**}$ (Rattrapage)')

# Mark catch up point
idx_catch = np.argmin(np.abs(t_q5 - t_catch))
plt.scatter([t_catch], [z1_q5[idx_catch]], color='red', zorder=5)

plt.title("Question 5: Trajectoires avec champ électrique")
plt.xlabel("Temps (s)")
plt.ylabel("Position relative (m)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(output_dir, 'trajectory_q5.png'))
plt.close()

print("Plots generated successfully.")
