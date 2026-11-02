import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pii_sanitizer import PIISanitizer


class TestPIISanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = PIISanitizer()

    def test_masks_brazilian_cpf_and_cnpj(self):
        text = "CPF 123.456.789-09; CNPJ 12.345.678/0001-95."

        self.assertEqual(
            self.sanitizer.sanitize(text),
            "CPF [CPF_REDACTED]; CNPJ [CNPJ_REDACTED].",
        )

    def test_masks_unformatted_brazilian_cpf(self):
        self.assertEqual(
            self.sanitizer.sanitize("CPF 12345678909"),
            "CPF [CPF_REDACTED]",
        )

    def test_masks_email_and_formatted_brazilian_phone(self):
        text = "Contato: pessoa@example.com, telefone (11) 98765-4321."

        self.assertEqual(
            self.sanitizer.sanitize(text),
            "Contato: [EMAIL_REDACTED], telefone [PHONE_REDACTED].",
        )

    def test_masks_unformatted_brazilian_phone(self):
        self.assertEqual(
            self.sanitizer.sanitize("Telefone 11987654321"),
            "Telefone [PHONE_REDACTED]",
        )

    def test_preserves_text_without_recognized_pii(self):
        text = "Deal 9876543210: Acme Logística SA."

        self.assertEqual(self.sanitizer.sanitize(text), text)


if __name__ == "__main__":
    unittest.main()
