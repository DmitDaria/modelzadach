import numpy as np
import matplotlib.pyplot as plt

def gr(x1, x2):
    p1 = (x1**2 + x2**2) / 4000
    p2 = np.cos(x1 / np.sqrt(1)) * np.cos(x2 / np.sqrt(2))
    return p1 - p2 + 1

x1 = np.linspace(-10.0, 10.0, 100)
x2 = np.linspace(-10.0, 10.0, 100)
X1, X2 = np.meshgrid(x1, x2)
Y = gr(X1, X2)
x10, x20 = 0.0, 0.0
y0 = gr(x10, x20)

fig = plt.figure(figsize=(16, 12))
fig.suptitle(f'Тестовая точка: ({x10}, {x20}), Значение функции: {y0:.4f}', fontsize=14)

ax1 = fig.add_subplot(221, projection='3d')
surf = ax1.plot_surface(X1, X2, Y, cmap='plasma')
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.set_zlabel('y = f(x1, x2)')
ax1.set_title('3D поверхность в изометрическом виде')

ax2 = fig.add_subplot(222)
contour = ax2.contourf(X1, X2, Y, levels=20, cmap='plasma')
ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.set_title('3D поверхность (вид сверху)')

ax3 = fig.add_subplot(223)
y_x1 = gr(x1, x20)
ax3.plot(x1, y_x1)
ax3.set_xlabel('x1')
ax3.set_ylabel('y = f(x1, x2=0)')
ax3.set_title(f'График функции при x2 = {x20}')
ax3.grid(True)

ax4 = fig.add_subplot(224)
y_x2 = gr(x10, x2)
ax4.plot(x2, y_x2)
ax4.set_xlabel('x2')
ax4.set_ylabel('y = f(x1=0, x2)')
ax4.set_title(f'График функции при x1 = {x10}')
ax4.grid(True)
plt.show()