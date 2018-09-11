# -*- coding: utf-8 -*-

"""
***************************************************************************
    GdalAlgorithmDialog.py
    ---------------------
    Date                 : May 2015
    Copyright            : (C) 2015 by Victor Olaya
    Email                : volayaf at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""

__author__ = 'Victor Olaya'
__date__ = 'May 2015'
__copyright__ = '(C) 2015, Victor Olaya'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtWidgets import (QWidget,
                                 QVBoxLayout,
                                 QHBoxLayout,
                                 QPushButton,
                                 QLabel,
                                 QPlainTextEdit,
                                 QLineEdit,
                                 QComboBox,
                                 QListWidget,
                                 QCheckBox,
                                 QSizePolicy,
                                 QDialogButtonBox)

from qgis.core import (Qgis,
                       QgsProcessingFeedback,
                       QgsProcessingParameterDefinition,
                       QgsProject,
                       QgsMessageLog)
from qgis.gui import (QgsMessageBar,
                      QgsProjectionSelectionWidget,
                      QgsProcessingAlgorithmDialogBase)

from processing.gui.AlgorithmDialog import AlgorithmDialog
from processing.gui.AlgorithmDialogBase import AlgorithmDialogBase
from processing.gui.ParametersPanel import ParametersPanel
from processing.gui.MultipleInputPanel import MultipleInputPanel
from processing.gui.NumberInputPanel import NumberInputPanel
from processing.gui.DestinationSelectionPanel import DestinationSelectionPanel
from processing.tools.dataobjects import createContext


class PdfAlgorithmDialog(AlgorithmDialog):

    def __init__(self, alg):
        super().__init__(alg)

    def getParametersPanel(self, alg, parent):
        return PdfParametersPanel(parent, alg)

    def accept(self):
        if not self.mainWidget().validate():
            self.messageBar().pushMessage("", "You must have the same number of template layers than override layers",level=Qgis.Warning, duration=5)
        else:
            return super().accept()

class PdfParametersPanel(ParametersPanel):

    def __init__(self, parent, alg):
        super().__init__(parent, alg)

        # assign widgets
        self.project_path_widget = self.layoutMain.itemAt(1).widget()
        self.layout_name_widget = self.layoutMain.itemAt(3).widget()
        self.template_layers_widget = self.layoutMain.itemAt(5).widget()
        self.override_layers_widget = self.layoutMain.itemAt(7).widget()

        # feedback widget
        self.feedback_label = QLabel("...")
        self.layoutMain.addWidget(self.feedback_label)

        # inject helpers widgets
        self.layouts_combobox = QComboBox()
        self.inject_helper_widget(self.layout_name_widget, self.layouts_combobox)

        self.template_list = QListWidget()
        self.template_list.setSelectionMode(QListWidget.MultiSelection)
        self.inject_helper_widget(self.template_layers_widget, self.template_list, hide=True)

        # initialize
        self.project_path_changed()

        # connect signals
        self.project_path_widget.leText.textChanged.connect(self.project_path_changed)
        self.layouts_combobox.activated[str].connect(self.layouts_combobox_activated)
        self.template_list.itemSelectionChanged.connect(self.template_list_selection_changed)
        
        self.project_path_widget.leText.textChanged.connect(self.validate)
        self.layout_name_widget.textChanged.connect(self.validate)
        self.template_layers_widget.textChanged.connect(self.validate)
        self.override_layers_widget.selectionChanged.connect(self.validate)

    def inject_helper_widget(self, widget, helper_widget, hide=False):
        """
        Helper to add a widget to the right of an existing widget (e.g. to add a button)
        """
        hboxwidget = QWidget()
        hboxwidget.setLayout(QHBoxLayout())
        hboxwidget.layout().setContentsMargins(0,0,0,0)
        self.layoutMain.replaceWidget(widget, hboxwidget)
        hboxwidget.layout().addWidget(widget)
        hboxwidget.layout().addWidget(helper_widget)
        if hide:
            widget.hide()

    def project_path_changed(self):
        project_path = self.project_path_widget.getValue()
        if project_path:
            self.project_instance = QgsProject()
            self.project_instance.read(project_path)
        else:
            self.project_instance = QgsProject.instance()

        # repopulate the layouts dropdown
        layout_manager = self.project_instance.layoutManager()
        self.layouts_combobox.clear()
        for layout in layout_manager.layouts():
            self.layouts_combobox.addItem(layout.name())

        # repopulate the template layers
        layer_ids = self.project_instance.mapLayers()
        self.template_list.clear()
        for layer_id in layer_ids:
            self.template_list.addItem(layer_id)

    def layouts_combobox_activated(self, text):
        self.layout_name_widget.setText(text)

    def template_list_selection_changed(self):
        layers_ids = [item.text() for item in self.template_list.selectedItems()]
        self.template_layers_widget.setText(','.join(layers_ids))

    def validate(self):
        template_layers_count = len(self.template_layers_widget.text().split(',')) if self.template_layers_widget.text() else 0
        override_layers_count = len(self.override_layers_widget.selectedoptions)
        return template_layers_count == override_layers_count
