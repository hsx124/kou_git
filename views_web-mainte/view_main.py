
from django.views.generic import TemplateView
from datetime import date, datetime
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

class MainView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):

    # date, datetimeの変換関数
    def json_serial(self, obj):
        # 日付型の場合には、文字列に変換
        if isinstance(obj, (datetime, date)):
            return obj.strftime('%Y/%m/%d')
        # 上記以外はサポート対象外.
        raise TypeError ("Type %s not serializable" % type(obj))

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='g_mainte')