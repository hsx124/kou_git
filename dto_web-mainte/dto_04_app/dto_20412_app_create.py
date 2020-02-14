from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class AppCreateForm(forms.Form):

    ip_code = forms.CharField(
        label='IPコード',
        max_length=10,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('IPコード'),
                        'max_length': ValidationUtil.E0000002.format('IPコード','10')}
    )

    ip_name = forms.CharField(
        label='IP名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('IP名'),
                    'max_length': ValidationUtil.E0000002.format('IP名','100')}
    )

    app_name = forms.CharField(
        label='アプリ名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('アプリ名'),
                        'max_length': ValidationUtil.E0000002.format('アプリ名','100')}
                        )

    app_id_ios = forms.CharField(
        label='アプリID_iOS',
        min_length=9,
        max_length=10,
        required=False,
        validators=[ValidationUtil.validate_halfwidth_num],
        error_messages={'max_length': ValidationUtil.E0000012.format('アプリID_iOS','9','10'),
                        'min_length': ValidationUtil.E0000012.format('アプリID_iOS','9','10'),
                        'halfwidth_num': ValidationUtil.E0000013.format('アプリID_iOS')}
    )

    app_id_android = forms.CharField(
        label='アプリID_Android',
        min_length=14,
        max_length=14,
        required=False,
        validators=[ValidationUtil.validate_halfwidth_num],
        error_messages={'max_length': ValidationUtil.E0000016.format('アプリID_Android','14'),
                        'min_length': ValidationUtil.E0000016.format('アプリID_Android','14'),
                        'halfwidth_num': ValidationUtil.E0000013.format('アプリID_Android')}
    )

    distributor_name = forms.CharField(
        label='販売元',
        max_length=100,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('販売元','100')}
    )

    service_start_date = forms.DateTimeField(
        label='サービス開始年月日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y/%m/%d'],
        error_messages={'invalid': ValidationUtil.E0000008},
    )
    service_end_date = forms.DateTimeField(
        label='サービス終了年月日',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y/%m/%d'],
        error_messages={'invalid': ValidationUtil.E0000008},
    )

    # 複合項目チェック
    def clean(self):
        cleaned_data = super().clean()

        # キーワードの文字数チェック
        if ('app_id_ios' in cleaned_data
            and 'app_id_android' in cleaned_data):
            if ('' == cleaned_data['app_id_ios']
                and '' == cleaned_data['app_id_android']):
                self.add_error('app_id_ios',ValidationUtil.E0000015.format('アプリID_iOS','アプリID_Android'))

        # IP公開開始とIP公開終了の整合性チェック
        if ('service_start_date' in cleaned_data
            and 'service_end_date' in cleaned_data):
            if (cleaned_data['service_start_date']
                and cleaned_data['service_end_date']
                and cleaned_data['service_start_date'] > cleaned_data['service_end_date']):
                self.add_error('service_end_date',ValidationUtil.E0000009.format('サービス終了年月日','サービス開始年月日'))

        # アプリID_iOSが9桁 10桁以外の時にエラー
        if 'app_id_ios' in cleaned_data:
            if (len(cleaned_data['app_id_ios']) < 9
                and len(cleaned_data['app_id_ios']) > 10):
                self.add_error('app_id_ios',ValidationUtil.E0000012.format('アプリID_iOS', '9', '10'))

        return cleaned_data
