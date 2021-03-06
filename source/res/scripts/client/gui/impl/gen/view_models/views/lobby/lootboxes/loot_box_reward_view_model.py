# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/impl/gen/view_models/views/lobby/lootboxes/loot_box_reward_view_model.py
from frameworks.wulf import Array
from frameworks.wulf import ViewModel

class LootBoxRewardViewModel(ViewModel):
    __slots__ = ('onCloseBtnClick', 'onNextBtnClick', 'onVideoChangeClick', 'onCloseEvent', 'onDestroyEvent', 'onVideoStarted', 'onVideoStopped', 'onReadyToRestart', 'showSpecialReward', 'onBuyBoxBtnClick', 'onSpecialActionBtnClick')

    def __init__(self, properties=12, commands=11):
        super(LootBoxRewardViewModel, self).__init__(properties=properties, commands=commands)

    def getIsVideoOff(self):
        return self._getBool(0)

    def setIsVideoOff(self, value):
        self._setBool(0, value)

    def getLeftLootBoxes(self):
        return self._getNumber(1)

    def setLeftLootBoxes(self, value):
        self._setNumber(1, value)

    def getBoxType(self):
        return self._getString(2)

    def setBoxType(self, value):
        self._setString(2, value)

    def getBoxCategory(self):
        return self._getString(3)

    def setBoxCategory(self, value):
        self._setString(3, value)

    def getIsFreeBox(self):
        return self._getBool(4)

    def setIsFreeBox(self, value):
        self._setBool(4, value)

    def getFadeOut(self):
        return self._getBool(5)

    def setFadeOut(self, value):
        self._setBool(5, value)

    def getIsReload(self):
        return self._getBool(6)

    def setIsReload(self, value):
        self._setBool(6, value)

    def getRewards(self):
        return self._getArray(7)

    def setRewards(self, value):
        self._setArray(7, value)

    def getIsNextBtnEnabled(self):
        return self._getBool(8)

    def setIsNextBtnEnabled(self, value):
        self._setBool(8, value)

    def getIsGiftBuyBtnVisible(self):
        return self._getBool(9)

    def setIsGiftBuyBtnVisible(self, value):
        self._setBool(9, value)

    def getHardReset(self):
        return self._getBool(10)

    def setHardReset(self, value):
        self._setBool(10, value)

    def getSpecialRewardType(self):
        return self._getString(11)

    def setSpecialRewardType(self, value):
        self._setString(11, value)

    def _initialize(self):
        super(LootBoxRewardViewModel, self)._initialize()
        self._addBoolProperty('isVideoOff', False)
        self._addNumberProperty('leftLootBoxes', 0)
        self._addStringProperty('boxType', '')
        self._addStringProperty('boxCategory', '')
        self._addBoolProperty('isFreeBox', False)
        self._addBoolProperty('fadeOut', False)
        self._addBoolProperty('isReload', False)
        self._addArrayProperty('rewards', Array())
        self._addBoolProperty('isNextBtnEnabled', True)
        self._addBoolProperty('isGiftBuyBtnVisible', True)
        self._addBoolProperty('hardReset', False)
        self._addStringProperty('specialRewardType', '')
        self.onCloseBtnClick = self._addCommand('onCloseBtnClick')
        self.onNextBtnClick = self._addCommand('onNextBtnClick')
        self.onVideoChangeClick = self._addCommand('onVideoChangeClick')
        self.onCloseEvent = self._addCommand('onCloseEvent')
        self.onDestroyEvent = self._addCommand('onDestroyEvent')
        self.onVideoStarted = self._addCommand('onVideoStarted')
        self.onVideoStopped = self._addCommand('onVideoStopped')
        self.onReadyToRestart = self._addCommand('onReadyToRestart')
        self.showSpecialReward = self._addCommand('showSpecialReward')
        self.onBuyBoxBtnClick = self._addCommand('onBuyBoxBtnClick')
        self.onSpecialActionBtnClick = self._addCommand('onSpecialActionBtnClick')
