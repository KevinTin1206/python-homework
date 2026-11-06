"""按作业说明编写的行为测试；不是老师提供的测试。"""

import contextlib
import io
import os
from pathlib import Path
import runpy
import unittest


# 可用环境变量把同一套测试指向老师的原始模板，观察实现前的失败。
module_path = Path(os.environ.get(
    "BANK_MODULE_PATH", str(Path(__file__).resolve().parents[1] / "oo_inheritance.py")
))
import_output = io.StringIO()
with contextlib.redirect_stdout(import_output):
    bank = runpy.run_path(str(module_path))
Account = bank["Account"]
StudentAccount = bank["StudentAccount"]


class AccountTests(unittest.TestCase):
    def test_new_accounts_start_at_zero_and_do_not_share_balance(self):
        first, second = Account("A"), Account("B")
        self.assertEqual(first.owner, "A")
        self.assertEqual(first.balance, 0.0)
        self.assertIsInstance(first.balance, float)
        first.deposit(100)
        self.assertEqual(first.balance, 100.0)
        self.assertEqual(second.balance, 0.0)

    def test_deposit_and_withdraw_accumulate(self):
        account = Account("A")
        account.deposit(100)
        account.deposit(0.5)
        account.withdraw(20.25)
        self.assertEqual(account.balance, 80.25)

    def test_regular_account_can_keep_withdrawing_while_negative(self):
        account = Account("A")
        account.withdraw(100)
        self.assertEqual(account.balance, -100.0)
        account.withdraw(600)
        self.assertEqual(account.balance, -700.0)
        account.deposit(50)
        self.assertEqual(account.balance, -650.0)

    def test_balance_assignment_is_rejected_without_changing_money(self):
        for account in [Account("A"), StudentAccount("S")]:
            with self.subTest(account=type(account).__name__):
                account.deposit(50)
                with self.assertRaises(AttributeError):
                    account.balance = 999
                self.assertEqual(account.balance, 50.0)

    def test_balance_deletion_is_rejected(self):
        account = Account("A")
        account.deposit(10)
        with self.assertRaises(AttributeError):
            del account.balance
        self.assertEqual(account.balance, 10.0)

    def test_negative_amounts_do_not_change_either_account_type(self):
        for cls in [Account, StudentAccount]:
            for method in ["deposit", "withdraw"]:
                with self.subTest(cls=cls.__name__, method=method):
                    account = cls("A")
                    account.deposit(100)
                    with self.assertRaises(ValueError):
                        getattr(account, method)(-100)
                    self.assertEqual(account.balance, 100.0)

    def test_zero_amounts_leave_accounts_unchanged(self):
        for cls in [Account, StudentAccount]:
            account = cls("A")
            account.deposit(0)
            account.withdraw(0)
            self.assertEqual(account.balance, 0.0)

    def test_non_numeric_amounts_are_rejected_without_change(self):
        for amount in ["10", None, True, False, [], 1j]:
            for cls in [Account, StudentAccount]:
                for method in ["deposit", "withdraw"]:
                    with self.subTest(amount=amount, cls=cls.__name__, method=method):
                        account = cls("A")
                        account.deposit(25)
                        with self.assertRaises(TypeError):
                            getattr(account, method)(amount)
                        self.assertEqual(account.balance, 25.0)

    def test_non_finite_amounts_are_rejected_without_change(self):
        for amount in [float("nan"), float("inf"), -float("inf"), 10 ** 1000]:
            for cls in [Account, StudentAccount]:
                for method in ["deposit", "withdraw"]:
                    with self.subTest(amount=amount, cls=cls.__name__, method=method):
                        account = cls("A")
                        account.deposit(25)
                        with self.assertRaises(ValueError):
                            getattr(account, method)(amount)
                        self.assertEqual(account.balance, 25.0)

    def test_float_balance_overflow_does_not_change_balance(self):
        account = Account("A")
        account.deposit(1e308)
        with self.assertRaises(ValueError):
            account.deposit(1e308)
        self.assertEqual(account.balance, 1e308)
        other = Account("B")
        other.withdraw(1e308)
        with self.assertRaises(ValueError):
            other.withdraw(1e308)
        self.assertEqual(other.balance, -1e308)

    def test_student_is_an_account_and_inherits_deposit(self):
        # 继承是本题明确要求的接口，而不是只要行为相似即可。
        self.assertTrue(issubclass(StudentAccount, Account))
        student = StudentAccount("S")
        student.deposit(100)
        student.withdraw(30)
        self.assertEqual(student.owner, "S")
        self.assertEqual(student.balance, 70.0)

    def test_student_can_withdraw_exact_balance(self):
        student = StudentAccount("S")
        student.deposit(100)
        student.withdraw(100)
        self.assertEqual(student.balance, 0.0)

    def test_student_overdraft_raises_without_changing_balance(self):
        student = StudentAccount("S")
        with self.assertRaises(ValueError):
            student.withdraw(1)
        self.assertEqual(student.balance, 0.0)
        student.deposit(100)
        with self.assertRaises(ValueError):
            student.withdraw(100.01)
        self.assertEqual(student.balance, 100.0)

    def test_string_representation_identifies_account_and_balance(self):
        for cls in [Account, StudentAccount]:
            account = cls("Alice")
            account.deposit(12.5)
            text = str(account)
            self.assertIn("Alice", text)
            self.assertIn("12.50", text)

    def test_import_does_not_run_demo(self):
        self.assertEqual(import_output.getvalue(), "")


class TransferTests(unittest.TestCase):
    def test_transfers_work_between_all_account_type_combinations(self):
        for sender_cls in [Account, StudentAccount]:
            for receiver_cls in [Account, StudentAccount]:
                with self.subTest(sender=sender_cls.__name__, receiver=receiver_cls.__name__):
                    sender, receiver = sender_cls("A"), receiver_cls("B")
                    sender.deposit(100)
                    receiver.deposit(5)
                    Account.transfer(25, sender, receiver)
                    self.assertEqual(sender.balance, 75.0)
                    self.assertEqual(receiver.balance, 30.0)

    def test_regular_sender_can_transfer_while_already_overdrawn(self):
        sender, receiver = Account("A"), StudentAccount("S")
        sender.withdraw(100)
        Account.transfer(600, sender, receiver)
        self.assertEqual(sender.balance, -700.0)
        self.assertEqual(receiver.balance, 600.0)

    def test_student_transfer_failure_does_not_credit_receiver(self):
        for receiver_cls in [Account, StudentAccount]:
            sender, receiver = StudentAccount("S"), receiver_cls("B")
            sender.deposit(100)
            receiver.deposit(25)
            with self.assertRaises(ValueError):
                Account.transfer(500000, sender, receiver)
            self.assertEqual(sender.balance, 100.0)
            self.assertEqual(receiver.balance, 25.0)

    def test_student_can_transfer_all_funds_and_zero(self):
        sender, receiver = StudentAccount("S"), Account("B")
        sender.deposit(10)
        Account.transfer(10, sender, receiver)
        Account.transfer(0, sender, receiver)
        self.assertEqual(sender.balance, 0.0)
        self.assertEqual(receiver.balance, 10.0)

    def test_invalid_transfer_amounts_do_not_change_either_balance(self):
        for amount, error in [(-1, ValueError), (float("nan"), ValueError),
                              (float("inf"), ValueError), ("10", TypeError),
                              (None, TypeError), (True, TypeError), (10 ** 1000, ValueError)]:
            with self.subTest(amount=amount):
                sender, receiver = Account("A"), StudentAccount("S")
                sender.deposit(100)
                receiver.deposit(20)
                with self.assertRaises(error):
                    Account.transfer(amount, sender, receiver)
                self.assertEqual(sender.balance, 100.0)
                self.assertEqual(receiver.balance, 20.0)

    def test_invalid_transfer_endpoints_do_not_change_valid_account(self):
        account = Account("A")
        account.deposit(100)
        for sender, receiver in [(account, object()), (object(), account)]:
            with self.assertRaises(TypeError):
                Account.transfer(10, sender, receiver)
            self.assertEqual(account.balance, 100.0)

    def test_same_account_transfer_is_rejected_without_change(self):
        for cls in [Account, StudentAccount]:
            account = cls("A")
            account.deposit(100)
            with self.assertRaises(ValueError):
                Account.transfer(10, account, account)
            self.assertEqual(account.balance, 100.0)

    def test_receiver_overflow_is_rejected_before_sender_is_debited(self):
        sender, receiver = Account("A"), Account("B")
        sender.deposit(100)
        receiver.deposit(1e308)
        with self.assertRaises(ValueError):
            Account.transfer(1e308, sender, receiver)
        self.assertEqual(sender.balance, 100.0)
        self.assertEqual(receiver.balance, 1e308)

    def test_sender_overflow_does_not_credit_receiver(self):
        sender, receiver = Account("A"), Account("B")
        sender.withdraw(1e308)
        with self.assertRaises(ValueError):
            Account.transfer(1e308, sender, receiver)
        self.assertEqual(sender.balance, -1e308)
        self.assertEqual(receiver.balance, 0.0)

    def test_static_method_works_through_an_instance_without_binding_self(self):
        sender, receiver = StudentAccount("S"), Account("B")
        sender.deposit(20)
        sender.transfer(5, sender, receiver)
        self.assertEqual(sender.balance, 15.0)
        self.assertEqual(receiver.balance, 5.0)

    def test_original_demo_has_expected_balances(self):
        first, second = Account("A"), Account("B")
        first.deposit(100)
        second.withdraw(100)
        Account.transfer(600, first, second)
        self.assertEqual(first.balance, -500.0)
        self.assertEqual(second.balance, 500.0)
        student = StudentAccount("S")
        student.deposit(100)
        with self.assertRaises(ValueError):
            Account.transfer(500000, student, first)
        self.assertEqual(student.balance, 100.0)
        self.assertEqual(first.balance, -500.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
