# -*- coding: utf-8 -*-

# This file is part of 'hamster-gtk'.
#
# 'hamster-gtk' is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# 'hamster-gtk' is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with 'hamster-gtk'.  If not, see <http://www.gnu.org/licenses/>.


"""This Module provides the ``ExportDialog`` class to choose file to be exported."""

from __future__ import absolute_import

import os.path
from enum import Enum
from gettext import gettext as _

from gi.repository import Gtk

ExportType = Enum('ExportType', ('CSV', 'ICAL', 'XML'))


class ExportDialog(Gtk.FileChooserDialog):
    """Dialog used for exporting."""

    def __init__(self, parent):
        """
        Initialize headerbar.

        Args:
            parent (Gtk.Window): Parent window for the dialog.
        """
        super(ExportDialog, self).__init__(_("Please Choose where to export to"), parent,
            Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        self._export_type_chooser = Gtk.ComboBoxText()
        self._export_type_chooser.append(str(ExportType.CSV), _("CSV"))
        self._export_type_chooser.append(str(ExportType.ICAL), _("iCal"))
        self._export_type_chooser.append(str(ExportType.XML), _("XML"))
        self._export_type_chooser.connect('changed', self._export_type_changed)

        export_type_label = Gtk.Label(_("Export as file _type:"))
        export_type_label.set_use_underline(True)
        export_type_label.set_mnemonic_widget(self._export_type_chooser)

        export_options = Gtk.Grid()
        export_options.attach(export_type_label, 0, 0, 1, 1)
        export_options.attach_next_to(self._export_type_chooser, export_type_label,
                                      Gtk.PositionType.RIGHT, 1, 1)
        export_options.show_all()
        self.set_extra_widget(export_options)

        self.set_current_name(_("hamster_export"))
        self._export_type_chooser.set_active_id(str(ExportType.CSV))

    def _export_type_changed(self, combobox):
        """
        Change file extension of the selected file to the one that was chosen.

        Args:
            combobox (Gtk.ComboBoxText): Combo box that was changed.
        """
        new_type = self.get_export_type()

        if new_type == ExportType.CSV:
            new_ext = 'csv'
        elif new_type == ExportType.ICAL:
            new_ext = 'ical'
        elif new_type == ExportType.XML:
            new_ext = 'xml'

        (name, ext) = os.path.splitext(self.get_current_name())
        self.set_current_name('{}.{}'.format(name, new_ext))

    def get_export_type(self):
        """
        Return currently selected export type.

        GTK only allows string IDs, so the ID has to be transformed into enum.

        Returns:
            ExportType: Currently selected export type.

        Raises:
            ValueError: When the type does not match any enum value.
        """
        active_type = self._export_type_chooser.get_active_id()
        for val in ExportType:
            if active_type == str(val):
                return val

        raise ValueError('Unknown export type.')
