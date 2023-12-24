from src.target import SellTarget, TargetFactory


class TestTargetFactory:
    def test_get_target(self, mock_minute_chart, sell_candle):
        target_factory = TargetFactory.get_target(
            signal="SELL",
            current_candle=mock_minute_chart["data"],
            ordered_candle=sell_candle,
            percent=80,
        )
        assert type(target_factory) == SellTarget
