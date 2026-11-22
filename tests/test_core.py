import unittest
from consentgate.core import Gate, GateError


class GateTests(unittest.TestCase):
    def setUp(self):
        self.gate = Gate(secret='test-secret')
        self.task = self.gate.issue_task('tenant-a', 'cust-1', 'order-101', 'ORDER_STATUS')

    def test_minimal_order_result(self):
        result = self.gate.access(self.task, 'get_order_status', 'order-101')
        self.assertEqual(set(result['data']), {'status', 'delivery_window'})
        self.assertNotIn('email', str(result['data']))

    def test_profile_is_denied(self):
        with self.assertRaises(GateError):
            self.gate.access(self.task, 'get_customer_profile', 'cust-1')

    def test_cross_customer_and_tenant_are_denied(self):
        for target in ('order-202', 'order-301'):
            with self.assertRaises(GateError):
                self.gate.access(self.task, 'get_order_status', target)

    def test_tampered_token_is_denied(self):
        with self.assertRaises(GateError):
            self.gate.access(self.task + 'x', 'get_order_status', 'order-101')

    def test_revocation_blocks_existing_task(self):
        self.gate.revoke('tenant-a', 'cust-1')
        with self.assertRaises(GateError):
            self.gate.access(self.task, 'get_order_status', 'order-101')

    def test_expired_task_is_denied(self):
        token = self.gate.issue_task('tenant-a', 'cust-1', 'order-101', 'ORDER_STATUS', ttl=-1)
        with self.assertRaises(GateError):
            self.gate.access(token, 'get_order_status', 'order-101')

    def test_audit_tamper_is_detected(self):
        self.gate.access(self.task, 'get_order_status', 'order-101')
        self.assertTrue(self.gate.verify_audit())
        self.gate.audit[0]['decision'] = 'DENY'
        self.assertFalse(self.gate.verify_audit())


if __name__ == '__main__':
    unittest.main()
