# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/Scaleform/daapi/view/meta/RallyMainWindowWithSearchMeta.py
from gui.Scaleform.daapi.view.lobby.rally.BaseRallyMainWindow import BaseRallyMainWindow

class RallyMainWindowWithSearchMeta(BaseRallyMainWindow):
    """
    DO NOT MODIFY!
    Generated with yaml.
    __author__ = 'yaml_processor'
    @extends BaseRallyMainWindow
    null
    """

    def onAutoMatch(self, value, values):
        """
        :param value:
        :param values:
        :return :
        """
        self._printOverrideError('onAutoMatch')

    def autoSearchApply(self, value):
        """
        :param value:
        :return :
        """
        self._printOverrideError('autoSearchApply')

    def autoSearchCancel(self, value):
        """
        :param value:
        :return :
        """
        self._printOverrideError('autoSearchCancel')

    def as_autoSearchEnableBtnS(self, value):
        """
        :param value:
        :return :
        """
        return self.flashObject.as_autoSearchEnableBtn(value) if self._isDAAPIInited() else None

    def as_changeAutoSearchStateS(self, value):
        """
        :param value:
        :return :
        """
        return self.flashObject.as_changeAutoSearchState(value) if self._isDAAPIInited() else None

    def as_changeAutoSearchBtnsStateS(self, waitingPlayers, searchEnemy):
        """
        :param waitingPlayers:
        :param searchEnemy:
        :return :
        """
        return self.flashObject.as_changeAutoSearchBtnsState(waitingPlayers, searchEnemy) if self._isDAAPIInited() else None

    def as_hideAutoSearchS(self):
        """
        :return :
        """
        return self.flashObject.as_hideAutoSearch() if self._isDAAPIInited() else None