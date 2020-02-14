from django import forms
from typing import NamedTuple
from dateutil.parser import parse

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoMangaCreateForm(forms.Form):

    class DtoMedia(NamedTuple):
        media_code : str
        media_name : str

    class DtoPublisher(NamedTuple):
        publisher_code : str
        publisher_name : str

    class DtoStaffRole(NamedTuple):
        staff_role_code : str
        staff_role_name : str

    class DtoStaff(NamedTuple):
        staff_code : str
        staff_name : str

    manga_title_code = forms.CharField(
        label='マンガタイトルコード',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('マンガタイトルコード')}
    )
    manga_title_name = forms.CharField(
        label='マンガタイトル名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('マンガタイトル名'),
                        'max_length': ValidationUtil.E0000002.format('マンガタイトル名','100')},
    )
    rensai_start_yyyymm = forms.DateTimeField(
        label='連載開始年月',
        required=True,
        input_formats=['%Y','%Y%m'],
        error_messages={'required': ValidationUtil.E0000001.format('連載開始年月'),
                        'invalid': ValidationUtil.E0000008},
    )
    published_cnt = forms.CharField(
        label='既刊数',
        required=True,
        max_length=3,
        validators=[ValidationUtil.validate_halfwidth_num],
        error_messages={'max_length': ValidationUtil.E0000018.format('既刊数','3'),
                        'required': ValidationUtil.E0000001.format('既刊数')}
    )
    rensai_end_flg = forms.BooleanField(
        label='連載終了フラグ',
        required=False,
    )
    award_history = forms.CharField(
        label='作品受賞歴',
        required=False,
    )
    media_code = forms.CharField(
        label='掲載媒体コード',
        required=False,
    )
    publisher_code = forms.CharField(
        label='出版社コード',
        required=False,
    )
    staff_map_code = forms.CharField(
        label='スタッフ紐づけコード',
        required=False,
    )
    staff_role_code1 = forms.CharField(
        label='スタッフ役割コード1',
        required=False,
    )
    staff_code1 = forms.CharField(
        label='スタッフコード1',
        required=False,
    )
    staff_role_code2 = forms.CharField(
        label='スタッフ役割コード1',
        required=False,
    )
    staff_code2 = forms.CharField(
        label='スタッフコード1',
        required=False,
    )
    staff_role_code3 = forms.CharField(
        label='スタッフ役割コード1',
        required=False,
    )
    staff_code3 = forms.CharField(
        label='スタッフコード1',
        required=False,
    )
    staff_role_code4 = forms.CharField(
        label='スタッフ役割コード1',
        required=False,
    )
    staff_code4 = forms.CharField(
        label='スタッフコード1',
        required=False,
    )
    staff_role_code5 = forms.CharField(
        label='スタッフ役割コード1',
        required=False,
    )
    staff_code5 = forms.CharField(
        label='スタッフコード1',
        required=False,
    )

    # 複合項目チェック
    def clean(self):
        cleaned_data = super().clean()

        # スタッフの役割と名前のどちらかが入力されていない場合エラー
        if (not ('' == cleaned_data['staff_role_code1'] and '' == cleaned_data['staff_code1'])
            and ('' == cleaned_data['staff_role_code1'] or '' == cleaned_data['staff_code1'])):
            self.add_error('staff_code1',ValidationUtil.E0000020.format('スタッフ役割1','スタッフ1'))

        if (not ('' == cleaned_data['staff_role_code2'] and '' == cleaned_data['staff_code2'])
            and ('' == cleaned_data['staff_role_code2'] or '' == cleaned_data['staff_code2'])):
            self.add_error('staff_code2',ValidationUtil.E0000020.format('スタッフ役割2','スタッフ2'))

        if (not ('' == cleaned_data['staff_role_code3'] and '' == cleaned_data['staff_code3'])
            and ('' == cleaned_data['staff_role_code3'] or '' == cleaned_data['staff_code3'])):
            self.add_error('staff_code3',ValidationUtil.E0000020.format('スタッフ役割3','スタッフ3'))

        if (not ('' == cleaned_data['staff_role_code4'] and '' == cleaned_data['staff_code4'])
            and ('' == cleaned_data['staff_role_code4'] or '' == cleaned_data['staff_code4'])):
            self.add_error('staff_code4',ValidationUtil.E0000020.format('スタッフ役割4','スタッフ4'))

        if (not ('' == cleaned_data['staff_role_code5'] and '' == cleaned_data['staff_code5'])
            and ('' == cleaned_data['staff_role_code5'] or '' == cleaned_data['staff_code5'])):
            self.add_error('staff_code5',ValidationUtil.E0000020.format('スタッフ役割5','スタッフ5'))

        return cleaned_data
