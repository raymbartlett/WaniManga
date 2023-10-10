"""Helper functions."""
import requests
import json

with open('kanji_data.json', 'r') as json_file:
    KANJI_DATA = json.load(json_file)


def get_known_kanji(WANIKANI_KEY):
    """Request kanji at SRS Stage 5 or higher."""
    HEADERS = {
        'Authorization': f'Bearer {WANIKANI_KEY}',
    }

    with open('wanikani_kanji.json') as f:
        wanikani_kanji = json.load(f)

    known_kanji = []
    assignments_url = 'https://api.wanikani.com/v2/assignments'
    while assignments_url:
        assignments_response = requests.get(assignments_url, headers=HEADERS)
        if assignments_response.status_code == 200:
            for obj in assignments_response.json()['data']:
                if obj['data']['srs_stage'] >= 5 and obj['data']['subject_type'] == 'kanji':
                    kanji = wanikani_kanji[str(obj['data']['subject_id'])]  # link Subject ID to actual kanji character
                    known_kanji.append(kanji)
        else:
            print('error:', assignments_response.status_code)
            return None
        assignments_url = assignments_response.json()['pages']['next_url']

    return set(known_kanji)


def sort_kanji(kanji_set):
    """Return input kanji set sorted by multiple metrics."""
    by_wk_level = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '7': [],
        '8': [],
        '9': [],
        '10': [],
        '11': [],
        '12': [],
        '13': [],
        '14': [],
        '15': [],
        '16': [],
        '17': [],
        '18': [],
        '19': [],
        '20': [],
        '21': [],
        '22': [],
        '23': [],
        '24': [],
        '25': [],
        '26': [],
        '27': [],
        '28': [],
        '29': [],
        '30': [],
        '31': [],
        '32': [],
        '33': [],
        '34': [],
        '35': [],
        '36': [],
        '37': [],
        '38': [],
        '39': [],
        '40': [],
        '41': [],
        '42': [],
        '43': [],
        '44': [],
        '45': [],
        '46': [],
        '47': [],
        '48': [],
        '49': [],
        '50': [],
        '51': [],
        '52': [],
        '53': [],
        '54': [],
        '55': [],
        '56': [],
        '57': [],
        '58': [],
        '59': [],
        '60': [],
        'Not on WaniKani': []
    }

    by_jlpt_level = {
        'N5': [],
        'N4': [],
        'N3': [],
        'N2': [],
        'N1': [],
        'Not on JLPT': []
    }

    by_joyo_level = {
        '1': [],
        '2': [],
        '3': [],
        '4': [],
        '5': [],
        '6': [],
        '9': [],
        'Not in Jōyō': []
    }

    by_frequency = {
        '1-500': [],
        '501-1000': [],
        '1001-1500': [],
        '1501-2000': [],
        '2001-2500': [],
        'Not in top 2500': []
    }

    for kanji in kanji_set:
        if kanji in KANJI_DATA:
            wk_level = str(KANJI_DATA[kanji]['wanikani_level'])
            jlpt_level = str(KANJI_DATA[kanji]['jlpt_level'])
            joyo_level = str(KANJI_DATA[kanji]['joyo_level'])
            frequency = str(KANJI_DATA[kanji]['frequency'])
        else:
            wk_level = '0'
            jlpt_level = '0'
            joyo_level = '0'
            frequency = '0'

        if wk_level == '0':
            by_wk_level['Not on WaniKani'].append(kanji)
        else:
            by_wk_level[wk_level].append(kanji)

        if jlpt_level == '0':
            by_jlpt_level['Not on JLPT'].append(kanji)
        else:
            by_jlpt_level[jlpt_level].append(kanji)

        if joyo_level == '0':
            by_joyo_level['Not in Jōyō'].append(kanji)
        else:
            by_joyo_level[joyo_level].append(kanji)

        if frequency == '0':
            by_frequency['Not in top 2500'].append(kanji)
        else:
            by_frequency[frequency].append(kanji)

    return by_wk_level, by_jlpt_level, by_joyo_level, by_frequency
