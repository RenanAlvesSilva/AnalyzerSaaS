from django.test import TestCase

class AnalyzeTests(TestCase):
    def test_analyze_view(self):
        response = self.client.get('/api/v1/analyzer/')
        self.assertEqual(response.status_code, 200)
        
    def test_analyze_view(self):
        response = self.client.get('/api/v1/analyzer/32')
        self.assertEqual(response.status_code, 200)
        

   
