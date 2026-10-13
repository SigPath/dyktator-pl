# Dyktator PL

**Lokalne dyktowanie po polsku**: mówisz do mikrofonu → whisper.cpp (lokalnie, na Twoim
Macu/PC) → sformatowany tekst w schowku. Z komendami głosowymi po polsku.

## Komendy głosowe

| Mówisz | Dostajesz |
|---|---|
| „kropka" | `.` |
| „przecinek" | `,` |
| „pytajnik" / „wykrzyknik" / „dwukropek" | `?` `!` `:` |
| „nowa linia" / „nowy akapit" | `\n` / pusta linia |
| „myślnik" | `-` |

Po przetworzeniu: wielkie litery na początku zdań, sprzątanie spacji.

## Szybki start

```bash
# zależności runtime (lokalny whisper):
pip install faster-whisper sounddevice numpy scipy

# demo bez mikrofonu (wbudowany dyktat):
python3 -m dyktator demo

# przetwórz gotowy tekst:
python3 -m dyktator text "lista zakupów dwukropek jajka przecinek mąka kropka"

# realne dyktowanie (8 s z mikrofonu → schowek):
python3 -m dyktator once --seconds 8 --model small
```

`text` i `demo` działają bez żadnych zależności — czysty Python. Mikrofon wymaga
`faster-whisper` + `sounddevice`.

## Architektura

```
dyktator/
├── processor.py   # komendy PL → interpunkcja, wielkie litery (czysty, testowalny)
├── transcribe.py  # WhisperTranscriber (faster-whisper, lazy) + EchoTranscriber (testy)
├── audio.py       # nagrywanie przez sounddevice (opcjonalne)
├── clipboard.py   # schowek: pbcopy / wl-copy / xclip / PowerShell
└── cli.py         # once | text | demo
```

## Testy

```bash
python3 tests/test_dyktator.py   # 9 testów: komendy, wielkie litery, przepływ, schowek
```

## Uczciwe ograniczenia

- v1 nagrywa stały odcinek czasu (domyślnie 8 s); VAD (auto-stop po ciszy) w planach,
- meni-bar macOS zrobię, gdy M0 MB Translatora przejdzie pierwszą kompilację —
  na razie CLI, które da się spiąć z jakimkolwiek hotkeyem (np. Raycast/Alfred),
- jakość = jakość whispera „small"; „base" szybszy, ale gorzej z polskimi końcówkami.

## Licencja

MIT
