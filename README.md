# WaniManga

An app to aid in Japanese immersion by judging the user's difficulty in reading a manga based on the kanji used. Takes a Japanese manga file and optionally a WaniKani API key as input and sorts the kanji by:
1. Known vs. Unknown (if WaniKani key is used)
2. WaniKani level
3. JLPT level
4. Jōyō level
5. Frequency

<details>
<summary>View results page</summary>

![Results page](/static/images/homepage.png)

</details>

## Setup Tutorial
1. Run `pip install -r requirements.txt`
2. Add WaniKani key to update_wk_kanji.py and run `python update_wk_kanji.py` (optional)
3. Run `flask run`

## Notes
* Inputting a full volume takes a long time; check your command line output for a progress bar.

## TODO
* Compile into an executable
* Speed up
