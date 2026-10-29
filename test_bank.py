
import pytest
from bank import Bank


@pytest.fixture
def bank_setup(tmp_path, monkeypatch):
    # Use a temporary file so your real data.json stays unchanged.
    monkeypatch.setattr(Bank, "database", str(tmp_path / "test_data.json"))
    monkeypatch.setattr(Bank, "data", [])
    return Bank()


def test_create_account(bank_setup):
    bank = bank_setup

    success, result = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )

    assert success is True
    assert result["name"] == "Test User"
    assert result["balance"] == 0


def test_reject_underage_account(bank_setup):
    bank = bank_setup

    success, result = bank.createAccount(
        "Test User", 17, "test@example.com", "1234"
    )

    assert success is False
    assert result == "You must be at least 18 years old"


def test_deposit_money(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    success, balance = bank.depositMoney(
        account["account number"], "1234", 500
    )

    assert success is True
    assert balance == 500


def test_reject_invalid_deposit(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    success, result = bank.depositMoney(
        account["account number"], "1234", 0
    )

    assert success is False
    assert "Deposit must be between" in result



def test_withdraw_money(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    # Deposit Rs. 1000 first
    success, balance = bank.depositMoney(
        account["account number"], "1234", 1000
    )
    assert success is True

    # Withdraw Rs. 400
    success, balance = bank.withdrawMoney(
        account["account number"], "1234", 400
    )

    assert success is True
    assert balance == 600


def test_incorrect_pin(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    success, result = bank.depositMoney(
        account["account number"], "9999", 500
    )

    assert success is False
    assert result == "No such account found"


def test_update_account_name(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    success, result = bank.updateDetails(
        account["account number"],
        "1234",
        newName="Updated User"
    )

    assert success is True

    details = bank.showDetails(
        account["account number"], "1234"
    )
    assert details["name"] == "Updated User"


def test_delete_account(bank_setup):
    bank = bank_setup

    success, account = bank.createAccount(
        "Test User", 22, "test@example.com", "1234"
    )
    assert success is True

    # Your application requires a balance of exactly Rs. 100
    bank.depositMoney(
        account["account number"], "1234", 100
    )

    success, result = bank.deleteAccount(
        account["account number"], "1234"
    )

    assert success is True
    assert result == "Your account is deleted successfully"
