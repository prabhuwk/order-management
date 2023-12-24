from src.symbol_id import SymbolId


class TestSymbolId:
    def test_symbol_id_values(self):
        assert SymbolId["MIDCPNIFTY"].value == "442"
        assert SymbolId["BANKNIFTY"].value == "25"
        assert SymbolId["NIFTY"].value == "13"
        assert SymbolId["FINNIFTY"].value == "27"
        assert SymbolId["SENSEX"].value == "51"
