# ヒートマップ生成スクリプト（AI枕プロジェクト）
# 圧力センサデータから頭の位置を推定し、
# 各フレームのヒートマップを生成 → GIFにまとめる

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import imageio
import os

# 枕サイズ（cm）※可変化可能
PILLOW_WIDTH = 60
PILLOW_HEIGHT = 40

# センサ配置（物理座標、cm）
# Pressure1: 左上, Pressure2: 右上, Pressure3: 左下, Pressure4: 右下
sensor_positions = {
    'Pressure1': (0, 0),
    'Pressure2': (PILLOW_WIDTH, 0),
    'Pressure3': (0, PILLOW_HEIGHT),
    'Pressure4': (PILLOW_WIDTH, PILLOW_HEIGHT)
}

# 圧力値の加重平均により頭部位置（x, y）を推定
def estimate_head_position_cm(row):
    total_force = sum(row[p] for p in sensor_positions)
    if total_force == 0:
        # 圧力がゼロなら中央を仮の頭部位置とする
        return PILLOW_WIDTH / 2, PILLOW_HEIGHT / 2
    # 各センサの位置 × 圧力 を合計し、全体で割って加重平均
    x = sum(row[p] * sensor_positions[p][0] for p in sensor_positions) / total_force
    y = sum(row[p] * sensor_positions[p][1] for p in sensor_positions) / total_force
    return x, y

# ヒートマップ生成（赤：圧中心、青：周囲）
def generate_heatmap(center_x, center_y, size=100, radius=10, filename='output/heatmap.png'):
    # 枕サイズの格子状グリッド（size×size）を生成
    grid_x, grid_y = np.meshgrid(
        np.linspace(0, PILLOW_WIDTH, size),
        np.linspace(0, PILLOW_HEIGHT, size)
    )
    # 各点の中心からの距離を計算し、擬似的な圧力分布とする
    distance = np.sqrt((grid_x - center_x) ** 2 + (grid_y - center_y) ** 2)
    heatmap = np.clip(1 - distance / radius, 0, 1)  # 半径内を1〜0で表現

    # 可視化
    plt.figure(figsize=(6, 4))
    plt.imshow(heatmap, cmap='jet', origin='lower',
               extent=(0, PILLOW_WIDTH, 0, PILLOW_HEIGHT))
    plt.colorbar(label='Pressure Intensity')
    plt.title('Estimated Head Position Heatmap')
    plt.savefig(filename)
    plt.close()

# メイン処理：CSV → PNG群 → GIF出力
def main():
    os.makedirs('output', exist_ok=True)  # 出力フォルダを作成
    df = pd.read_csv('sensor_data/sensor_data.csv')  # センサデータ読み込み

    filenames = []  # GIF用フレーム画像パスの記録用リスト

    # 各行＝各時間ステップについて処理
    for i, row in df.iterrows():
        cx, cy = estimate_head_position_cm(row)
        filepath = f'output/heatmap_{i:03}.png'
        generate_heatmap(cx, cy, filename=filepath)
        filenames.append(filepath)
        print(f"Saved: {filepath}")

    # PNG群をまとめてGIFに変換
    images = [imageio.v2.imread(f) for f in filenames]
    imageio.mimsave('output/heatmap_animation.gif', images, fps=5)
    print("✅ GIF生成完了: output/heatmap_animation.gif")

# スクリプトとして実行されたときのみ main() を呼び出す
if __name__ == '__main__':
    main()
