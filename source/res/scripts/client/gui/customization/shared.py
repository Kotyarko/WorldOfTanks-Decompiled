# Python bytecode 2.7 (decompiled from Python 2.7)
# Embedded file name: scripts/client/gui/customization/shared.py
from collections import namedtuple, Counter
import logging
import Math
from gui.Scaleform.daapi.view.lobby.store.browser.ingameshop_helpers import isIngameShopEnabled
from gui.Scaleform.daapi.view.dialogs.ExchangeDialogMeta import InfoItemBase
from gui.Scaleform.genConsts.SEASONS_CONSTANTS import SEASONS_CONSTANTS
from gui.shared.gui_items import GUI_ITEM_TYPE, GUI_ITEM_TYPE_NAMES
from gui.shared.gui_items.gui_item_economics import ITEM_PRICE_EMPTY
from gui.shared.money import Currency, ZERO_MONEY
from items.components.c11n_constants import CustomizationType, C11N_MASK_REGION, MAX_USERS_PROJECTION_DECALS, ProjectionDecalFormTags, SeasonType, ApplyArea, C11N_GUN_APPLY_REGIONS
from shared_utils import CONST_CONTAINER, isEmpty
from skeletons.gui.shared import IItemsCache
from vehicle_systems.tankStructure import TankPartIndexes, TankPartNames
from CurrentVehicle import g_currentVehicle
from gui.shared.utils.requesters import REQ_CRITERIA
from gui.shared.gui_items.customization.outfit import Area, scaffold
from gui.shared.gui_items.customization.slots import SLOT_TYPE_TO_ANCHOR_TYPE_MAP
from gui.impl import backport
from gui.impl.gen import R
from helpers import dependency
_logger = logging.getLogger(__name__)
C11nId = namedtuple('C11nId', ('areaId', 'slotType', 'regionIdx'))
C11nId.__new__.__defaults__ = (-1, -1, -1)
C11N_ITEM_TYPE_MAP = {GUI_ITEM_TYPE.PAINT: CustomizationType.PAINT,
 GUI_ITEM_TYPE.CAMOUFLAGE: CustomizationType.CAMOUFLAGE,
 GUI_ITEM_TYPE.MODIFICATION: CustomizationType.MODIFICATION,
 GUI_ITEM_TYPE.DECAL: CustomizationType.DECAL,
 GUI_ITEM_TYPE.EMBLEM: CustomizationType.DECAL,
 GUI_ITEM_TYPE.INSCRIPTION: CustomizationType.DECAL,
 GUI_ITEM_TYPE.PERSONAL_NUMBER: CustomizationType.PERSONAL_NUMBER,
 GUI_ITEM_TYPE.STYLE: CustomizationType.STYLE,
 GUI_ITEM_TYPE.PROJECTION_DECAL: CustomizationType.PROJECTION_DECAL}

class PurchaseItem(object):
    __slots__ = ('item', 'price', 'areaID', 'slot', 'regionID', 'selected', 'group', 'isFromInventory', 'isDismantling', 'component')

    def __init__(self, item, price, areaID, slot, regionID, selected, group, isFromInventory=False, isDismantling=False, component=None):
        self.item = item
        self.price = price
        self.areaID = areaID
        self.slot = slot
        self.regionID = regionID
        self.selected = selected
        self.group = group
        self.isFromInventory = isFromInventory
        self.isDismantling = isDismantling
        self.component = component


class HighlightingMode(CONST_CONTAINER):
    PAINT_REGIONS = 0
    CAMO_REGIONS = 1
    WHOLE_VEHICLE = 2
    REPAINT_REGIONS_MERGED = 3
    CAMO_REGIONS_SKIP_TURRET = 4


MODE_TO_C11N_TYPE = {HighlightingMode.PAINT_REGIONS: GUI_ITEM_TYPE.PAINT,
 HighlightingMode.REPAINT_REGIONS_MERGED: GUI_ITEM_TYPE.PAINT,
 HighlightingMode.CAMO_REGIONS: GUI_ITEM_TYPE.CAMOUFLAGE,
 HighlightingMode.WHOLE_VEHICLE: GUI_ITEM_TYPE.STYLE,
 HighlightingMode.CAMO_REGIONS_SKIP_TURRET: GUI_ITEM_TYPE.CAMOUFLAGE}
REGIONS_BY_AREA_ID = {Area.CHASSIS: ApplyArea.CHASSIS_REGIONS,
 Area.HULL: ApplyArea.HULL_REGIONS,
 Area.TURRET: ApplyArea.TURRET_REGIONS,
 Area.GUN: ApplyArea.GUN_REGIONS}
AREA_ID_BY_REGION = {region:areaId for areaId, regions in REGIONS_BY_AREA_ID.iteritems() for region in regions}
QUANTITY_LIMITED_CUSTOMIZATION_TYPES = {GUI_ITEM_TYPE.PROJECTION_DECAL: MAX_USERS_PROJECTION_DECALS}
PROJECTION_DECAL_IMAGE_FORM_TAG = {ProjectionDecalFormTags.SQUARE: backport.image(R.images.gui.maps.icons.customization.icon_form_1()),
 ProjectionDecalFormTags.RECT1X2: backport.image(R.images.gui.maps.icons.customization.icon_form_2()),
 ProjectionDecalFormTags.RECT1X3: backport.image(R.images.gui.maps.icons.customization.icon_form_3()),
 ProjectionDecalFormTags.RECT1X4: backport.image(R.images.gui.maps.icons.customization.icon_form_4()),
 ProjectionDecalFormTags.RECT1X6: backport.image(R.images.gui.maps.icons.customization.icon_form_6())}
PROJECTION_DECAL_TEXT_FORM_TAG = {ProjectionDecalFormTags.SQUARE: backport.text(R.strings.vehicle_customization.form.formfactor_square()),
 ProjectionDecalFormTags.RECT1X2: backport.text(R.strings.vehicle_customization.form.formfactor_rect1x2()),
 ProjectionDecalFormTags.RECT1X3: backport.text(R.strings.vehicle_customization.form.formfactor_rect1x3()),
 ProjectionDecalFormTags.RECT1X4: backport.text(R.strings.vehicle_customization.form.formfactor_rect1x4()),
 ProjectionDecalFormTags.RECT1X6: backport.text(R.strings.vehicle_customization.form.formfactor_rect1x6())}
PROJECTION_DECAL_FORM_TO_UI_ID = {ProjectionDecalFormTags.SQUARE: 1,
 ProjectionDecalFormTags.RECT1X2: 2,
 ProjectionDecalFormTags.RECT1X3: 3,
 ProjectionDecalFormTags.RECT1X4: 4,
 ProjectionDecalFormTags.RECT1X6: 6}
SEASON_IDX_TO_TYPE = {SEASONS_CONSTANTS.SUMMER_INDEX: SeasonType.SUMMER,
 SEASONS_CONSTANTS.WINTER_INDEX: SeasonType.WINTER,
 SEASONS_CONSTANTS.DESERT_INDEX: SeasonType.DESERT}
SEASON_TYPE_TO_NAME = {SeasonType.SUMMER: SEASONS_CONSTANTS.SUMMER,
 SeasonType.WINTER: SEASONS_CONSTANTS.WINTER,
 SeasonType.DESERT: SEASONS_CONSTANTS.DESERT}
SEASON_TYPE_TO_IDX = {SeasonType.SUMMER: SEASONS_CONSTANTS.SUMMER_INDEX,
 SeasonType.WINTER: SEASONS_CONSTANTS.WINTER_INDEX,
 SeasonType.DESERT: SEASONS_CONSTANTS.DESERT_INDEX}
SEASONS_ORDER = (SeasonType.SUMMER, SeasonType.WINTER, SeasonType.DESERT)
CartInfo = namedtuple('CartInfo', 'totalPrice numSelected numApplying numBought numTotal isAtLeastOneItemFromInventory isAtLeastOneItemDismantled')

class MoneyForPurchase(object):
    NOT_ENOUGH = 0
    ENOUGH_WITH_EXCHANGE = 1
    ENOUGH = 2


class AdditionalPurchaseGroups(object):
    STYLES_GROUP_ID = -1
    UNASSIGNED_GROUP_ID = -2


class CartExchangeCreditsInfoItem(InfoItemBase):

    @property
    def itemTypeName(self):
        pass

    @property
    def userName(self):
        pass

    @property
    def itemTypeID(self):
        return GUI_ITEM_TYPE.CUSTOMIZATION

    def getExtraIconInfo(self):
        return None

    def getGUIEmblemID(self):
        pass


class CustomizationTankPartNames(TankPartNames):
    MASK = 'mask'
    ALL = TankPartNames.ALL + (MASK,)


def chooseMode(itemTypeID, vehicle):
    if itemTypeID == GUI_ITEM_TYPE.CAMOUFLAGE:
        if not __isTurretCustomizable(vehicle.descriptor):
            return HighlightingMode.CAMO_REGIONS_SKIP_TURRET
        return HighlightingMode.CAMO_REGIONS
    return HighlightingMode.REPAINT_REGIONS_MERGED if itemTypeID == GUI_ITEM_TYPE.PAINT else HighlightingMode.WHOLE_VEHICLE


def getAppliedRegionsForCurrentHangarVehicle(areaId, slotId):
    if not g_currentVehicle.isPresent():
        return ()
    else:
        outfit = g_currentVehicle.item.getCustomOutfit(SeasonType.SUMMER)
        area = outfit.getContainer(areaId)
        if area:
            slot = area.slotFor(slotId)
            if slot:
                if slotId in (GUI_ITEM_TYPE.INSCRIPTION, GUI_ITEM_TYPE.EMBLEM):
                    descriptor = g_currentVehicle.item.descriptor
                    allDecalesSlots = ()
                    if areaId == TankPartIndexes.HULL:
                        allDecalesSlots = descriptor.hull.emblemSlots + descriptor.hull.slotsAnchors
                    elif areaId == TankPartIndexes.TURRET and not descriptor.turret.showEmblemsOnGun or areaId == TankPartIndexes.GUN and descriptor.turret.showEmblemsOnGun:
                        allDecalesSlots = descriptor.turret.emblemSlots + descriptor.turret.slotsAnchors
                    slotType = SLOT_TYPE_TO_ANCHOR_TYPE_MAP.get(slotId, None)
                    if slotType is not None:
                        decalesSlots = tuple((slt for slt in allDecalesSlots if slt.type == slotType))
                        return tuple(range(min(len(decalesSlots), len(slot.getRegions()))))
                    _logger.warning('slotId=%d does not have matched value', slotId)
                    return ()
                if slotId in (GUI_ITEM_TYPE.PROJECTION_DECAL,):
                    return tuple(g_currentVehicle.item.getAnchors(slotId, Area.MISC))
                if slotId in (GUI_ITEM_TYPE.PAINT, GUI_ITEM_TYPE.CAMOUFLAGE):
                    customizableAreas = []
                    vehiclePart = getVehiclePartByIdx(g_currentVehicle.item, areaId)
                    if vehiclePart is not None:
                        if areaId == TankPartIndexes.GUN:
                            return tuple((C11N_GUN_APPLY_REGIONS[area] for area in vehiclePart.customizableVehicleAreas[GUI_ITEM_TYPE_NAMES[slotId]][1]))
                        customizableAreas = vehiclePart.customizableVehicleAreas[GUI_ITEM_TYPE_NAMES[slotId]][1]
                    return tuple(range(len(customizableAreas)))
                if slotId in (GUI_ITEM_TYPE.MODIFICATION,):
                    return (0,)
        return ()


def __isTurretCustomizable(vhicleDescriptor):
    return bool(ApplyArea.TURRET & vhicleDescriptor.turret.customizableVehicleAreas['camouflage'][0])


def getCustomizationTankPartName(areaId, regionIdx):
    return CustomizationTankPartNames.MASK if areaId == TankPartIndexes.GUN and regionIdx == C11N_MASK_REGION else TankPartIndexes.getName(areaId)


def createCustomizationBaseRequestCriteria(vehicle, progress, appliedItems, season=None, itemTypeID=None):
    season = season or SeasonType.ALL
    criteria = REQ_CRITERIA.CUSTOM(lambda item: (not itemTypeID or item.itemTypeID == itemTypeID) and item.season & season and (not item.requiredToken or progress.getTokenCount(item.requiredToken) > 0) and (item.buyCount > 0 or item.fullInventoryCount(vehicle) > 0 or appliedItems and item.intCD in appliedItems or item.getInstalledVehicles() and not item.isVehicleBound) and item.mayInstall(vehicle))
    return criteria


def isOutfitVisuallyEmpty(oufit):
    return isEmpty((item for item in oufit.items() if not item.isHiddenInUI()))


def fromWorldCoordsToHangarVehicle(worldCoords):
    compoundModel = g_currentVehicle.hangarSpace.space.getVehicleEntity().appearance.compoundModel
    modelMat = Math.Matrix(compoundModel.matrix)
    modelMat.invert()
    return modelMat.applyPoint(worldCoords)


def fromHangarVehicleToWorldCoords(hangarVehicleCoords):
    compoundModel = g_currentVehicle.hangarSpace.space.getVehicleEntity().appearance.compoundModel
    modelMatrix = Math.Matrix(compoundModel.matrix)
    return modelMatrix.applyPoint(hangarVehicleCoords)


def slotsIdsFromAppliedTo(appliedTo, slotType):
    st = scaffold()
    result = list()
    for region in ApplyArea.RANGE:
        if appliedTo & region:
            areaId = AREA_ID_BY_REGION[region]
            slot = st[areaId].slotFor(slotType)
            if slot is not None:
                regions = slot.getRegions()
                regionIdx = next((i for i, rg in enumerate(regions) if rg == region), -1)
                result.append((areaId, slotType, regionIdx))

    return result


def appliedToFromSlotsIds(slotsIds):
    st = scaffold()
    appliedTo = 0
    for slotId in slotsIds:
        areaId, slotType, regionIdx = slotId
        slot = st[areaId].slotFor(slotType)
        if slot is not None:
            regions = slot.getRegions()
            region = regions[regionIdx] if len(regions) > regionIdx else ApplyArea.NONE
            appliedTo |= region

    return appliedTo


def getVehiclePartByIdx(vehicle, partIdx):
    vehiclePart = None
    if partIdx == TankPartIndexes.CHASSIS:
        vehiclePart = vehicle.descriptor.chassis
    if partIdx == TankPartIndexes.TURRET:
        vehiclePart = vehicle.descriptor.turret
    if partIdx == TankPartIndexes.HULL:
        vehiclePart = vehicle.descriptor.hull
    if partIdx == TankPartIndexes.GUN:
        vehiclePart = vehicle.descriptor.gun
    return vehiclePart


def getTotalPurchaseInfo(purchaseItems):
    numSelectedItems = 0
    numApplyingItems = 0
    isAtLeastOneItemFromInventory = False
    isAtLeastOneItemDismantled = False
    itemCartInfo = {}
    for purchaseItem in purchaseItems:
        if purchaseItem.item is not None:
            itemCD = purchaseItem.item.intCD
            if itemCD not in itemCartInfo.keys():
                itemCartInfo.update({itemCD: {'totalPrice': ITEM_PRICE_EMPTY,
                          'quantity': 0}})
            if not purchaseItem.isDismantling:
                numApplyingItems += 1
                if purchaseItem.selected:
                    numSelectedItems += 1
                    itemCartInfo[itemCD]['totalPrice'] += purchaseItem.price
                    itemCartInfo[itemCD]['quantity'] += 1
                    if purchaseItem.isFromInventory:
                        isAtLeastOneItemFromInventory = True
                if purchaseItem.isFromInventory:
                    itemCartInfo[itemCD]['totalPrice'] -= purchaseItem.price
                    itemCartInfo[itemCD]['quantity'] -= 1
            else:
                isAtLeastOneItemDismantled = True

    totalPrice = sum([ item['totalPrice'] for item in itemCartInfo.itervalues() if item['totalPrice'].price > ZERO_MONEY ], ITEM_PRICE_EMPTY)
    numBoughtItems = sum((item['quantity'] for item in itemCartInfo.itervalues() if item['quantity'] > 0))
    return CartInfo(totalPrice, numSelectedItems, numApplyingItems, numBoughtItems, len(purchaseItems), isAtLeastOneItemFromInventory, isAtLeastOneItemDismantled)


def containsVehicleBound(purchaseItems):
    fromInventoryCounter = Counter()
    vehCD = g_currentVehicle.item.intCD
    for purchaseItem in purchaseItems:
        if purchaseItem.item and purchaseItem.item.isVehicleBound and not purchaseItem.isDismantling and not purchaseItem.item.isRentable:
            if not purchaseItem.isFromInventory:
                return True
            fromInventoryCounter[purchaseItem.item] += 1

    return any((count > item.boundInventoryCount.get(vehCD, 0) for item, count in fromInventoryCounter.items()))


def getPurchaseMoneyState(price):
    itemsCache = dependency.instance(IItemsCache)
    money = itemsCache.items.stats.money
    exchangeRate = itemsCache.items.shop.exchangeRate
    shortage = money.getShortage(price)
    if not shortage:
        moneyState = MoneyForPurchase.ENOUGH
    else:
        money = money - price + shortage
        price = shortage
        money = money.exchange(Currency.GOLD, Currency.CREDITS, exchangeRate, default=0)
        shortage = money.getShortage(price)
        if not shortage:
            moneyState = MoneyForPurchase.ENOUGH_WITH_EXCHANGE
        else:
            moneyState = MoneyForPurchase.NOT_ENOUGH
    return moneyState


def isTransactionValid(moneyState, price):
    itemsCache = dependency.instance(IItemsCache)
    money = itemsCache.items.stats.money
    shortage = money.getShortage(price)
    inGameShopOn = Currency.GOLD in shortage.getCurrency() and isIngameShopEnabled()
    validTransaction = moneyState != MoneyForPurchase.NOT_ENOUGH or inGameShopOn
    return validTransaction
