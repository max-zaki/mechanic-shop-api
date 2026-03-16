import unittest
import json
from app import create_app
from app.models import db


class TestInventory(unittest.TestCase):

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

    def _create_part(self, name="Oil Filter", price=12.99):
        return self.client.post('/inventory/', json={
            "name": name,
            "price": price
        })

    # ── POST /inventory/ ──────────────────────────────────────

    def test_create_part_success(self):
        resp = self._create_part()
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Oil Filter')
        self.assertEqual(data['price'], 12.99)

    def test_create_part_missing_name(self):
        resp = self.client.post('/inventory/', json={"price": 9.99})
        self.assertEqual(resp.status_code, 400)

    def test_create_part_missing_price(self):
        resp = self.client.post('/inventory/', json={"name": "Spark Plug"})
        self.assertEqual(resp.status_code, 400)

    def test_create_part_empty_body(self):
        resp = self.client.post('/inventory/', json={})
        self.assertEqual(resp.status_code, 400)

    # ── GET /inventory/ ───────────────────────────────────────

    def test_get_all_parts(self):
        self._create_part()
        self._create_part("Brake Pad Set", 45.00)
        resp = self.client.get('/inventory/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_all_parts_empty(self):
        resp = self.client.get('/inventory/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), [])

    # ── GET /inventory/<id> ───────────────────────────────────

    def test_get_part_by_id(self):
        self._create_part()
        resp = self.client.get('/inventory/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['name'], 'Oil Filter')

    def test_get_part_not_found(self):
        resp = self.client.get('/inventory/999')
        self.assertEqual(resp.status_code, 404)

    # ── PUT /inventory/<id> ───────────────────────────────────

    def test_update_part(self):
        self._create_part()
        resp = self.client.put('/inventory/1', json={
            "name": "Premium Oil Filter",
            "price": 18.99
        })
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Premium Oil Filter')
        self.assertEqual(data['price'], 18.99)

    def test_update_part_not_found(self):
        resp = self.client.put('/inventory/999', json={
            "name": "Ghost Part",
            "price": 0.0
        })
        self.assertEqual(resp.status_code, 404)

    def test_update_part_missing_price(self):
        self._create_part()
        resp = self.client.put('/inventory/1', json={"name": "No Price"})
        self.assertEqual(resp.status_code, 400)

    # ── DELETE /inventory/<id> ────────────────────────────────

    def test_delete_part(self):
        self._create_part()
        resp = self.client.delete('/inventory/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('message', data)

    def test_delete_part_not_found(self):
        resp = self.client.delete('/inventory/999')
        self.assertEqual(resp.status_code, 404)

    def test_deleted_part_no_longer_accessible(self):
        self._create_part()
        self.client.delete('/inventory/1')
        resp = self.client.get('/inventory/1')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
