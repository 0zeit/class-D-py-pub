import sys
from typing import Dict, Tuple, Optional

class Customer:
    """고객 클래스 - 은행의 고객 정보를 담는 클래스"""

    def __init__(self, _name: str, _account_number: str, _balance: int = 0) -> None:
        self.name: str = _name  # 고객 이름
        self.account_number: str = _account_number  # 계좌번호
        self.balance: int = _balance  # 잔액

    def deposit(self, _amount: int) -> Tuple[bool, str]:
        """입금 - 돈을 계좌에 넣기"""
        if _amount <= 0:
            return False, "입금액은 0보다 커야 합니다."

        self.balance += _amount

        return True, f"{_amount:,}원이 입금되었습니다. 현재 잔액: {self.balance:,}원"

    def withdraw(self, _amount: int) -> Tuple[bool, str]:
        """출금 - 돈을 계좌에서 빼기"""
        if _amount <= 0:
            return False, "출금액은 0보다 커야 합니다."

        if self.balance < _amount:
            return False, f"잔액이 부족합니다. 현재 잔액: {self.balance:,}원"

        self.balance -= _amount

        return True, f"{_amount:,}원이 출금되었습니다. 현재 잔액: {self.balance:,}원"

    def get_info(self) -> str:
        """고객 정보를 문자열로 반환"""
        return f"[{self.account_number}] {self.name}님 - 잔액: {self.balance:,}원"


class Bank:
    """은행 클래스 - 여러 고객을 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name  # 은행 이름
        self.customers: Dict[str, Customer] = ( # 고객들을 저장하는 딕셔너리 {계좌번호: Customer}
            {}
        )
        self.next_account_number: int = 1000  # 다음에 발급할 계좌번호

    def create_account(self, _name: str, _initial_deposit: int = 0) -> Tuple[bool, str]:
        """새 계좌 개설"""
        if _initial_deposit < 0:
            return False, "초기 입금액은 0 이상이어야 합니다."

        account_number: str = str(self.next_account_number)
        new_customer: Customer = Customer(_name, account_number, _initial_deposit)

        self.customers[account_number] = new_customer
        self.next_account_number += 1

        return True, f"계좌가 개설되었습니다! 계좌번호: {account_number}"

    def find_customer(self, _account_number: str) -> Optional[Customer]:
        """계좌번호로 고객 찾기"""
        if _account_number in self.customers:
            return self.customers[_account_number]

        return None

    def transfer(
        self, _from_account: str, _to_account: str, _amount: int
    ) -> Tuple[bool, str]:
        """송금 - 한 계좌에서 다른 계좌로 돈 보내기"""
        sender: Optional[Customer] = self.find_customer(_from_account)
        receiver: Optional[Customer] = self.find_customer(_to_account)

        if sender is None:
            return False, "보내는 계좌를 찾을 수 없습니다."

        if receiver is None:
            return False, "받는 계좌를 찾을 수 없습니다."

        # 출금 시도
        success: bool
        message: str
        success, message = sender.withdraw(_amount)

        if not success:
            return False, message

        # 입금
        receiver.deposit(_amount)

        return True, f"{sender.name}님 → {receiver.name}님에게 {_amount:,}원 송금 완료"

    def get_all_customers(self) -> str:
        """모든 고객 정보를 문자열로 반환"""
        if not self.customers:
            return "등록된 고객이 없습니다."

        result: str = f"=== {self.name} 고객 목록 ===\n"

        for customer in self.customers.values():
            result += customer.get_info() + "\n"

        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    bank = Bank("으악")
    
    new_customer = bank.create_account("홍길동")
    # 이것저것 해보기!
