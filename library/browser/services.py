
import library.utilities.utilities as utils

def get_search_results():
    return utils.get_search_results()

def sort_by_date(array):
    results = get_search_results()
    results.sort(key=lambda x:x.release_year)
    return results
