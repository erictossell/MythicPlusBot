from unittest import TestCase
from raiderIO import get_score_colors
from util import binary_search_score_colors

class TestBinarySearch(TestCase):
    
    def test_always_fail(self):
        self.assertTrue(False)
    
    def test_binary_search_score_colors_200(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 200)
        assert result == '#ffffff'
    
    def test_binary_search_score_colors_3500(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 3500)
        assert result == '#ff8000'
        
    def test_binary_search_score_colors_5000(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 5000)
        assert result == '#ff8000'
        
    def test_binary_search_score_colors_0(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 0)
        assert result == '#ffffff'
        
    def test_binary_search_score_colors_207(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 207)
        assert result == '#ffffff'
    
    def test_binary_search_score_colors_301(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 301)
        assert result == '#eaffe0'
        
    def test_binary_search_score_colors_500(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 500)
        assert result == '#baffa2'
        
    def test_binary_search_score_colors_1000(self):
        scoreColors = get_score_colors()
        result = binary_search_score_colors(scoreColors, 1000)
        assert result == '#45ec46'