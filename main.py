"""Банковский счёт"""

from decimal import Decimal, ROUND_HALF_UP


class BankAccount:
    """Банковский счёт"""

    accounts_created = 0

    def __init__(
            self,
            account_holder: str,
            account_number: str,
            account_balance: Decimal = 0.00
        ):
        self.account_holder = account_holder
        self.account_number = account_number

        if account_balance < 0:
            raise ValueError("Остаток при открытии счёта не может быть отрицательным")
        else:
            self.account_balance = self._quantize_sum(account_balance)

        BankAccount.accounts_created += 1

    def _quantize_sum(self, value: float) -> Decimal:
        return Decimal(value).quantize(
                    Decimal("0.00"),
                    rounding = ROUND_HALF_UP
                    )

    def deposit(self, amount: float):
       """Пополнение счёта"""
       self.account_balance += self._quantize_sum(amount) 

    def withdraw(self, amount: float):
        if amount > self.account_balance:
            raise ValueError(f"""Сумма не может превышать
доступный остаток на счёте:\n{self.account_balance}""")
        else:
            self.account_balance -= self._quantize_sum(amount)

    def transfer_to(self, other_acc, amount: float):
        if not isinstance(other_acc, BankAccount):
            raise ValueError("Недопустимый счёт для перевода стредств")
        if amount > self.account_balance:
            raise ValueError(f"""Сумма перевода не может превышать
доступный остаток на счёте:\n{self.account_balance}""")
        else:
            transfer_amount = self._quantize_sum(amount)
            self.account_balance -= transfer_amount
            other_acc.account_balance += transfer_amount

    @property
    def info(self):
        return f"""Номер счёта: {self.account_number}\n
Владелец счёта: {self.account_holder}\n
Доступный остаток: {self.account_balance}
                """
    
    @classmethod
    def get_accounts_created(cls):
        return cls.accounts_created

test_account = BankAccount("Василий Патрушев", "acc_10001")
test_acc_2 = BankAccount("Геннадий Пешко", "acc_102001")

test_account.deposit(100000.234)
test_account.transfer_to(test_acc_2, 5000.453)

print(test_account.info)
print(test_acc_2.info)
print(BankAccount.get_accounts_created())
