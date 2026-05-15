import re
import unicodedata
import requests

RU_URL = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/ru"
EN_URL = "https://raw.githubusercontent.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/master/en"

REPLACEMENTS = str.maketrans(
    {
        "0": "o",
        "1": "i",
        "3": "e",
        "@": "a",
        "$": "s",
    }
)

_bad_words = set()


def load_bad_words():
    global _bad_words

    for url in (RU_URL, EN_URL):
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                for line in r.text.splitlines():
                    w = line.strip().lower()
                    if w and not w.startswith("#"):
                        _bad_words.add(w)
        except Exception:
            pass

    print(f"[moderation] loaded {len(_bad_words)} bad words")


load_bad_words()


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.lower()
    text = text.translate(REPLACEMENTS)
    text = re.sub(r"[^a-zа-яёіїєґ]+", "", text)
    return text


def censor_text(text: str) -> str:
    if not text:
        return text

    norm_text = normalize(text)

    for bad in _bad_words:
        bad_norm = normalize(bad)

        if bad_norm and bad_norm in norm_text:
            return "*" * len(text)

    words = re.findall(r"[a-zа-яёіїєґ0-9]+", text, flags=re.IGNORECASE)

    bad_hits = set()

    for w in words:
        if normalize(w) in _bad_words:
            bad_hits.add(w.lower())

    if not bad_hits:
        return text

    def repl(match):
        w = match.group(0)
        return "*" * len(w) if w.lower() in bad_hits else w

    return re.sub(r"[a-zа-яёіїєґ0-9]+", repl, text, flags=re.IGNORECASE)
