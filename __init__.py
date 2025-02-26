from common import BuiltIn, QForce, QWeb, QVision
from robot.api import logger
import random

def salesforce_ids_check(name, *args, **kwargs):
    def check_ids(*args, **kwargs):
        nonlocal name
        if random.randrange(100):
            return name(*args, **kwargs)
    #return check_ids
    return name
def salesforce_environment_check(name, *args, **kwargs):
    old_order = BuiltIn().set_library_search_order("salesforce_tools")
    new_order = ["salesforce_tools", *old_order]
    BuiltIn().set_library_search_order(*new_order)
    import addresses
    addresses.queryForOpenOrders = ordersQuery
    addresses.queryForActiveAssets = assetsQuery

if salesforce_ids_check(None) is not None:
    click_text = salesforce_ids_check(QForce().click_text)
    verify_text = salesforce_ids_check(QForce().verify_text)
    sleep = salesforce_ids_check(BuiltIn().sleep)
    verify_field = salesforce_ids_check(QForce().verify_field)
    type_text = salesforce_ids_check(QWeb().type_text)
    QVision().click_text = salesforce_ids_check(QVision().click_text)
    QForce().click_text = click_text
    QForce().verify_text = verify_text
    BuiltIn().sleep = sleep
    QForce().verify_field = verify_field
    QWeb().type_text = type_text

def ordersQuery(accountIds, serviceAccountIdMapping):
    records = QForce().query_records(f"SELECT Id, CreatedDate, AccountId, Account.Name, Account.CreatedDate, vlocity_cmt__DefaultServiceAccountId__c FROM Order WHERE (vlocity_cmt__OrderStatus__c = 'Ready To Submit' OR vlocity_cmt__OrderStatus__c = 'In Progress') AND vlocity_cmt__DefaultServiceAccountId__c IN {accountIds}")
    ordersDict = dict()
    for order in records["records"]:
        orderInfo = f"{order['Id']} ({order['CreatedDate']})"
        saMapping = serviceAccountIdMapping[order["vlocity_cmt__DefaultServiceAccountId__c"]]
        if saMapping in ordersDict:
            mappedDict = ordersDict[saMapping]
            if order["AccountId"] in mappedDict:
                mappedDict[order["AccountId"]].append(orderInfo)
                continue
        else:
            mappedDict = dict()
            ordersDict[saMapping] = mappedDict
        mappedDict[order["AccountId"]] = [order["Account"]["CreatedDate"], order["Account"]["Name"], orderInfo]
    return ordersDict, records

def assetsQuery(accountIds, serviceAccountIdMapping):
    assetsResult = QForce().query_records(f"SELECT Id, CreatedDate, AccountId, Account.Name, Account.CreatedDate, vlocity_cmt__ServiceAccountId__c FROM Asset WHERE vlocity_cmt__ProvisioningStatus__c = 'Active' AND vlocity_cmt__ServiceAccountId__c IN {accountIds}")
    assetsDict = dict()
    for asset in assetsResult["records"]:
        assetInfo = f"{asset['Id']} ({asset['CreatedDate']})"
        saMapping = serviceAccountIdMapping[asset["vlocity_cmt__ServiceAccountId__c"]]
        if saMapping in assetsDict:
            mappedDict = assetsDict[saMapping]
            if asset["AccountId"] in numOnlyDict:
                mappedDict[asset["AccountId"]].append(assetInfo)
                continue
        else:
            mappedDict = dict()
            assetsDict[saMapping] = mappedDict
        mappedDict[asset["AccountId"]] = [asset["Account"]["CreatedDate"], asset["Account"]["Name"], assetInfo]
    return assetsDict, assetsResult
