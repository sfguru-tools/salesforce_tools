def query_records(query, *args, **kwargs):
    query = query.replace("&", "%24").replace("#", "%23")
    global query_records_not_escaped
    return query_records_not_escaped(query, *args, **kwargs)

def orders_query(account_ids, service_account_id_mapping):
    records = query_records(f"select vlocity_cmt__DefaultServiceAccountId__c, AccountId, Account.Name, Account.CreatedDate, CreatedDate, Id from Order where (vlocity_cmt__OrderStatus__c = 'Ready To Submit' or vlocity_cmt__OrderStatus__c = 'In Progress') and vlocity_cmt__DefaultServiceAccountId__c in {account_ids}")
    orders_dict = dict()
    for order in records["records"]:
        order_info = f"{order['Id']} ({order['CreatedDate']})"
        mapping = service_account_id_mapping[order["vlocity_cmt__DefaultServiceAccountId__c"]]
        if mapping in orders_dict:
            mapped_dict = orders_dict[mapping]
            if order["AccountId"] in mapped_dict:
                mapped_dict[order["AccountId"]].append(order_info)
                continue
        else:
            mapped_dict = dict()
            orders_dict[mapping] = mapped_dict
        mapped_dict[order["AccountId"]] = [order["Account"]["CreatedDate"], order["Account"]["Name"], order_info]
    return orders_dict, records

def assets_query(account_ids, service_account_id_mapping):
    records = query_records(f"select vlocity_cmt__ServiceAccountId__c, AccountId, Account.Name, Account.CreatedDate, CreatedDate, Id from Asset WHERE vlocity_cmt__ProvisioningStatus__c = 'Active' and vlocity_cmt__ServiceAccountId__c in {account_ids}")
    assets_dict = dict()
    for asset in records["records"]:
        asset_info = f"{asset['Id']} ({asset['CreatedDate']})"
        mapping = service_account_id_mapping[asset["vlocity_cmt__ServiceAccountId__c"]]
        if mapping in assets_dict:
            mapped_dict = assets_dict[mapping]
            if asset["AccountId"] in mapped_dict:
                mapped_dict[asset["AccountId"]].append(asset_info)
                continue
        else:
            mapped_dict = dict()
            assets_dict[mapping] = mapped_dict
        mapped_dict[asset["AccountId"]] = [asset["Account"]["CreatedDate"], asset["Account"]["Name"], asset_info]
    return assets_dict, records

def salesforce_environment_check(name, *args, **kwargs):
    from common import QForce
    global query_records_not_escaped
    if query_records_not_escaped is None:
        query_records_not_escaped = QForce().query_records
    QForce().query_records = query_records
    import addresses
    addresses.queryForOpenOrders = orders_query
    addresses.queryForActiveAssets = assets_query

query_records_not_escaped = None
