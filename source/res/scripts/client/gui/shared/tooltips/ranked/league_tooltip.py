# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/shared/tooltips/ranked/league_tooltip.py
from gui.shared.formatters import text_styles
from gui.shared.tooltips import TOOLTIP_TYPE, formatters
from gui.shared.tooltips.common import BlocksTooltipData
from gui.impl import backport
from gui.impl.gen import R
from helpers import dependency
from gui.ranked_battles import ranked_formatters
from skeletons.gui.game_control import IRankedBattlesController
from gui.Scaleform.genConsts.BLOCKS_TOOLTIP_TYPES import BLOCKS_TOOLTIP_TYPES
from gui.ranked_battles.ranked_helpers.league_provider import UNDEFINED_LEAGUE_ID

class BonusTooltipData(BlocksTooltipData):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, context):
        super(BonusTooltipData, self).__init__(context, TOOLTIP_TYPE.RANKED_RANK)
        self._setContentMargin(bottom=14)
        self._setMargins(14, 20)
        self._setWidth(330)

    def _packBlocks(self, *args, **kwargs):
        items = super(BonusTooltipData, self)._packBlocks()
        headerBlocks = [formatters.packImageTextBlockData(title=text_styles.highTitle(backport.text(R.strings.tooltips.battleTypes.ranked.bonusBattle.title())), img=backport.image(R.images.gui.maps.icons.rankedBattles.bonusIcons.c_48x48()), txtPadding=formatters.packPadding(left=20), titleAtMiddle=True, padding=formatters.packPadding(left=30, top=14))]
        items.append(formatters.packBuildUpBlockData(headerBlocks, stretchBg=False, linkage=BLOCKS_TOOLTIP_TYPES.TOOLTIP_BUILDUP_BLOCK_NORMAL_VEHICLE_BG_LINKAGE, padding=formatters.packPadding(left=-20, top=-12, bottom=-6)))
        bonusBattlesValue = self.rankedController.getClientBonusBattlesCount()
        bonusCountName = backport.text(R.strings.tooltips.battleTypes.ranked.bonusBattle.count())
        items.append(formatters.packTextParameterBlockData(name=text_styles.main(bonusCountName), value=text_styles.stats(bonusBattlesValue), padding=formatters.packPadding(top=-8, left=20, bottom=0)))
        descriptionBlock = [formatters.packTextBlockData(text_styles.main(backport.text(R.strings.tooltips.battleTypes.ranked.bonusBattle.description())), padding=formatters.packPadding(top=-10))]
        items.append(formatters.packBuildUpBlockData(descriptionBlock, linkage=BLOCKS_TOOLTIP_TYPES.TOOLTIP_BUILDUP_BLOCK_WHITE_BG_LINKAGE))
        return items


class LeagueTooltipData(BlocksTooltipData):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, context):
        super(LeagueTooltipData, self).__init__(context, TOOLTIP_TYPE.RANKED_RANK)
        self._setContentMargin(bottom=14)
        self._setMargins(14, 20)
        self._setWidth(330)

    def _packBlocks(self, *args, **kwargs):
        items = super(LeagueTooltipData, self)._packBlocks()
        webLeague = self.rankedController.getClientLeague()
        if webLeague.league != UNDEFINED_LEAGUE_ID and webLeague.position is not None:
            title = backport.text(R.strings.ranked_battles.rankedBattleMainView.leaguesView.dyn('league{}'.format(webLeague.league))())
            description = backport.text(R.strings.ranked_battles.rankedBattleMainView.leaguesView.descr())
        else:
            title = backport.text(R.strings.ranked_battles.rankedBattleMainView.leaguesView.unavailableTitle())
            description = backport.text(R.strings.ranked_battles.rankedBattleMainView.leaguesView.unavailableDescr())
        items.append(formatters.packTitleDescBlock(title=text_styles.highTitle(title), desc=text_styles.main(description)))
        return items


class EfficiencyTooltipData(BlocksTooltipData):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, context):
        super(EfficiencyTooltipData, self).__init__(context, TOOLTIP_TYPE.RANKED_RANK)
        self._setContentMargin(bottom=14)
        self._setMargins(14, 20)
        self._setWidth(330)

    def _packBlocks(self, *args, **kwargs):
        items = super(EfficiencyTooltipData, self)._packBlocks()
        items.append(formatters.packTextBlockData(text_styles.highTitle(backport.text(R.strings.tooltips.ranked.widget.efficiency.title()))))
        efficiencyBlocks = []
        statsComposer = self.rankedController.getStatsComposer()
        currEff, currUpdateTime = statsComposer.currentSeasonEfficiency
        efficiencyBlocks.append(self.__getEfficiencyBlock(currEff, currUpdateTime, R.strings.tooltips.ranked.widget.efficiency.currentUpdate()))
        prevEff, prevUpdateTime = statsComposer.cachedSeasonEfficiency
        efficiencyBlocks.append(self.__getEfficiencyBlock(prevEff, prevUpdateTime, R.strings.tooltips.ranked.widget.efficiency.previousUpdate()))
        items.append(formatters.packBuildUpBlockData(efficiencyBlocks, linkage=BLOCKS_TOOLTIP_TYPES.TOOLTIP_BUILDUP_BLOCK_WHITE_BG_LINKAGE, padding=formatters.packPadding(left=60, top=-8, bottom=-8)))
        items.append(formatters.packTextBlockData(text_styles.main(backport.text(R.strings.tooltips.ranked.widget.efficiency.description()))))
        return items

    def __getEfficiencyBlock(self, efficiency, updateTime, resID):
        text = text_styles.main(backport.text(resID)).format(value=text_styles.stats(ranked_formatters.getFloatPercentStrStat(efficiency)), date=text_styles.standard(backport.getShortDateFormat(updateTime)), time=text_styles.standard(backport.getShortTimeFormat(updateTime)))
        return formatters.packTextBlockData(text)


class PositionTooltipData(BlocksTooltipData):
    rankedController = dependency.descriptor(IRankedBattlesController)

    def __init__(self, context):
        super(PositionTooltipData, self).__init__(context, TOOLTIP_TYPE.RANKED_RANK)
        self._setContentMargin(bottom=14)
        self._setMargins(14, 20)
        self._setWidth(330)

    def _packBlocks(self, *args, **kwargs):
        items = super(PositionTooltipData, self)._packBlocks()
        title = text_styles.highTitle(backport.text(R.strings.tooltips.ranked.widget.position.title()))
        updateTime = self.rankedController.getClientLeagueUpdateTime()
        items.append(formatters.packTitleDescBlock(title=title, desc=text_styles.main(backport.text(R.strings.tooltips.ranked.widget.position.description()).format(date=text_styles.neutral(ranked_formatters.getTimeLongStr(updateTime))))))
        posComment = R.strings.tooltips.ranked.widget.position
        items.append(formatters.packTextBlockData(text_styles.standard(backport.text(posComment.updateLabel() if updateTime is not None else posComment.unavailableLabel()))))
        return items
