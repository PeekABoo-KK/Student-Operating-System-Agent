import requests

SERVER_URL = "http://localhost:8000"

class ScholarshipClient:

    def search(self, profile):
        res = requests.post(
            f"{SERVER_URL}/search_scholarships",
            json=profile
        )
        return res.json()

    def rank(self, scholarships):
        res = requests.post(
            f"{SERVER_URL}/rank_scholarships",
            json={"scholarships": scholarships}
        )
        return res.json()
