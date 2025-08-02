from qgis.core import (
    QgsVectorLayer, 
    QgsFillSymbol, 
    QgsSimpleFillSymbolLayer,
    QgsLineSymbolLayer,
    QgsSymbolLayerUtils,  # For dash patterns
    QgsSingleSymbolRenderer,
    QgsSimpleLineSymbolLayer
)
from qgis.PyQt.QtGui import QColor

def polygonSymbol(
    layer,
    fill_color='200,200,200,150',  # RGBA (default: semi-transparent gray)
    outline_color='0,0,0,255',     # RGBA (default: opaque black)
    outline_width=0.5,
    dash_pattern='5,2',            # Dash pattern (e.g., '5,2' for 5mm dash + 2mm gap)
):

    # Create symbol and remove default layers
    symbol = QgsFillSymbol()
    symbol.deleteSymbolLayer(0)
    
    # ---- FILL LAYER (Transparent) ----
    fill = QgsSimpleFillSymbolLayer()
    r, g, b, a = map(int, fill_color.split(','))
    fill.setColor(QColor(r, g, b, a))  # Apply RGBA fill
    symbol.appendSymbolLayer(fill)
    
    # ---- OUTLINE LAYER (Dashed) ----
    outline = QgsSimpleLineSymbolLayer()
    r, g, b, a = map(int, outline_color.split(','))
    outline.setColor(QColor(r, g, b, a))
    outline.setWidth(outline_width)
    
    # Set dash pattern (convert string like '5,2' to QVector)
    dash_vector = [float(x) for x in dash_pattern.split(',')]
    outline.setCustomDashVector(dash_vector)
    outline.setUseCustomDashPattern(True)
    
    symbol.appendSymbolLayer(outline)
    
    # Apply to layer
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    layer.triggerRepaint()


    from qgis.core import (
    QgsMarkerSymbol,
    QgsSimpleMarkerSymbolLayer,
    QgsSingleSymbolRenderer
)
from qgis.PyQt.QtGui import QColor

def stylePointLayer(layer, size=2, fill_color='23,96,255', outline_color='255,255,255', outline_width=0.2):
    """
    Style a point layer with custom fill/outline.
    
    Args:
        layer: QgsVectorLayer (Point type)
        size: Point size in mm
        fill_color: RGB string (e.g., '23,96,255' for #1760ff)
        outline_color: RGB string (e.g., '255,255,255' for white)
        outline_width: Outline width in mm
    """
    # Create symbol
    symbol = QgsMarkerSymbol()
    symbol.deleteSymbolLayer(0)  # Remove default layer
    
    # Configure marker
    marker = QgsSimpleMarkerSymbolLayer()
    marker.setSize(size)
    marker.setColor(QColor(*map(int, fill_color.split(','))))  # Fill color
    marker.setStrokeColor(QColor(*map(int, outline_color.split(','))))  # Outline color
    marker.setStrokeWidth(outline_width)
    
    symbol.appendSymbolLayer(marker)
    layer.setRenderer(QgsSingleSymbolRenderer(symbol))
    layer.triggerRepaint()