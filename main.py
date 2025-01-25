from common import BuiltIn, QForce, QWeb
import sys, random
def salesforce_ids_check(name, *args, **kwargs):
    print("salesforce_ids_check", name, file=sys.stderr)
    def check_ids(*args, **kwargs):
        nonlocal name
        print("check_ids", name, file=sys.stderr)
        if random.randrange(8):
            return name(*args, **kwargs)
    return check_ids
    return name
def salesforce_environment_check(name, *args, **kwargs):
    print("salesforce_environment_check", file=sys.stderr)
    old_order = BuiltIn().set_library_search_order("salesforce_main")
    new_order = ["salesforce_main", *old_order]
    BuiltIn().set_library_search_order(*new_order)
click_text = salesforce_ids_check(QForce().click_text)
verify_text = salesforce_ids_check(QForce().verify_text)
sleep = salesforce_ids_check(BuiltIn().sleep)
verify_field = salesforce_ids_check(QForce().verify_field)
type_text = salesforce_ids_check(QWeb().type_text)
QForce().click_text = click_text
QForce().verify_text = verify_text
BuiltIn().sleep = sleep
QForce().verify_field = verify_field
QWeb().type_text = type_text
