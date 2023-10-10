"""Extracts kanji from images (repurposed and modified code from Mokuro)."""
import re
import os
import zipfile
import tempfile
from tqdm import tqdm
from mokuro.manga_page_ocr import MangaPageOcr


def is_kanji(character):
    """Check whether a character is kanji."""
    kanji_pattern = re.compile(r'[\u4e00-\u9faf]')
    return bool(kanji_pattern.match(character))


class TextExtractor:
    """Contains code for text extraction."""

    def __init__(self, pretrained_model_name_or_path='kha-white/manga-ocr-base', force_cpu=False, **kwargs):
        """Mokuro settings."""
        self.pretrained_model_name_or_path = pretrained_model_name_or_path
        self.force_cpu = force_cpu
        self.kwargs = kwargs
        self.mpocr = None

    def init_models(self):
        """Check OCR settings."""
        if self.mpocr is None:
            self.mpocr = MangaPageOcr(self.pretrained_model_name_or_path, self.force_cpu, **self.kwargs)

    def extract_kanji(self, result):
        """Add kanji to array."""
        kanji_list = []
        for block in result['blocks']:
            for line in block['lines']:
                for character in line:
                    if is_kanji(character):
                        kanji_list.append(character)
        return kanji_list

    def process_image(self, img_path):
        """Run OCR on image."""
        self.init_models()
        result = self.mpocr(img_path)
        return self.extract_kanji(result)

    # LINUX / WSL
    def process_cbz(self, cbz_path):
        """Loops through .cbz file, creating tempfile for each page."""
        kanji_array = []
        with zipfile.ZipFile(cbz_path, 'r') as cbz_file:
            for page in tqdm(cbz_file.namelist(), desc='processing pages...'):
                if page.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    image_data = cbz_file.read(page)
                    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(page)[1], delete=True) as temp_image_file:
                        temp_image_file.write(image_data)
                        kanji_list = self.process_image(temp_image_file.name)
                        kanji_array.extend(kanji_list)
        return set(kanji_array)
