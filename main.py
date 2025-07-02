
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

PILLOW_WIDTH = 60
PILLOW_HEIGHT = 40

sensor_positions = {
    'Pressure1': (PILLOW_WIDTH, 0),
    'Pressure2': (PILLOW_WIDTH, PILLOW_HEIGHT),
    'Pressure3': (0, 0),
    'Pressure4': (0, PILLOW_HEIGHT)
}

def estimate_head_position_cm(row):
    total_force = sum(row[p] for p in sensor_positions)
    if total_force == 0:
        return PILLOW_WIDTH / 2, PILLOW_HEIGHT / 2
    x = sum(row[p] * sensor_positions[p][0] for p in sensor_positions) / total_force
    y = sum(row[p] * sensor_positions[p][1] for p in sensor_positions) / total_force
    return x, y

def generate_heatmap(center_x, center_y, size=100, radius=10, filename='output/heatmap.png'):
    grid_x, grid_y = np.meshgrid(
        np.linspace(0, PILLOW_WIDTH, size),
        np.linspace(0, PILLOW_HEIGHT, size)
    )
    distance = np.sqrt((grid_x - center_x) ** 2 + (grid_y - center_y) ** 2)
    heatmap = np.clip(1 - distance / radius, 0, 1)

    plt.figure(figsize=(6, 4))
    plt.imshow(heatmap, cmap='jet', origin='lower',
               extent=(0, PILLOW_WIDTH, 0, PILLOW_HEIGHT))
    plt.colorbar(label='Pressure Intensity')
    plt.title('Estimated Head Position Heatmap')
    plt.savefig(filename)
    plt.close()

def main():
    os.makedirs('output', exist_ok=True)
    df = pd.read_csv('sensor_data/sensor_data.csv')

    filenames = []

    for i, row in df.iterrows():
        cx, cy = estimate_head_position_cm(row)
        filepath = f'output/heatmap_{i:03}.png'
        generate_heatmap(cx, cy, filename=filepath)
        filenames.append(filepath)
        print(f"Saved: {filepath}")

    images = [imageio.v2.imread(f) for f in filenames]
    imageio.mimsave('output/heatmap_animation.gif', images, fps=5)
    print("✅ GIF生成完了: output/heatmap_animation.gif")

if __name__ == '__main__':
    main()
