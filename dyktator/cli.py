"""CLI Dyktatora:  python3 -m dyktator once | text "..." | demo"""
import argparse
import os
import sys
import tempfile
from typing import List

from .clipboard import copy_to_clipboard
from .processor import process_dictation
from .transcribe import EchoTranscriber, WhisperTranscriber


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dyktator",
        description="Lokalne dyktowanie PL: mów → tekst z polskimi komendami (kropka, przecinek, nowa linia…).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    once_p = sub.add_parser("once", help="nagraj z mikrofonu → przetwórz → schowek")
    once_p.add_argument("--seconds", type=float, default=8.0)
    once_p.add_argument("--model", default="small", help="rozmiar whispera (tiny/base/small)")
    once_p.add_argument("--no-clipboard", action="store_true", help="tylko wydruk, bez schowka")

    text_p = sub.add_parser("text", help="przetwórz podany tekst (bez mikrofonu)")
    text_p.add_argument("raw")

    sub.add_parser("demo", help="demonstracja na wbudowanym dyktacie (bez mikrofonu)")

    args = parser.parse_args(argv)

    if args.cmd == "text":
        print(process_dictation(args.raw))
        return 0

    if args.cmd == "demo":
        raw = EchoTranscriber.FIXED
        result = process_dictation(raw)
        print("DYKTAT (surowy):", raw)
        print("WYNIK:")
        print(result)
        return 0

    if args.cmd == "once":
        with tempfile.TemporaryDirectory() as tmp:
            wav = os.path.join(tmp, "dyktat.wav")
            try:
                from .audio import record_wav
                print(f"Mów! ({args.seconds} s)…")
                if not record_wav(wav, seconds=args.seconds):
                    print("BŁĄD: brak mikrofonu albo zależności (pip install faster-whisper sounddevice numpy scipy).", file=sys.stderr)
                    return 2
            except ImportError:
                print("BŁĄD: pip install faster-whisper sounddevice numpy scipy", file=sys.stderr)
                return 2
            transcriber = WhisperTranscriber(model_size=args.model)
            print("Transkrybuję lokalnie…")
            raw = transcriber.transcribe(wav)
        result = process_dictation(raw)
        print("\nWYNIK:")
        print(result)
        if not args.no_clipboard:
            if copy_to_clipboard(result):
                print("→ skopiowano do schowka")
            else:
                print("→ schowek niedostępny (zainstaluj xclip/wl-copy na Linuksie)", file=sys.stderr)
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
