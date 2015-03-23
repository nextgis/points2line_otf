# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Points2LineOTF
                                 A QGIS plugin
 On-the-fly tool for convert points to line
                             -------------------
        begin                : 2015-03-23
        copyright            : (C) 2015 by NextGIS

        email                : info@nextgis.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Points2LineOTF class from file Points2LineOTF.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .points_2_line_otf import Points2LineOTF
    return Points2LineOTF(iface)
