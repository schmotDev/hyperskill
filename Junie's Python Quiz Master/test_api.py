import unittest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

class TestQuizAPI(unittest.TestCase):
    def test_get_questions(self):
        response = client.get("/questions")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertGreater(len(response.json()), 0)
        # Check that 'answer' is not in the response
        self.assertNotIn("answer", response.json()[0])

    def test_get_random_question(self):
        response = client.get("/questions/random")
        self.assertEqual(response.status_code, 200)
        self.assertIn("question", response.json())
        self.assertIn("options", response.json())
        self.assertNotIn("answer", response.json())

    def test_verify_correct_answer(self):
        # We know question 1 answer is 'b'
        response = client.post("/verify", json={"question_id": 1, "answer": "b"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["correct"])
        self.assertEqual(data["message"], "Correct! Well done.")

    def test_verify_wrong_answer(self):
        # We know question 1 answer is 'b', so 'a' is wrong
        response = client.post("/verify", json={"question_id": 1, "answer": "a"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["correct"])
        self.assertEqual(data["correct_answer"], "b")

    def test_verify_invalid_question(self):
        response = client.post("/verify", json={"question_id": 999, "answer": "a"})
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
