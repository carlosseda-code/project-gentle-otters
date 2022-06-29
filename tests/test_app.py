import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Carlos Seda</title>" in html 
        assert "High school" in html 
        assert "May 2020 - August 2020" in html
        assert "email@email.com" in html        
    
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        response = self.client.post("/api/timeline_post", data={
            'name': 'Daisy',
            'email': 'daisy@gmail.com',
            'content': 'Test for post'
        })
        assert response.status_code == 200
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Daisy"
        assert json["timeline_posts"][0]["email"] == "daisy@gmail.com"
        assert json["timeline_posts"][0]["content"] == "Test for post"

        response = self.client.post("/api/timeline_post", data={
            'name': 'Jenna',
            'email': 'jenna@gmail.com',
            'content': 'Test for post 2'
        })
        assert response.status_code == 200
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 2
        assert json["timeline_posts"][0]["name"] == "Jenna"
        assert json["timeline_posts"][0]["email"] == "jenna@gmail.com"
        assert json["timeline_posts"][0]["content"] == "Test for post 2"

        response = self.client.get("/timeline")
        html = response.get_data(as_text=True)
        assert "<title>Timeline</title>" in html 
        assert "List of Timeline Posts" in html 
