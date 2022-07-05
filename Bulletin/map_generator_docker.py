from qgis.PyQt import *
from qgis.core import *
from qgis.PyQt.QtGui import *
import os
import sys
from PyQt5 import Qt
import datetime

os.environ["QT_QPA_PLATFORM"] = "offscreen"

#Supply the path to the qgis install location
qgs = QgsApplication([], True)
QgsApplication.setPrefixPath("/usr/bin/qgis", True)


#Load providers
qgs.initQgis()
print("Docker environmets set")
###################################################################
###################################################################
#Project
###################################################################
###################################################################

def makeMap(mapVariable):

    if mapVariable == "chl":
        ColorRampValues = [0,3,6,9,12]
        MapTitle = "Bottom chlorophyll concentration"
        Unit = "mg/m\u00B3"
        Path_to_Tiff = r"/usr/src/app/Bulletin/chl.tif"
        
    if mapVariable == "botsalt":
        ColorRampValues = [20,23,26,29,32]
        MapTitle = "Bottom salinity"
        Unit = "g/kg"
        Path_to_Tiff = r"/usr/src/app/Bulletin/botsalt.tif"
        
    if mapVariable == "bottemp":
        ColorRampValues = [0,6,12,18,24]
        MapTitle = "Bottom temperature"
        Unit = "\u00B0C"
        Path_to_Tiff = r"/usr/src/app/Bulletin/bottemp.tif"
        
    if mapVariable ==  "oxy":
        ColorRampValues = [4,6.5,9,11.5,14]
        MapTitle = "Bottom oxygen concentration"
        Unit = "mg/L"
        Path_to_Tiff = r"/usr/src/app/Bulletin/oxy_mgL.tif"

    if mapVariable == "resup":
        ColorRampValues = [0,0.015,0.03,0.045,0.06]
        MapTitle = "Resuspension of sediments"
        Unit = "g-POM/m\u00B2/d"
        Path_to_Tiff = r"/usr/src/app/Bulletin/resup.tif"

    if mapVariable == "ssi":
        ColorRampValues = [0,0.25,0.5,0.75,1]
        MapTitle = "Site suitability index"
        Unit = "Index"
        Path_to_Tiff = r"/usr/src/app/Bulletin/ssi.tif"

    QgsProject.instance().clear()

    #Create project
    project = QgsProject.instance()
    crs = project.crs()
    crs.createFromId(4326)
    project.setCrs(crs)

    #Import layers
    #Set path to layers
    basemap_path = r"/usr/src/app/Bulletin/OSM_standard_tile_layer.xml"
    data_layer_path = Path_to_Tiff

    #Define path and name
    basemap_layer = QgsRasterLayer(basemap_path, "Basemap")
    data_layer_layer = QgsRasterLayer(data_layer_path, Unit)

    #Import layers to project
    project.addMapLayer(basemap_layer)
    project.addMapLayer(data_layer_layer)

    ################################################################
    #Editing the indiviual layers
    ################################################################

    ###Editing data_layer###

    #Set color ramp
    ColorRamp = QgsColorRampShader(ColorRampValues[0], ColorRampValues[4])
    ColorRamp.setColorRampType(QgsColorRampShader.Interpolated)
    ColorRampRange = [QgsColorRampShader.ColorRampItem(ColorRampValues[0], QColor(255,255,0)),\
                      QgsColorRampShader.ColorRampItem(ColorRampValues[1], QColor(0,255,0)),\
                      QgsColorRampShader.ColorRampItem(ColorRampValues[2], QColor(0,255,255)),\
                      QgsColorRampShader.ColorRampItem(ColorRampValues[3], QColor(0,0,255)),\
                      QgsColorRampShader.ColorRampItem(ColorRampValues[4], QColor(255,0,255))]
    ColorRamp.setColorRampItemList(ColorRampRange)
    ApplyRamp = QgsRasterShader()
    ApplyRamp.setRasterShaderFunction(ColorRamp)
    renderer = QgsSingleBandPseudoColorRenderer(data_layer_layer.dataProvider(), 1, ApplyRamp)
    data_layer_layer.setRenderer(renderer)

    #Set some default extentsChange
    Limfjord = QgsRectangle(QgsPointXY(float(sys.argv[1]),float(sys.argv[3])), QgsPointXY(float(sys.argv[2]),float(sys.argv[4])))


    ################################################################
    #Creation of the mapframe
    ################################################################

    ###Create layout with settings###

    #Give a name to layout
    layoutName = mapVariable

    #Assign variable with layout manager class
    layout_manager = project.layoutManager()

    #If layout exists, delete it
    layouts_list = layout_manager.printLayouts()
    for items in layouts_list:
        if items.name() == layoutName:
            manager.removeLayout(items)

    #Add the project including the list of layers to the layout
    layout = QgsPrintLayout(project)
    #Initialize default settings
    layout.initializeDefaults()
    #Give the layout a name
    layout.setName(layoutName)

    #set layout size
    layout_size = layout.pageCollection()
    layout_size.pages()[0].setPageSize('A6', QgsLayoutItemPage.Orientation.Landscape)
    #add current layout to the manager of layouts
    layout_manager.addLayout(layout)

    ###Map-item###

    #add the layout as a map item in the print manager
    map = QgsLayoutItemMap(layout)
    map.setRect(30, 30, 30, 30)

    #set the map extent
    map_settings = QgsMapSettings()
    #Choose which layer the extent will be set to
    map_settings.setLayers([data_layer_layer])
    #Display the full extent of the layer otherwise custom x and y can be set
    rect = Limfjord
    rect.scale(1.0)
    #set the map extent to the defined rectangle
    map_settings.setExtent(rect)
    #set mapframe to the same extent
    map.setExtent(rect)

    ###Grid###

    grid = QgsLayoutItemMapGrid("Grid", map)
    grid.Cross
    grid.setIntervalX(0.2)
    grid.setIntervalY(0.2)
    grid.setAnnotationEnabled(True)
    grid.setAnnotationPrecision(1)
    grid.setAnnotationPosition(QgsLayoutItemMapGrid.InsideMapFrame, QgsLayoutItemMapGrid.Left)
    grid.setAnnotationPosition(QgsLayoutItemMapGrid.InsideMapFrame, QgsLayoutItemMapGrid.Top)
    grid.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Right)
    grid.setAnnotationPosition(QgsLayoutItemMapGrid.OutsideMapFrame, QgsLayoutItemMapGrid.Bottom)
    grid_line = QgsSimpleLineSymbolLayer()
    grid_line.setPenStyle(Qt.Qt.PenStyle(Qt.Qt.DotLine))
    grid_line.setColor(QColor(23,111,176))
    grid_line_symbol = QgsLineSymbol()
    grid_line_symbol.changeSymbolLayer(0, grid_line)
    grid.setLineSymbol(grid_line_symbol)

    map.grids().addGrid(grid)

    #add map item to layout
    layout.addLayoutItem(map)


    #sent upper left corner of the map item
    map.attemptMove(QgsLayoutPoint(0, 15, QgsUnitTypes.LayoutMillimeters))
    #set size of the map item
    map.attemptResize(QgsLayoutSize(119.4, 90, QgsUnitTypes.LayoutMillimeters))

    ###Legend###

    #Create a legend item in the map layout
    legend = QgsLayoutItemLegend(layout)
    legend.setTitle("Legend")
    legend.setSymbolHeight(85)
    legend.setAutoUpdateModel(False)
    legend.setFontColor(QColor(23,111,176))

    #Build layer tree layer 0 = data-layer, layer 1 = basemap
    layerTree = QgsLayerTree()
    layerTree.addLayer(data_layer_layer)
    layerTree.addLayer(basemap_layer)
    layerTreeModel = QgsLayerTreeModel(layerTree)
    #Remove layers from legend
    legend.model().rootGroup().removeLayer(basemap_layer)
    #Remove "band 1 - (grey)" node from legend
    data_layer_LayerTreeLayer = legend.model().rootGroup().findLayer(data_layer_layer)
    QgsMapLayerLegendUtils.setLegendNodeOrder(data_layer_LayerTreeLayer,[1])
    legend.model().refreshLayerLegend(data_layer_LayerTreeLayer)
    #add to layout
    layout.addLayoutItem(legend)
    legend.attemptMove(QgsLayoutPoint(119.8, 0, QgsUnitTypes.LayoutMillimeters))
    
     ##Intermediate legend values##
    Intermediate1 = QgsLayoutItemLabel(layout)
    Intermediate1.setText(str(ColorRampValues[3]))
    Intermediate1.setFont(QFont('MS Shell Dlg 2',12))
    Intermediate1.setFontColor(QColor(23,111,176))
    Intermediate1.adjustSizeToText()
    Intermediate1.setHAlign(Qt.Qt.AlignLeft)
    layout.addLayoutItem(Intermediate1)
    Intermediate1.attemptMove(QgsLayoutPoint(130.3,38.3, QgsUnitTypes.LayoutMillimeters))
    
    Intermediate1 = QgsLayoutItemLabel(layout)
    Intermediate1.setText(str(ColorRampValues[2]))
    Intermediate1.setFont(QFont('MS Shell Dlg 2',12))
    Intermediate1.setFontColor(QColor(23,111,176))
    Intermediate1.adjustSizeToText()
    Intermediate1.setHAlign(Qt.Qt.AlignLeft)
    layout.addLayoutItem(Intermediate1)
    Intermediate1.attemptMove(QgsLayoutPoint(130.3,58, QgsUnitTypes.LayoutMillimeters))
    
    Intermediate1 = QgsLayoutItemLabel(layout)
    Intermediate1.setText(str(ColorRampValues[1]))
    Intermediate1.setFont(QFont('MS Shell Dlg 2',12))
    Intermediate1.setFontColor(QColor(23,111,176))
    Intermediate1.adjustSizeToText()
    Intermediate1.setHAlign(Qt.Qt.AlignLeft)
    layout.addLayoutItem(Intermediate1)
    Intermediate1.attemptMove(QgsLayoutPoint(130.3,78.4, QgsUnitTypes.LayoutMillimeters))

    ###Title###
    title = QgsLayoutItemLabel(layout)
    title.setText(MapTitle)
    title.setFont(QFont('Arial', 20))
    title.setFontColor(QColor(23,111,176))
    title.adjustSizeToText()
    title.setHAlign(Qt.Qt.AlignCenter)
    layout.addLayoutItem(title)
    title.attemptResize(QgsLayoutSize(119,15, QgsUnitTypes.LayoutMillimeters))
    title.attemptMove(QgsLayoutPoint(0,0, QgsUnitTypes.LayoutMillimeters))

    #############################################################
    #Print layout to image or pdf
    #############################################################
    exporter = QgsLayoutExporter(layout)

    #export_path_pdf = r"C:\Users\stoop_go\OneDrive - Stichting Deltares\Documents\QGIS projects\F1-Bulletin map\F1-Bulletin-map.pdf"
    export_path_png = r"/usr/src/app/Bulletin/A3_{}.png".format(mapVariable)
    #exporter.exportToPdf(export_path_pdf, QgsLayoutExporter.PdfExportSettings())
    exporter.exportToImage(export_path_png, QgsLayoutExporter.ImageExportSettings())

    return print(mapVariable)

Variables = ["chl", "botsalt", "bottemp", "oxy", "resup", "ssi"]

for mapVariable in Variables:
    makeMap(mapVariable)
    
print("All done")

###################################################################
###################################################################
#End of project
###################################################################
###################################################################

#Remove provider and layer registries from memory
qgs.exitQgis()