from src.strike_price import StrikePrice


class TestStrikePrice:
    def test_init(self):
        strik_price = StrikePrice("NIFTY", 20650.2, "PUT")
        assert strik_price.current == 20650
        assert strik_price.required == 20600
