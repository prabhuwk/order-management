from src.positions import Positions


class TestPositions:
    def test_init(self, mock_dhan_client):
        self.positions = Positions(dhan_client=mock_dhan_client)
        assert type(self.positions) == Positions

    def test_get(self, mock_dhan_client, mock_positions_output):
        mock_positions = Positions(dhan_client=mock_dhan_client)
        assert mock_positions.get is None
        mock_dhan_client.get_positions.return_value = mock_positions_output
        assert len(mock_positions.get) == 1

    def test_spot_exists(self, mock_dhan_client, mock_positions_output):
        mock_positions = Positions(dhan_client=mock_dhan_client)
        mock_position_type = mock_positions_output["data"][0]["positionType"]
        mock_dhan_client.get_positions.return_value = mock_positions_output
        assert (
            mock_positions.spot_exists(
                symbol_name="MIDCPNIFTY", position_type=mock_position_type
            )
            is True
        )

    def test_strike_exists(self, mock_dhan_client, mock_positions_output):
        mock_positions = Positions(dhan_client=mock_dhan_client)
        mock_security_id = mock_positions_output["data"][0]["securityId"]
        mock_position_type = mock_positions_output["data"][0]["positionType"]
        mock_dhan_client.get_positions.return_value = mock_positions_output
        assert (
            mock_positions.strike_exists(
                security_id=mock_security_id, position_type=mock_position_type
            )
            is True
        )
