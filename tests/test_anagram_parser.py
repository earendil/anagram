from unittest import TestCase
from unittest.mock import patch, call, MagicMock

from anagram_parser.anagram_parser import file_handler, Anagrams, _main


class TestFileHandler(TestCase):
    def test_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            handler = file_handler("there_is_no_way_i_exist.txt")
            handler.__next__()


class TestAnagram(TestCase):
    @patch("anagram_parser.anagram_parser.file_handler", MagicMock())
    def setUp(self):
        self.anagrams = Anagrams("file.txt")


class TestAnagramValidate(TestAnagram):
    def test_valid_line(self):
        self.assertTrue(self.anagrams.validate("word"))

    def test_invalid_line(self):
        self.assertFalse(self.anagrams.validate("This is not a single word"))
        self.assertFalse(self.anagrams.validate("N3ither%is&this"))


class TestAnagramPopulate(TestAnagram):
    def test_grouping(self):
        self.anagrams.words = ["good", "valid", "words", "doog", "idlav"]

        self.assertTrue(self.anagrams.populate())

        self.assertEqual(
            list(self.anagrams.anagrams.values()),
            [{"good", "doog"}, {"valid", "idlav"}, {"words"}],
        )

    def test_is_anagram(self):
        self.anagrams.words = ["good", "valid", "words"]

        self.assertTrue(self.anagrams.populate())

        for key, group in self.anagrams.anagrams.items():
            sorted_sample = sorted(group.pop())
            self.assertEqual(key, "".join(sorted_sample))

    def test_broken_word(self):
        self.anagrams.words = ["good or not ha!£", "valid", "words"]

        self.assertFalse(self.anagrams.populate())


class TestAnagramPrint(TestAnagram):
    @patch("anagram_parser.anagram_parser.print")
    def test_simple(self, ana_print):
        self.anagrams.anagrams = {"key": {"test"}}

        self.anagrams.print()

        ana_print.assert_called_with("test")

    @patch("anagram_parser.anagram_parser.print")
    def test_words_separated_by_comas_in_group(self, ana_print):
        # Used a list for the grouping here rather than a set to make the test deterministic.
        # It should not have any impact in the grouping.
        self.anagrams.anagrams = {"key": ["test", "estt"]}

        self.anagrams.print()

        ana_print.assert_called_with("test, estt")

    @patch("anagram_parser.anagram_parser.print")
    def test_groups_separated_by_new_line(self, ana_print):
        self.anagrams.anagrams = {"key": {"test"}, "key2": {"test2"}}

        self.anagrams.print()

        self.assertEqual(ana_print.call_args_list, [call("test"), call("test2")])


class TestMain(TestCase):
    def setUp(self):
        pass

    @patch("anagram_parser.anagram_parser.Anagrams")
    @patch("anagram_parser.anagram_parser.sys")
    def test_bad_file_path(self, sys_exit, anagrams):
        args = MagicMock(file_path="test_non_existent_file.txt")

        _main(args)

        anagrams.print.assert_not_called()
        sys_exit.exit.assert_called_with(
            "File not found within path: test_non_existent_file.txt"
        )

    @patch("anagram_parser.anagram_parser.isfile", MagicMock())
    @patch("anagram_parser.anagram_parser.Anagrams")
    @patch("anagram_parser.anagram_parser.sys")
    def test_bad_file(self, sys_exit, anagrams):
        args = MagicMock(file_path="test_file.txt")
        anagrams.return_value = MagicMock(populate=MagicMock(return_value=False))

        _main(args)

        anagrams.print.assert_not_called()
        sys_exit.exit.assert_called_with(
            "Unexpectedly formatted line within file, please ensure the file contains one word per line."
        )

    @patch("anagram_parser.anagram_parser.isfile", MagicMock())
    @patch("anagram_parser.anagram_parser.Anagrams")
    @patch("anagram_parser.anagram_parser.sys")
    def test_pass(self, sys_exit, anagrams):
        args = MagicMock(file_path="test_file.txt")
        anagrams_instance = MagicMock()
        anagrams.return_value = anagrams_instance
        _main(args)

        anagrams.assert_called_with(args.file_path)
        anagrams_instance.populate.assert_called_with()
        anagrams_instance.print.asser_called_with()
