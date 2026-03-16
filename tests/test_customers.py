import unittest
import json
from app import create_app
from app.models import db, Customer


class TestCustomers(unittest.TestCase):

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

    def _create_customer(self, email="jane@example.com"):
        return self.client.post('/customers/', json={
            "name": "Jane Doe",
            "email": email,
            "phone": "555-123-4567",
            "password": "secret123"
        })

    def _login(self, email="jane@example.com", password="secret123"):
        return self.client.post('/customers/login', json={
            "email": email,
            "password": password
        })

    def _get_token(self, email="jane@example.com"):
        self._create_customer(email)
        resp = self._login(email)
        return json.loads(resp.data)['token']

    # ── POST /customers/ ─────────────────────────────────────

    def test_create_customer_success(self):
        resp = self._create_customer()
        self.assertEqual(resp.status_code, 201)
        data = json.loads(resp.data)
        self.assertEqual(data['email'], 'jane@example.com')

    def test_create_customer_duplicate_email(self):
        self._create_customer()
        resp = self._create_customer()
        self.assertEqual(resp.status_code, 400)
        data = json.loads(resp.data)
        self.assertIn('error', data)

    def test_create_customer_missing_fields(self):
        resp = self.client.post('/customers/', json={"email": "x@x.com"})
        self.assertEqual(resp.status_code, 400)

    # ── POST /customers/login ─────────────────────────────────

    def test_login_success(self):
        self._create_customer()
        resp = self._login()
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('token', data)
        self.assertEqual(data['status'], 'success')

    def test_login_wrong_password(self):
        self._create_customer()
        resp = self._login(password="wrongpassword")
        self.assertEqual(resp.status_code, 401)

    def test_login_nonexistent_email(self):
        resp = self._login(email="nobody@example.com")
        self.assertEqual(resp.status_code, 401)

    # ── GET /customers/ ───────────────────────────────────────

    def test_get_customers(self):
        self._create_customer()
        resp = self.client.get('/customers/')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_customers_empty(self):
        resp = self.client.get('/customers/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.data), [])

    # ── GET /customers/<id> ───────────────────────────────────

    def test_get_customer_by_id(self):
        self._create_customer()
        resp = self.client.get('/customers/1')
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['id'], 1)

    def test_get_customer_not_found(self):
        resp = self.client.get('/customers/999')
        self.assertEqual(resp.status_code, 404)

    # ── GET /customers/my-tickets ─────────────────────────────

    def test_get_my_tickets_authenticated(self):
        token = self._get_token()
        resp = self.client.get('/customers/my-tickets',
                               headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(json.loads(resp.data), list)

    def test_get_my_tickets_no_token(self):
        resp = self.client.get('/customers/my-tickets')
        self.assertEqual(resp.status_code, 401)

    def test_get_my_tickets_invalid_token(self):
        resp = self.client.get('/customers/my-tickets',
                               headers={"Authorization": "Bearer badtoken"})
        self.assertEqual(resp.status_code, 401)

    # ── PUT /customers/ ───────────────────────────────────────

    def test_update_customer(self):
        token = self._get_token()
        resp = self.client.put('/customers/', json={
            "name": "Jane Updated",
            "email": "jane@example.com",
            "phone": "555-000-0000",
            "password": "newpassword"
        }, headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertEqual(data['name'], 'Jane Updated')

    def test_update_customer_no_token(self):
        resp = self.client.put('/customers/', json={
            "name": "Jane Updated",
            "email": "jane@example.com",
            "phone": "555-000-0000",
            "password": "newpassword"
        })
        self.assertEqual(resp.status_code, 401)

    # ── DELETE /customers/ ────────────────────────────────────

    def test_delete_customer(self):
        token = self._get_token()
        resp = self.client.delete('/customers/',
                                  headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data)
        self.assertIn('message', data)

    def test_delete_customer_no_token(self):
        resp = self.client.delete('/customers/')
        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()
