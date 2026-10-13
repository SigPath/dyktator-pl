"""Dyktator PL — lokalne dyktowanie: mowa → tekst, z polskimi komendami głosowymi."""
from .processor import process_dictation
from .transcribe import EchoTranscriber, WhisperTranscriber
from .clipboard import copy_to_clipboard

__version__ = "1.0.0"
__all__ = ["process_dictation", "EchoTranscriber", "WhisperTranscriber", "copy_to_clipboard", "__version__"]
