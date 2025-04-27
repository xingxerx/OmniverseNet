import numpy as np
import matplotlib.pyplot as plt
class NanoParticle:
  def __init__(self, size, material, charge):
    self.size = size  # in nanometers
    self.material = material
    self.charge = charge
  def interact(self, other_particle):
    # Van der Waals force calculation
    force = (1e-21 * self.charge * other_particle.charge) / (self.size * other_particle.size)
    return force
class NanoSystem:
  def __init__(self, particles):
    self.particles = particles
  def simulate(self, steps):
    for _ in range(steps):
      for i in range(len(self.particles)):
        for j in range(i+1, len(self.particles)):
          force = self.particles[i].interact(self.particles[j])
          # Update particle positions based on force
          self.particles[i].size += force * 1e-6
          self.particles[j].size -= force * 1e-6
  def plot_system(self):
    sizes = [p.size for p in self.particles]
    plt.hist(sizes, bins=10)
    plt.show()
# Example usage:
particle1 = NanoParticle(10, "Gold", 1)
particle2 = NanoParticle(15, "Silver", -1)
system = NanoSystem([particle1, particle2])
system.simulate(1000)
system.plot_system()

