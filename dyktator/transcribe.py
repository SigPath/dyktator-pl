"""Transkrybenci: Whisper (lokalny, opcjonalna zależność) i Echo (deterministyczny)."""
from typing import Protocol


class Transcriber(Protocol):
    def transcribe(self, wav_path: str) -> str: ...


class WhisperTranscriber:
    """faster-whisper (lokalnie, model small domyślnie). Zależność instalowana opcjonalnie:

        pip install faster-whisper
    """

    def __init__(self, model_size: str = "small", language: str = "pl"):
        self.model_size = model_size
        self.language = language
        self._model = None

    def _load(self):
        if self._model is None:
            from faster_whisper import WhisperModel  # opcjonalna zależność
            self._model = WhisperModel(self.model_size, compute_type="int8")
        return self._model

    def transcribe(self, wav_path: str) -> str:
        model = self._load()
        segments, _info = model.transcribe(wav_path, language=self.language)
        return " ".join(seg.text.strip() for seg in segments).strip()


class EchoTranscriber:
    """Zwraca zawsze ten sam dyktat — do testów i demo bez mikrofonu."""

    FIXED = (
        "witaj świecie kropka to jest test przecinek dyktatora wykrzyknik "
        "nowa linia druga linia działa"
    )

    def transcribe(self, wav_path: str) -> str:
        return self.FIXED
