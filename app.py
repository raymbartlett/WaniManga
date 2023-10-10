"""All app routes and function calls."""
from flask import Flask, request, render_template
from io import BytesIO
import zipfile
import base64
from text_extractor import TextExtractor
from helpers import get_known_kanji, sort_kanji

app = Flask(__name__)


def extract_cover(cbz_file):
    """Return base64 encoded image of first page of upload."""
    try:
        with zipfile.ZipFile(cbz_file, 'r') as archive:
            file_list = archive.namelist()
            for file in file_list:
                if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                    first_image_data = archive.read(file)
                    return base64.b64encode(first_image_data).decode('utf-8')

    except Exception as e:
        print(f"Error extracting image from CBZ file: {str(e)}")

    return None


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """Return results page with sorted kanji and stats."""
    if request.method == 'GET':
        return render_template('index.html')  # TODO: add error page for incorrect file

    if request.method == 'POST':
        file = request.files['file-input']
        WANIKANI_KEY = request.form['text-input']

        if file and file.filename.endswith(('.cbz', '.cbr')):
            cbz_file_data = BytesIO(file.read())
            cover = extract_cover(cbz_file_data)

            extractor = TextExtractor()
            try:
                source_kanji = extractor.process_cbz(cbz_file_data)
            except:
                return render_template('error.html', message='Corrupted input file')
            known_kanji = get_known_kanji(WANIKANI_KEY)

            by_wk_level, by_jlpt_level, by_joyo_level, by_frequency = sort_kanji(source_kanji)

            kanji_data = {}
            if known_kanji is None:
                kanji_data["known_in_source"] = []
                kanji_data["unknown_in_source"] = source_kanji
            else:
                kanji_data["known_in_source"] = list(source_kanji.intersection(known_kanji))
                kanji_data["unknown_in_source"] = list(source_kanji.difference(known_kanji))
            kanji_data["by_wk_level"] = by_wk_level
            kanji_data["by_jlpt_level"] = by_jlpt_level
            kanji_data["by_joyo_level"] = by_joyo_level
            kanji_data["by_frequency"] = by_frequency

            stats = {}
            stats['filename'] = str(file).split('\'')[1]
            stats['cover'] = cover
            stats['total_kanji'] = len(kanji_data['known_in_source']) + len(kanji_data['unknown_in_source'])
            stats['num_known'] = len(kanji_data['known_in_source'])
            stats['num_unknown'] = len(kanji_data['unknown_in_source'])

            ratio_known = stats['num_known'] / stats['total_kanji']
            diff = ''
            if known_kanji is None:
                diff = 'Invalid WaniKani Key'
            elif 0.00 <= ratio_known < 0.25:
                diff = 'Difficulty: Hell'
            elif 0.25 <= ratio_known < 0.50:
                diff = 'Difficulty: Death'
            elif 0.50 <= ratio_known < 0.75:
                diff = 'Difficulty: Painful'
            elif 0.75 <= ratio_known < 0.99:
                diff = 'Difficulty: Pleasant'
            else:
                diff = 'Difficulty: 全勝'
            stats['difficulty'] = diff

            return render_template(
                'results.html',
                stats=stats,
                kanji_data=kanji_data
            )
        else:
            return render_template('error.html', message='Invalid file type')


if __name__ == '__main__':
    app.run(debug=True)
