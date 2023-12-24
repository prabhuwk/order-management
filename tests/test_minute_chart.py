from src.minute_chart import MinuteChart


class TestMinuteChart:
    def test_intraday(self, mock_dhan_client, mock_minute_chart):
        minute_chart = MinuteChart(dhan_client=mock_dhan_client)
        mock_dhan_client.intraday_daily_minute_charts.return_value = mock_minute_chart
        output = minute_chart.intraday(security_id="12345")
        assert len(output) == 6
        assert "close" in output.keys()
