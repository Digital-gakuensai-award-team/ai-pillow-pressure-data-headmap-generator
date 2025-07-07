# ai-pillow-pressure-data-headmap-generator

本リポジトリは，AI枕プロジェクトにおいて，CSVに記録された圧力データから頭部の位置を推定し，二次元ヒートマップとして出力するシステムです。  
本ツールは，ユーザの頭部位置の可視化を通じて，AI枕のリアルタイム制御や適切な高さ・形状調整に役立てることを目的としています。

---

## 仕様

### 🎯 目的

- 枕にかかる圧力分布から頭部の位置を推定し，ヒートマップとして可視化することで今後の開発効率向上を目指す。
- 睡眠姿勢の分析や個人最適化アルゴリズム開発に応用する。

### 📄 入力

- 圧力センサ情報を含むCSVファイル（`sensor_data/sensor_data.csv`）
- 圧力データは以下の4次元：
  - `Pressure1`: 左上
  - `Pressure2`: 右上
  - `Pressure3`: 左下
  - `Pressure4`: 右下

### 🧠 出力

- 頭部推定位置を中心としたヒートマップ画像（赤：高圧 → 青：低圧）
- 各時刻のヒートマップ画像を `output/` に保存（PNG）
- すべてのフレームを1つにまとめたアニメーションGIF（`output/heatmap_animation.gif`）
## 🎥 出力イメージ
![gif](https://github.com/Digital-gakuensai-award-team/ai-pillow-pressure-data-headmap-generator/blob/main/output/heatmap_animation.gif?raw=true)



### 💻 頭の位置推定式

各圧力センサの値 $F_i$ と設置位置 $(P_{ix}, P_{iy})$ を用い，頭部の重心を以下の加重平均で求めます：

$$
x = \frac{F_1 \cdot P_{1x} + F_2 \cdot P_{2x} + F_3 \cdot P_{3x} + F_4 \cdot P_{4x}}{F}
$$

$$
y = \frac{F_1 \cdot P_{1y} + F_2 \cdot P_{2y} + F_3 \cdot P_{3y} + F_4 \cdot P_{4y}}{F}
$$

- $F = F_1 + F_2 + F_3 + F_4$
- 枕サイズは横60cm × 縦40cmで、センサ位置はそれを基準に決定

---

## ⚙️ 処理の流れ

1. `sensor_data.csv` を読み込む
2. 各行の圧力値から頭部中心位置を加重平均で推定
3. 中心位置をもとにヒートマップ画像を生成（PNGで保存）
4. すべての画像をGIFとして結合

---

## 💻 実行環境

- Python 3.11.9
- 仮想環境（venv）推奨
- 必要ライブラリは `requirements.txt` に記載

```bash
# 仮想環境の作成と起動（初回のみ）
python -m venv venv
.\venv\Scripts\activate          # Windows の場合
source venv/bin/activate        # macOS/Linux の場合

# 必要パッケージのインストール
pip install -r requirements.txt

# メインスクリプトの実行
python main.py
