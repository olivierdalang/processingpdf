# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ProcessingPDF
                                 A QGIS plugin
 Allow to export PDFs from Processing
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-09-10
        copyright            : (C) 2018 by Olivier Dalang / SPC
        email                : olivier.dalang@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Olivier Dalang / SPC'
__date__ = '2018-09-10'
__copyright__ = '(C) 2018 by Olivier Dalang / SPC'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from PyQt5.QtCore import QCoreApplication, QFile
from PyQt5.QtXml import QDomDocument
from qgis.core import (QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFile ,
                       QgsProcessingParameterFolderDestination,
                       QgsReadWriteContext)
from qgis.core import *

import os.path


class ProcessingPDFAlgorithm(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    OUTPUT_FOLDER = 'OUTPUT_FOLDER'
    LAYOUT_FILE = 'LAYOUT_FILE'

    def initAlgorithm(self, config):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        self.addParameter(
            QgsProcessingParameterFile (
                self.LAYOUT_FILE,
                self.tr('Input layout'),
                behavior=QgsProcessingParameterFile.File,
                extension='qpt',
            )
        )

        self.addParameter(
            QgsProcessingParameterFile(
                self.OUTPUT_FOLDER,
                self.tr('Output folder'),
                behavior=QgsProcessingParameterFile.Folder,
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        input_layout = self.parameterAsFile(parameters, self.LAYOUT_FILE, context)
        output_folder = self.parameterAsFile(parameters, self.OUTPUT_FOLDER, context)

        output_file = os.path.join(output_folder, 'test.pdf')

        dom_document = QDomDocument()
        dom_document.setContent( QFile(input_layout) )

        project_instance = QgsProject.instance()

        layout = QgsLayout(project_instance)
        layout.loadFromTemplate(dom_document, context=QgsReadWriteContext())

        # layout_manager = project_instance.layoutManager()
        # layout_item = layout_manager.layoutByName("test")  # test is the layout name

        export = QgsLayoutExporter(layout)
        export.exportToPdf(output_file, QgsLayoutExporter.PdfExportSettings())

        return {}

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Export template to PDF'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'PDF Exports'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ProcessingPDFAlgorithm()