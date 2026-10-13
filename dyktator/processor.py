"""Przetwarzanie zapisu dyktowanego: komendy głosowe PL → interpunkcja, wielkie litery."""
import re
from typing import List

COMMANDS = [
    (r"\bkropka\b", "."),
    (r"\bprzecinek\b", ","),
    (r"\bwykrzyknik\b", "!"),
    (r"\bpytajnik\b", "?"),
    (r"\bdwukropek\b", ":"),
    (r"\bmyślnik\b", " - "),
    (r"\bnowa linia\b", "\n"),
    (r"\bnowy akapit\b", "\n\n"),
]


def process_dictation(raw: str) -> str:
    """Zamienia dyktat na sformatowany tekst:
    1. komendy głosowe → znaki interpunkcyjne,
    2. sprzątanie spacji przed interpunkcją,
    3. wielka litera na początku każdego zdania/wiersza.
    """
    text = raw.strip()
    if not text:
        return ""

    for pattern, replacement in COMMANDS:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # spacja przed interpunkcją i wokół znaku nowej linii znika, po interpunkcji — zostaje
    text = re.sub(r"\s+([.,!?:])", r"\1", text)
    text = re.sub(r"[ \t]*\n[ \t]*", "\n", text)
    text = re.sub(r"\s*-\s*", " - ", text.replace(" - - ", " - "))
    text = re.sub(r"[ \t]{2,}", " ", text)

    # wielka litera: początek tekstu, po kropce/wykrzykniku/pytajniku i po nowej linii
    def capitalize_after(match: re.Match) -> str:
        return match.group(1) + match.group(2).upper()

    text = re.sub(r"(^|[.!?]\s+|\n)([a-ząćęłńóśźż])", capitalize_after, text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
