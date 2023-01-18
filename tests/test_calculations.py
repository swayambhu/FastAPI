from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 2, 5),
    (7, 1, 8),
    (12, 4, 16)
])
def test_add(num1, num2, expected):
    print('Testing add function')
    assert add(num1, num2) == expected
    
def test_subtract():
    print('Testing subtract function')
    assert subtract(3, 5) == 2
    
def test_multiply():
    print('Testing multiply function')
    assert multiply(5, 3) == 15

def test_divide():
    print('Testing divide function')
    assert divide(3, 15) == 5
    

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw_amount(bank_account):
    bank_account.withdraw(5)
    assert bank_account.balance == 45
    
    
def test_deposit_amount(bank_account):
    bank_account.deposit(5)
    assert bank_account.balance == 55
    
def test_add_interest_amount(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
    
    

@pytest.mark.parametrize("deposit, withdraw, balance", [
    (200, 100, 100),
    (50, 10, 40),
    (250, 10, 240),
])    
def test_bank_transaction(zero_bank_account, deposit, withdraw, balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == balance
    

@pytest.mark.parametrize("withdraw", [
    (200),
    (51),
    (250),
])  
def test_insufficient_funds(bank_account, withdraw):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(withdraw)