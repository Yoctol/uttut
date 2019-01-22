import unicodedata

from .add_whitespace_around_character import AddWhitespaceAroundCharacter


class AddWhitespaceAroundPunctuation(AddWhitespaceAroundCharacter):

    def _is_valid_char(self, char: str) -> bool:
        """Checks whether char is a punctuation character.

        This code is copied from Bert `tokenization.py`.

        We treat all non-letter/number ASCII as punctuation.
        Characters such as "^", "$", and "`" are not in the Unicode
        Punctuation class but we treat them as punctuation anyways, for
        consistency.

        """
        code_point = ord(char)
        if ((
                code_point >= 33 and code_point <= 47) or (
                code_point >= 58 and code_point <= 64) or (
                code_point >= 91 and code_point <= 96) or (
                code_point >= 123 and code_point <= 126)
            ):
            return True

        cat = unicodedata.category(char)
        print(cat)
        # For more details, please take a look at
        # https://www.fileformat.info/info/unicode/category/index.htm
        if cat.startswith("P"):
            return True

        return False
