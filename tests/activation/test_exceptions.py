from ville_flexible.activation.exceptions import StrategyNotCoveringRequestedVolumeException


def test_strategy_not_covering_request_volume_exception():
    # Act
    exception = StrategyNotCoveringRequestedVolumeException()

    # Assert
    assert str(exception) == StrategyNotCoveringRequestedVolumeException.MESSAGE
