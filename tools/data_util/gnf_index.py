import requests
import datetime

value_classification_list = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']
value_classification_label_dict = {vc: idx for idx, vc in enumerate(value_classification_list)}
value_classification_threshold = [0, 25, 46, 54, 75, 99]
gnf_api_base = 'https://api.alternative.me/fng/?limit={}'

def get_gnf(limit=10):
    assert isinstance(limit, int), TypeError('limit {} must be an integer'.format(limit))
    c = requests.get(gnf_api_base.format(limit))
    if c.status_code != 200:
        raise ValueError("get gnf index error, code: {}".format(c.status_code))
    c = c.json()
    for item in c['data']:
        item['value'] = int(item['value'])
        item['timestamp'] = datetime.datetime.fromtimestamp(int(item['timestamp']))
        score_floor = value_classification_threshold[value_classification_list.index(item['value_classification'])]
        score_ceil = value_classification_threshold[value_classification_list.index(item['value_classification']) + 1]
        item['normalized_value'] = (item['value'] - score_floor) / (score_ceil - score_floor)
        item['value_classification_index'] = value_classification_list.index(item['value_classification'])
    return c

if __name__ == "__main__":
    print(get_gnf())