from st_nextseq_sample_sheet.utils import remove_special_chars


class TestRemoveSpecialChars:
    # The function should remove all special characters from the input string and return the modified string.
    def test_remove_special_chars_remove_all_special_chars(self):
        # Arrange
        sample_id = "abc!@#$%^&*()123"
        expected_result = "abc123"
        replace_char = ""
        # Act
        result = remove_special_chars(sample_id, replace_char)

        # Assert
        assert result == expected_result

    # The function should replace special characters with the specified replace_char if provided.
    def test_remove_special_chars_replace_special_chars(self):
        # Arrange
        sample_id = "abc!@*123"
        replace_char = "-"
        expected_result = "abc---123"

        # Act
        result = remove_special_chars(sample_id, replace_char)

        # Assert
        assert result == expected_result

    def test_remove_unicode_chars(self):
        # Arrange
        sample_id = "abc!@*êấ123"
        replace_char = ""
        expected_result = "abc123"

        # Act
        result = remove_special_chars(sample_id, replace_char)

        # Assert
        assert result == expected_result
