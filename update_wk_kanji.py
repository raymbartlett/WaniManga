"""Request all kanji from WaniKani."""
import requests
import json

WANIKANI_KEY = ''

with open('kanji_data.json', 'r') as json_file:
    kanji_data = json.load(json_file)

with open('wanikani_kanji.json') as f:
    wanikani_kanji = json.load(f)


def get_all_subjects(WANIKANI_KEY):
    """Generate json of { id: kanji }."""
    HEADERS = {
        'Authorization': f'Bearer {WANIKANI_KEY}',
    }

    subjects_url = 'https://api.wanikani.com/v2/subjects/'
    while subjects_url:
        subjects_response = requests.get(subjects_url, headers=HEADERS)
        if subjects_response.status_code == 200:
            for obj in subjects_response.json()['data']:
                if obj['object'] == 'kanji':
                    if obj['id'] not in wanikani_kanji:
                        wanikani_kanji[obj['id']] = obj['data']['characters']
                    if obj['data']['characters'] not in kanji_data:
                        kanji_data[obj['data']['characters']] = {
                            "joyo_level": 0,
                            "jlpt_level": "0",
                            "frequency": "0",
                        }
                    kanji_data[obj['data']['characters']]['wanikani_level'] = obj['data']['level']
                    kanji_data[obj['data']['characters']]['wanikani_id'] = obj['id']
        else:
            print('error:', subjects_response.status_code)
        subjects_url = subjects_response.json()['pages']['next_url']

    return wanikani_kanji, kanji_data


if __name__ == "__main__":
    wanikani_kanji, kanji_data = get_all_subjects(WANIKANI_KEY)
    with open('kanji_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(kanji_data, json_file, ensure_ascii=False)
    with open('wanikani_kanji.json', 'w', encoding='utf-8') as json_file:
        json.dump(wanikani_kanji, json_file, ensure_ascii=False)
