import sys
from typing import Dict, Tuple, Optional

# 만들어보기!
# 클래스(Class)
#   은행(Bank)
#       __init__()
#       create_account()
#       find_customer()
#       transfer()
#       get_all_customers()
#
#   고객(Customer)
#       __init__()
#       deposit()
#       withdraw()
#       get_info()


class Customer:
    """고객 클래스 - 은행의 고객 정보를 담는 클래스"""

    def __init__(self, _name: str, _account_number: str, _balance: int = 0) -> None:
        self.name: str = _name  # 고객 이름
        self.account_number: str = _account_number  # 계좌번호
        self.balance: int = _balance  # 잔액

    def deposit(self, _amount: int) -> Tuple[bool, str]:
        """입금 - 돈을 계좌에 넣기"""
        # 내용 써보기!
        return True, f"{_amount:,}원이 입금되었습니다. 현재 잔액: {self.balance:,}원"

    def withdraw(self, _amount: int) -> Tuple[bool, str]:
        """출금 - 돈을 계좌에서 빼기"""
        # 내용 써보기!
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
        # 내용 써보기!
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
        # 내용 써보기!
        return True, f"{sender.name}님 → {receiver.name}님에게 {_amount:,}원 송금 완료"

    def get_all_customers(self) -> str:
        """모든 고객 정보를 문자열로 반환"""
        # 내용 써보기!
        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    bank = Bank("으악") # 은행 개설!
    
    new_customer = bank.create_account("홍길동") # 만들어진 은행 시스템으로 계좌 만들기
    # 이것저것 해보기!
