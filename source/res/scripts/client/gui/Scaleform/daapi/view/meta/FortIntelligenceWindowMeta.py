# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/FortIntelligenceWindowMeta.py
from gui.Scaleform.framework.entities.abstract.AbstractWindowView import AbstractWindowView

class FortIntelligenceWindowMeta(AbstractWindowView):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends AbstractWindowView
    null
    """

    def requestClanFortInfo(self, index):
        """
        :param index:
        :return :
        """
        self._printOverrideError('requestClanFortInfo')

    def as_setStatusTextS(self, statusText):
        """
        :param statusText:
        :return :
        """
        return self.flashObject.as_setStatusText(statusText) if self._isDAAPIInited() else None

    def as_getSearchDPS(self):
        """
        :return Object:
        """
        return self.flashObject.as_getSearchDP() if self._isDAAPIInited() else None

    def as_getCurrentListIndexS(self):
        """
        :return int:
        """
        return self.flashObject.as_getCurrentListIndex() if self._isDAAPIInited() else None

    def as_selectByIndexS(self, index):
        """
        :param index:
        :return :
        """
        return self.flashObject.as_selectByIndex(index) if self._isDAAPIInited() else None

    def as_setTableHeaderS(self, data):
        """
        :param data:
        :return :
        """
        return self.flashObject.as_setTableHeader(data) if self._isDAAPIInited() else None