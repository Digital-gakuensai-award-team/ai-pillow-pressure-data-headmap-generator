import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

sensor_positions = {
    'Pressure1': (0, 0),
    'Pressure2': (1, 0),
    'Pressure3': (0, 1),
    'Pressure4': (1, 1),
}

def estimate_head_position(row):
    forces = [row[p] for p in sensor_positions]
    total_force = sum(forces)
    if total_force == 0:
        return 0.5, 0.5
    x = sum(row[p] * sensor_positions[p][0] for p in sensor_positions) / total_force
    y = sum(row[p] * sensor_positions[p][1] for p in sensor_positions) / total_force
    return x, y

def generate_heatmap(center_x, center_y, size=100, radius=0.2):
    grid_x, grid_y = np.meshgrid(np.linspace(0, 1, size), np.linspace(0, 1, size))
    distance = np.sqrt((grid_x - center_x)**2 + (grid_y - center_y)**2)
    heatmap = np.clip(1 - distance / radius, 0, 1)
    return heatmap

def main():
    os.makedirs('output', exist_ok=True)
    df = pd.read_csv('sensor_data.csv')
    filenames = []

    for i, row in df.iterrows():
        cx, cy = estimate_head_position(row)
        heatmap = generate_heatmap(cx, cy)

        fig, ax = plt.subplots(figsize=(5, 5))
        im = ax.imshow(heatmap, cmap='jet', origin='lower', extent=(0, 1, 0, 1))
        plt.colorbar(im, ax=ax, label='Pressure Intensity')
        ax.set_title(f'Frame {i}')
        filename = f'output/heatmap_{i:03}.png'
        plt.savefig(filename)
        plt.close()
        filenames.append(filename)
        print(f"Saved: {filename}")

    # GIF生成
    images = [imageio.v2.imread(fn) for fn in filenames]
    imageio.mimsave('output/heatmap_animation.gif', images, fps=5)
    print("✅ アニメーションGIFを生成しました：output/heatmap_animation.gif")

if __name__ == '__main__':
    main()
