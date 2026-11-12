import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch
spec = importlib.util.spec_from_file_location('update', Path(__file__).resolve().parents[1] / 'scripts/update_data.py')
u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(u)
class RefreshTests(unittest.TestCase):
    def test_invalid_download_rejected(self):
        with self.assertRaises(ValueError): u.validate('<html>Unavailable</html>', 'UNRATE.csv')
    def test_failed_download_does_not_replace_files(self):
        with patch.object(u, 'download', side_effect=RuntimeError('offline')), patch.object(u.Path, 'replace') as replace:
            with self.assertRaises(RuntimeError): u.main()
            replace.assert_not_called()
if __name__ == '__main__': unittest.main()
