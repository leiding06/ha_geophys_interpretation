# utils/layer_processing.py

import os
from qgis.core import (
    QgsProject,   QgsCoordinateReferenceSystem,
     edit
)
from qgis.core import QgsApplication, QgsProcessingAlgorithm, QgsProcessingException
import processing
import time

def timed_run(name, algorithm_id, parameters):
    start = time.time()
    result = processing.run(algorithm_id, parameters)
    end = time.time()
    print(f"[{name}] time used: {end - start:.2f} seconds")
    return result

def process_pixel(raster_layer,  value_exp, area_exp, disturbance = ''):
    if QgsApplication.processingRegistry().algorithmById('gdal:polygonize'):
        # Use GDAL if available
        raster_poly = timed_run("Polygonize","gdal:polygonize", {
            'INPUT': raster_layer,
            'BAND': 1,
            'FIELD': 'VALUE',
            'EIGHT_CONNECTEDNESS': False,
            'EXTRA': '',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']
    else:
        # Fallback to native:pixelstopolygons if GDAL not found
        raster_poly = timed_run("Polygonize","native:pixelstopolygons", {
            'INPUT_RASTER': raster_layer,
            'RASTER_BAND': 1,
            'FIELD_NAME': 'VALUE',
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']

        
    threshold_poly = timed_run("Threshold extracted","native:extractbyexpression", {
        'INPUT': raster_poly,
        'EXPRESSION': value_exp,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })['OUTPUT']

    dissolved = timed_run("Dissolve","native:dissolve", {
        'INPUT': threshold_poly,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })['OUTPUT']

    singleparts = timed_run("Singleparts","native:multiparttosingleparts", {
        'INPUT': dissolved,
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })['OUTPUT']
    
    # Remove unnecessary fields
    delete_fid= timed_run("Delete_fid","native:deletecolumn", {
        'INPUT': singleparts,
        'COLUMN': ['fid'],
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })['OUTPUT']
    #test:
    delete_fid.setCrs(QgsCoordinateReferenceSystem("EPSG:27700"))
    
    


    add_geom = timed_run("Add area","qgis:exportaddgeometrycolumns",{
        'INPUT': delete_fid,
        'CALC_METHOD':0,
        'OUTPUT':'TEMPORARY_OUTPUT'
    })['OUTPUT']
    

    filtered_polygon = timed_run("Filter polygon","native:extractbyexpression", {
        'INPUT': add_geom,
        'EXPRESSION': area_exp, #"area"
        'OUTPUT': 'TEMPORARY_OUTPUT'
    })['OUTPUT']
    filtered_polygon.setCrs(QgsCoordinateReferenceSystem("EPSG:27700"))

    if disturbance == 'Yes':
        extent_layers = QgsProject.instance().mapLayersByName("Survey Extent")
        if not extent_layers:
            raise QgsProcessingException("Layer 'Survey Extent' not found.")
        extent_layer = extent_layers[0]
        # Polygon to line
        extent_lines = timed_run("Survey Polygon to Line","native:polygonstolines", {
            'INPUT': extent_layer,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']
        

        # Buffer 0.1m
        buffer = timed_run("Buffer","native:buffer",{
            'INPUT': extent_lines,
            'DISTANCE': 0.2,
            'SEGMENTS':5,
            'END_CAP_STYLE':0,
            'JOIN_STYLE': 0,
            'MITER_LIMIT':2,
            'DISSOLVE':False,
            'SEPARATE_DISJOINT':False,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        })['OUTPUT']
        
        buffer.setCrs(QgsCoordinateReferenceSystem("EPSG:27700"))


        # Extract by location
        extract_by_location = timed_run("Select when intersect with extent edge","native:extractbylocation", {
            'INPUT':delete_fid,
            'PREDICATE':[0], 
            'INTERSECT': buffer,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
        
        if extract_by_location is None:
            iface.messageBar.pushWarning("Error","Looks like there is no survey extent match with you greyscale." )

        #Delete holes
        disturbance_polygon = timed_run("Disturbance","native:deleteholes", {
            'INPUT':extract_by_location,
            'MIN_AREA': 0,
            'OUTPUT':'TEMPORARY_OUTPUT'
        })['OUTPUT']
       

        processing.run("native:selectbylocation",{
            'INPUT':filtered_polygon,
            'PREDICATE':[0],
            'INTERSECT':disturbance_polygon,
            'METHOD':0
        })
        with edit(filtered_polygon):
            filtered_polygon.dataProvider().deleteFeatures(filtered_polygon.selectedFeatureIds())

        
    
        


        return filtered_polygon, disturbance_polygon


    else:
        return filtered_polygon


def tidy_points(filtered_polygon):
    # create centriod for the point layer
    
    centroid =  processing.run("native:centroids", {
        'INPUT':filtered_polygon,
        'ALL_PARTS':False,
        'OUTPUT':'TEMPORARY_OUTPUT'})['OUTPUT']

   
    return centroid

