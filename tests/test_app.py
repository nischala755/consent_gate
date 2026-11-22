import unittest
from fastapi.testclient import TestClient
from consentgate.app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.client.post('/api/reset')

    def test_health_and_demo(self):
        self.assertEqual(self.client.get('/health').status_code, 200)
        response = self.client.post('/api/demo/counterfactual', json={'order_id': 'order-101'})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(set(body['protected']['data']), {'status', 'delivery_window'})
        self.assertIn('email', body['baseline']['data'])

    def test_mid_run_revocation(self):
        task = self.client.post('/api/tasks', json={'order_id': 'order-101'}).json()['token']
        self.assertEqual(self.client.post('/api/access', json={'token': task, 'operation': 'get_order_status', 'target': 'order-101'}).status_code, 200)
        self.assertEqual(self.client.post('/api/consent/revoke', json={'customer_id': 'cust-1', 'tenant_id': 'tenant-a'}).status_code, 200)
        self.assertEqual(self.client.post('/api/access', json={'token': task, 'operation': 'get_order_status', 'target': 'order-101'}).status_code, 403)

    def test_scored_scenarios(self):
        result = self.client.get('/api/evaluate').json()
        self.assertEqual(result['failed'], 0)
        self.assertGreaterEqual(result['passed'], 6)


if __name__ == '__main__':
    unittest.main()

