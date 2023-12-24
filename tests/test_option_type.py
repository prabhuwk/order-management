from src.option_type import OptionType


class TestOptionType:
    def test_option_type_values(self):
        assert OptionType["BUY"].value == "PUT"
        assert OptionType["SELL"].value == "CALL"
