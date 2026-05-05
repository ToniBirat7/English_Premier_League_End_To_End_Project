from django.test import TestCase
from unittest.mock import patch, MagicMock
from . import services


class PredictionServiceTests(TestCase):
    @patch('football_api.services.requests.post')
    def test_predict_match_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'prob_H': 0.65,
            'prob_NH': 0.35,
            'prediction': 'H',
            'model_version': '2',
        }
        mock_post.return_value = mock_response

        result = services.predict_match('Arsenal', 'Chelsea', '2023-24', 10)

        assert result is not None
        assert result['prob_H'] == 0.65
        assert result['prediction'] == 'H'
        mock_post.assert_called_once()

    @patch('football_api.services.requests.post')
    def test_predict_match_timeout(self, mock_post):
        mock_post.side_effect = Exception("Connection timeout")

        result = services.predict_match('Arsenal', 'Chelsea', '2023-24', 10)

        assert result is None
