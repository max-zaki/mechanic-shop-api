import unittest
import json
from app import create_app
from app.models import db


class TestMechanics(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ── helpers ──────────────────────────────────────────────

    def _create_mechanic(self, name="Bob Smith", email="bob@shop.com"):
        return self.client.post('/mechanics/', json={
            "name": name,
            "email": email,
            "phone": "555-987-6543",
            "salary": 55000.0
        })

    # ── POST /mechanics/ ──────────────────────────────────────

    def test_create_mechanic_success(self):
        resp = self._create_mechanic()
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Bob Smith')
        self.assertEqual(data['salary'], 55000.0)

    def test_create_mechanic_missing_fields(self):
        resp = self.client.post('/mechanics/', json={"name": "Bob"})
        self.assertEqual(resp.status_code, 400)

    def test_create_mechanic_missing_salary(self):
        resp = self.client.post('/mechanics/', json={
            "name": "Bob Smith",
            "email": "bob@shop.com",
            "phone": "555-987-6543"
        })
        self.assertEqual(resp.status_code, 400)

    # ── GET /mechanics/ ───────────────────────────────────────

    def test_get_mechanics(self):
        self._create_mechanic()
        resp = self.client.get('/mechanics/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_mechanics_empty(self):
        resp = self.client.get('/mechanics/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), [])

    # ── GET /mechanics/most-worked ────────────────────────────

    def test_most_worked_mechanics(self):
        self._create_mechanic("Alice", "alice@shop.com")
        self._create_mechanic("Bob", "bob@shop.com")
        resp = self.client.get('/mechanics/most-worked')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_most_worked_mechanics_empty(self):
        resp = self.client.get('/mechanics/most-worked')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), [])

    # ── PUT /mechanics/<id> ───────────────────────────────────

    def test_update_mechanic(self):
        self._create_mechanic()
        resp = self.client.put('/mechanics/1', json={
            "name": "Bob Updated",
            "email": "bobupdated@shop.com",
            "phone": "555-000-1111",
            "salary": 60000.0
        })
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Bob Updated')
        self.assertEqual(data['salary'], 60000.0)

    def test_update_mechanic_not_found(self):
        resp = self.client.put('/mechanics/999', json={
            "name": "Ghost",
            "email": "ghost@shop.com",
            "phone": "000-000-0000",
            "salary": 0.0
        })
        self.assertEqual(resp.status_code, 404)

    def test_update_mechanic_invalid_data(self):
        self._create_mechanic()
        resp = self.client.put('/mechanics/1', json={"name": "No salary"})
        self.assertEqual(resp.status_code, 400)

    # ── DELETE /mechanics/<id> ────────────────────────────────

    def test_delete_mechanic(self):
        self._create_mechanic()
        resp = self.client.delete('/mechanics/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('message', data)

    def test_delete_mechanic_not_found(self):
        resp = self.client.delete('/mechanics/999')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
