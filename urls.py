from django.urls import path,re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from ipdds_app.views.view_01_home.view_10101_home import HomeView
from ipdds_app.views.view_02_sakuhin_list.view_10201_sakuhin_list_title import SakuhinListTitleView
from ipdds_app.views.view_02_sakuhin_list.view_10202_sakuhin_list_age import SakuhinListAgeView
from ipdds_app.views.view_03_detail.view_10301_detail import SakuhinDetailView
from ipdds_app.views.view_04_compare.view_10401_compare import SakuhinCompareView
from ipdds_app.views.view_05_search.view_10502_search_result import SearchResultFormView
from ipdds_app.views.view_05_search.view_10501_search import SearchFormView
from ipdds_app.views.view_06_link_collection.view_10601_link_collection import LinkCollectionView
from ipdds_app.views.view_compare_kago import CompareKagoView
from django.contrib.auth import views as auth_views

app_name= 'ipdds_app'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='ipdds_app/00_login.html'), name='00_login'),
    path('home/', HomeView.as_view(), name='10101_home'),    
    path('sakuhin_list_title/', SakuhinListTitleView.as_view(), name='10201_sakuhin_list_title'),
    path('detail/', SakuhinDetailView.as_view(), name='10301_detail'),
    path('compare/', SakuhinCompareView.as_view(), name='10401_compare'),    
    path('search_result/', SearchResultFormView.as_view(), name='10502_search_result'),
    path('search/', SearchFormView.as_view(), name='10501_search'),
    path('sakuhin_list_age/', SakuhinListAgeView.as_view(), name='10202_sakuhin_list_age'),
    path('link_collection/', LinkCollectionView.as_view(), name='10601_link_collection'),   
    path('compare_kago/', CompareKagoView.set_session, name='compare_kago'),   

]
urlpatterns += staticfiles_urlpatterns()
