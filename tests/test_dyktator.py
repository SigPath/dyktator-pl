"""Testy Dyktatora PL — processor bez zależności, przepływ end-to-end na Echo."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dyktator.processor import process_dictation  # noqa: E402
from dyktator.transcribe import EchoTranscriber  # noqa: E402
from dyktator.clipboard import copy_to_clipboard  # noqa: E402


class TestProcessor(unittest.TestCase):
    def test_komendy_interpunkcyjne(self):
        self.assertEqual(process_dictation("witaj świecie kropka"), "Witaj świecie.")

    def test_przecinek_i_wielka_litera(self):
        self.assertEqual(process_dictation("jeden przecinek dwa przecinek trzy"), "Jeden, dwa, trzy")

    def test_nowa_linia_rozdziela_zdania(self):
        out = process_dictation("pierwsza linia nowa linia druga linia działa")
        self.assertIn("\n", out)
        self.assertTrue(out.splitlines()[0].startswith("Pierwsza"))
        self.assertTrue(out.splitlines()[1].startswith("Druga"))

    def test_spacja_przed_kropka_znika(self):
        self.assertEqual(process_dictation("koniec zdania kropka koniec"), "Koniec zdania. Koniec")

    def test_pytajnik_i_wykrzyknik(self):
        self.assertEqual(process_dictation("co to jest pytajnik no brawo wykrzyknik"), "Co to jest? No brawo!")

    def test_pusty_dyktat(self):
        self.assertEqual(process_dictation("   "), "")

    def test_podwojne_spacje_sprzatane(self):
        self.assertEqual(process_dictation("witaj  świecie"), "Witaj  świecie".replace("  ", " "))


class TestFlow(unittest.TestCase):
    def test_echo_end_to_end(self):
        raw = EchoTranscriber.FIXED
        out = process_dictation(raw)
        self.assertIn("Witaj świecie.", out)
        self.assertIn("test, dyktatora!", out.replace("\n", " ") if "\n" not in out else out)
        self.assertIn("Druga linia", out)

    def test_clipboard_z_wstrzyknieta_komenda(self):
        # fałszywa „komenda”: cat czyta stdin — sprawdzamy tylko ścieżkę sukcesu/porażki
        self.assertTrue(copy_to_clipboard("test", command=["cat"]))
        self.assertFalse(copy_to_clipboard("test", command=["nie-ma-takiej-komendy-xyz"]))


if __name__ == "__main__":
    unittest.main()
