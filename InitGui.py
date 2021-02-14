# Inspect stylesheet for FreeCAD
# Copyright (C) Nauck @ FreeCAD
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA


def single_instance():
    import FreeCADGui as Gui
    from PySide2 import QtWidgets

    window = Gui.getMainWindow()
    if window:
        for i in window.findChildren(QtWidgets.QDockWidget):
            if i.objectName() == "InspectWidgets":
                i.deleteLater()
            else:
                pass
    else:
        pass


single_instance()


def dock_widget():
    import FreeCADGui as Gui
    from PySide2 import QtGui, QtCore, QtWidgets
    from PySide2.QtUiTools import QUiLoader
    from typing import Optional
    from utils import utils
    import os

    loader = QUiLoader(None)
    mod_path = utils.get_mod_path()
    widget_path = os.path.join(mod_path, 'ui', 'dockwidget.ui')
    widget: QtWidgets.QDockWidget = loader.load(widget_path)
    inspect_button: QtWidgets.QPushButton = widget.inspectButton
    identifier_label: QtWidgets.QLabel = widget.identifierLabel
    path_label: QtWidgets.QLabel = widget.pathLabel
    style_sheet_text: QtWidgets.QPlainTextEdit = widget.styleSheetText
    timer = QtCore.QTimer(widget)

    window = Gui.getMainWindow()
    def prettify_qss(qss):
        qss = str.replace(qss, ';', ';\n')
        qss = str.replace(qss, '{', '{\n')
        qss = str.replace(qss, '}', '}\n')
        items: list[str] = str.split(qss, '\n')
        items[:] = ['  ' + i if ';' in i else i for i in items]
        return '\n'.join(items)

    def get_meta_object(w) -> QtCore.QMetaObject:
        return w.metaObject()

    def get_class_name(meta_object) -> str:
        return meta_object.className().replace('::', '--')

    def sample():
        try:
            # use shift to cancel
            if QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.ShiftModifier:
                inspect_button.click()

            w: Optional[QtWidgets.QWidget] = QtWidgets.QApplication.widgetAt(QtGui.QCursor.pos())
            if not w:
                identifier_label.setText('')
                style_sheet_text.setPlainText('')
                path_label.setText('')
                return
            meta_obj = get_meta_object(w)
            class_name = get_class_name(meta_obj)

            object_name = w.objectName() if hasattr(w, 'objectName') else ''
            properties = []
            accessible_name = w.accessibleName()
            if accessible_name:
                properties.append('accessibleName="' + accessible_name + '"')
            classes = w.property('class')
            if classes:
                properties.append('class="' + str(classes) + '"')
            identifier = class_name
            identifier = identifier +\
                         ('#' + object_name if object_name else '') +\
                         ('[' + ', '.join(properties) + ']' if properties else '')

            parents = []
            while meta_obj:
                parents.append(meta_obj.className().replace('::', '--'))
                meta_obj = meta_obj.superClass()
            if parents:
                identifier = identifier + '\n' + ' -> '.join(parents)
            identifier_label.setText(identifier)

            path = []
            style_sheet_text.setPlainText(prettify_qss(w.styleSheet()))
            while not w.isTopLevel() and w is not window:
                path.append(get_class_name(get_meta_object(w)))
                w = w.parent()
            path.reverse()
            path_label.setText(' > '.join(path))
        except:
            pass
    timer.timeout.connect(sample)

    def clicked():
        if inspect_button.isChecked():
            timer.start(200)
        else:
            timer.stop()

    inspect_button.clicked.connect(clicked)

    if window:
        window.addDockWidget(QtCore.Qt.LeftDockWidgetArea, widget)


dock_widget()
