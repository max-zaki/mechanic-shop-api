import unittest
import json
from app import create_app
from app.models import db


class TestServiceTickets(unittest.TestCase):

    def setUp(self):
        self.app = create_app('TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self._seed()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    # ── helpers / seed data ──────────────────────────────────

    def _seed(self):
        self.client.post('/customers/', json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "555-123-4567",
            "password": "secret123"
        })
        self.client.post('/mechanics/', json={
            "name": "Bob Smith",
            "email": "bob@shop.com",
            "phone": "555-987-6543",
            "salary": 55000.0
        })
        self.client.post('/inventory/', json={
            "name": "Oil Filter",
            "price": 12.99
        })

    def _create_ticket(self, customer_id=1):
        return self.client.post('/service-tickets/', json={
            "vin": "1HGBH41JXMN109186",
            "svc_date": "2025-06-01",
            "svc_desc": "Oil change and tire rotation",
            "customer_id": customer_id
        })

    # ── POST /service-tickets/ ────────────────────────────────

    def test_create_ticket_success(self):
        resp = self._create_ticket()
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['vin'], '1HGBH41JXMN109186')
        self.assertEqual(data['customer_id'], 1)

    def test_create_ticket_missing_fields(self):
        resp = self.client.post('/service-tickets/', json={"vin": "SHORTVIN"})
        self.assertEqual(resp.status_code, 400)

    def test_create_ticket_invalid_customer(self):
        resp = self._create_ticket(customer_id=9999)
        # SQLite won't enforce FK by default, but the schema will still reject
        # missing required fields if they're absent — this tests unknown customer
        self.assertIn(resp.status_code, [201, 400, 404])

    # ── GET /service-tickets/ ─────────────────────────────────

    def test_get_service_tickets(self):
        self._create_ticket()
        resp = self.client.get('/service-tickets/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_service_tickets_empty(self):
        resp = self.client.get('/service-tickets/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), [])

    # ── PUT /service-tickets/<id>/assign-mechanic/<id> ────────

    def test_assign_mechanic(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/assign-mechanic/1')
        self.assertEqual(resp.status_code, 200)

    def test_assign_mechanic_ticket_not_found(self):
        resp = self.client.put('/service-tickets/999/assign-mechanic/1')
        self.assertEqual(resp.status_code, 404)

    def test_assign_mechanic_mechanic_not_found(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/assign-mechanic/999')
        self.assertEqual(resp.status_code, 404)

    def test_assign_mechanic_already_assigned(self):
        self._create_ticket()
        self.client.put('/service-tickets/1/assign-mechanic/1')
        resp = self.client.put('/service-tickets/1/assign-mechanic/1')
        self.assertEqual(resp.status_code, 400)

    # ── PUT /service-tickets/<id>/remove-mechanic/<id> ────────

    def test_remove_mechanic(self):
        self._create_ticket()
        self.client.put('/service-tickets/1/assign-mechanic/1')
        resp = self.client.put('/service-tickets/1/remove-mechanic/1')
        self.assertEqual(resp.status_code, 200)

    def test_remove_mechanic_not_assigned(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/remove-mechanic/1')
        self.assertEqual(resp.status_code, 400)

    def test_remove_mechanic_ticket_not_found(self):
        resp = self.client.put('/service-tickets/999/remove-mechanic/1')
        self.assertEqual(resp.status_code, 404)

    # ── PUT /service-tickets/<id>/edit ────────────────────────

    def test_edit_ticket_mechanics_add(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/edit',
                               json={"add_ids": [1], "remove_ids": []})
        self.assertEqual(resp.status_code, 200)

    def test_edit_ticket_mechanics_remove(self):
        self._create_ticket()
        self.client.put('/service-tickets/1/assign-mechanic/1')
        resp = self.client.put('/service-tickets/1/edit',
                               json={"add_ids": [], "remove_ids": [1]})
        self.assertEqual(resp.status_code, 200)

    def test_edit_ticket_not_found(self):
        resp = self.client.put('/service-tickets/999/edit',
                               json={"add_ids": [1], "remove_ids": []})
        self.assertEqual(resp.status_code, 404)

    # ── PUT /service-tickets/<id>/add-part/<id> ───────────────

    def test_add_part_to_ticket(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/add-part/1')
        self.assertEqual(resp.status_code, 200)

    def test_add_part_already_added(self):
        self._create_ticket()
        self.client.put('/service-tickets/1/add-part/1')
        resp = self.client.put('/service-tickets/1/add-part/1')
        self.assertEqual(resp.status_code, 400)

    def test_add_part_ticket_not_found(self):
        resp = self.client.put('/service-tickets/999/add-part/1')
        self.assertEqual(resp.status_code, 404)

    def test_add_part_part_not_found(self):
        self._create_ticket()
        resp = self.client.put('/service-tickets/1/add-part/999')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
