# ha_geophys_interpretation

A QGIS plugin to support the archaeological interpretation of greyscale geophysical survey data.

## 🧠 Project Goal

This project aims to assist archaeologists in interpreting greyscale geophysical images by developing a machine-learning-driven workflow that can **automatically identify and categorise patterns** in the data. 

The final goal is a tool that can **streamline the interpretation process**, reduce manual work, and support consistency across large datasets.

---

## 📍 Current Stage: Pixel-based Digitisation

We are currently in **Phase 1** of development. The current functionality includes:

- **Digitisation based on pixel values** from greyscale raster layers (e.g. magnetometry).
- **Initial filtering** of generated features based on:
  - Area size
  - Pixel value range (threshold)
- **Exporting filtered features** into **three temporary layers** for further inspection or classification.

This stage lays the groundwork for future integration with pattern recognition and ML-based classification techniques.

---

## 🛠️ How It Works

1. Load a **greyscale raster layer** into QGIS (e.g. geophysics survey result).
2. Run the plugin from the QGIS plugin toolbar.
3. The plugin will:
   - Scan pixels and digitise features based on pixel intensity.
   - Filter out small areas or noise based on predefined size thresholds.
   - Categorise outputs into **three temporary layers** (e.g. `Low`, `Medium`, `High` signal zones).

---

## 🚀 Planned Features (Future Work)

- Integration with **scikit-learn** or other ML libraries to categorise patterns (e.g. pits, ditches, walls).
- Export classified features with confidence scores.
- GUI improvements for custom thresholds and training data selection.

---

## 🧩 Tech Stack

- **QGIS Python API** (PyQGIS)
- **Python** 3.10+
- **QGIS Plugin Template**
- Future: **scikit-learn**, **NumPy**, **OpenCV**, **PostGIS**