from typing import NamedTuple
from typing import List
from typing import Dict
from ipdds_app.dto.dto_06_similar_search import DtoSimilarSearch

class DtoSearchResult(NamedTuple):
    
    class InputContents(NamedTuple):
        '''
        ユーザ入力情報
        '''
        keyword : List[str]
        category : List[str]
        core : List[str]
        media : List[str]
        imp : List[str]
        fiction : str
        fact_tag : List[str]
        start_date : List[str]
        end_date : List[str]
    
    class SearchResultContents(NamedTuple):
        '''
        検索結果
        '''
        class Tag(NamedTuple):
            class PairCodeName(NamedTuple):
                code : str
                name : str

            category : List[str]
            core : List[PairCodeName]
            media :PairCodeName
            imp : List[PairCodeName]
            fiction_flag : str
            fact_tag : List[PairCodeName]

        class BookSeries(NamedTuple):
            series_name : str
            qty_total_sales_2 :str
            avg_per_volume : str
        
        keyvisual_file_name : str
        ip_code : str
        ip_name : str
        ip_kana_name : str
        overview : str
        tag : Tag
        book_series : List[BookSeries]
        similar_rate : str
        release_date : str
        update_date : str
    
    form_elm : DtoSimilarSearch
    input_contents : InputContents
    search_result_keyword : List[SearchResultContents]
    search_result_similar : List[SearchResultContents]
    search_result_cnt : int
