import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from stl import mesh

inp = sys.argv[1]
outp = sys.argv[2]

your_mesh = mesh.Mesh.from_file(inp)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

faces = your_mesh.vectors
ax.add_collection3d(Poly3DCollection(faces, alpha=0.9, facecolor='cyan', linewidths=0.1, edgecolor='black'))

scale = your_mesh.points.flatten()
ax.auto_scale_xyz(scale, scale, scale)
ax.set_axis_off()

plt.savefig(outp, dpi=300, bbox_inches='tight', pad_inches=0)
plt.close(fig)
