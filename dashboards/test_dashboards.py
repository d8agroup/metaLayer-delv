import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from controllers import DashboardsController, _pagination
import constants

def setup():
    #TODO create test insights here
    #TODO currently assumes that Business category has 2 insights in it
    pass

def test_dashboards_in_category_bogus_category():
    
    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory("bogus category")
    
    assert passed
    assert dashboards.count() == 0, dashboard.count()

def test_dashboards_in_category_invalid_page_parameter():
    
    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page="one")
    
    assert not passed
    assert constants.PAGE_NUMBER_INVALID in errors

def test_dashboards_in_category_invalid_num_per_page_parameter():
    
    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page="1", num_per_page="ten")
    
    assert not passed
    assert constants.NUM_PER_PAGE_INVALID in errors

def test_dashboards_in_category_out_of_range():
    
    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page="5", num_per_page="2")
    
    dashboard_count = 0
    for dashboard in dashboards:
        dashboard_count += 1
    
    assert passed
    assert attributes['next_page'] == None
    assert attributes['prev_page'] == None, attributes['prev_page']
    assert attributes['max_page'] == 1, attributes['max_page']
    assert attributes['page'] == 5
    assert dashboard_count == 0, dashboard_count

def test_dashboards_in_category_success():
    
    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page="1", num_per_page="1")
    
    dashboard_count = 0
    for dashboard in dashboards:
        dashboard_count += 1
    
    assert passed
    assert attributes['next_page'] == 2
    assert attributes['prev_page'] == None
    assert attributes['max_page'] == 2
    assert attributes['page'] == 1
    assert dashboard_count == 1, dashboard_count

def test_dashboards_in_category_no_page_defined_success():

    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page=None, num_per_page="1")
    
    dashboard_count = 0
    for dashboard in dashboards:
        dashboard_count += 1
        
    assert passed
    assert attributes['next_page'] == 2
    assert attributes['prev_page'] == None
    assert attributes['max_page'] == 2
    assert attributes['page'] == 1
    assert dashboard_count == 1, dashboard_count

def test_dashboards_in_category_ten_per_page_success():

    passed, errors, dashboards, attributes = DashboardsController.GetDashboardsInCategory('Business', page="1", num_per_page="10")
    
    dashboard_count = 0
    for dashboard in dashboards:
        dashboard_count += 1
        
    assert passed
    assert attributes['next_page'] == None
    assert attributes['prev_page'] == None
    assert attributes['max_page'] == 1, attributes['max_page']
    assert attributes['page'] == 1
    assert dashboard_count == 2, dashboard_count

def test_pagination_1():
    
    pages = _pagination(1, 10)
    
    assert pages == range(1, 11), pages # 1 - 10

def test_pagination_2():
    
    pages = _pagination(5, 10)
    
    assert pages == range(1, 11), pages # 1 - 10

def test_pagination_3():
    
    pages = _pagination(1, 2)
    
    assert pages == range(1, 3), pages # 1 - 2

def test_pagination_4():
    
    pages = _pagination(10, 17)
    
    assert pages == range(1, 11), pages # 1 - 10

def test_pagination_5():
    
    pages = _pagination(11, 17)
    
    assert pages == range(11, 18), pages # 11 - 17

def test_pagination_6():
    
    pages = _pagination(11, 25)
    
    assert pages == range(11, 21), pages # 11 - 20

def test_pagination_7():
    
    pages = _pagination(1, 1)
    
    assert pages == [1], pages
    
def teardown():
    #TODO remove test insights here
    pass
    
    