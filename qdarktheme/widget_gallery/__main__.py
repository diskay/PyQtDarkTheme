# ---------------------------------------------------------------------------------------------
#  Copyright (c) Yunosuke Ohsugi. All rights reserved.
#  Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------*/

import sys

import qdarktheme
from qdarktheme.qtpy.QtCore import Qt, Slot
from qdarktheme.qtpy.QtWidgets import QApplication, QColorDialog, QFileDialog, QMainWindow
from qdarktheme.widget_gallery.ui.main_ui import UI


class WidgetGallery(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self._ui = UI()
        self._ui.setup_ui(self)
        self._setup()

    def _setup(self) -> None:
        self._ui.action_change_home.triggered.connect(self._change_page)
        self._ui.action_change_dock.triggered.connect(self._change_page)
        self._ui.action_open_folder.triggered.connect(
            lambda: QFileDialog.getOpenFileName(self, "Open File", options=QFileDialog.Option.DontUseNativeDialog)
        )
        self._ui.action_open_color_dialog.triggered.connect(
            lambda: QColorDialog.getColor(parent=self, options=QColorDialog.ColorDialogOption.DontUseNativeDialog)
        )
        self._ui.action_enable.triggered.connect(self._toggle_state)
        self._ui.action_disable.triggered.connect(self._toggle_state)
        for action in self._ui.actions_theme:
            action.triggered.connect(self._change_theme)

    @Slot()
    def _change_page(self) -> None:
        action_name = self.sender().text()
        self._ui.stack_widget.setCurrentIndex(0 if action_name == "Move to home" else 1)

    @Slot()
    def _toggle_state(self) -> None:
        state = self.sender().text()
        self._ui.central_window.centralWidget().setEnabled(state == "Enable")
        self._ui.action_enable.setEnabled(state == "Disable")
        self._ui.action_disable.setEnabled(state == "Enable")
        self.statusBar().showMessage(state)

    @Slot()
    def _change_theme(self) -> None:
        theme = self.sender().text()
        QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet(theme))


app = QApplication(sys.argv)
# Fix the svg icon display becoming low quality in Qt5.
# PyQt6 doesn't have attribute AA_UseHighDpiPixmaps.
if hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
win = WidgetGallery()
win.menuBar().setNativeMenuBar(False)
app.setStyleSheet(qdarktheme.load_stylesheet())
win.show()
app.exec()
