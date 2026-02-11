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


from typing import Dict, Tuple, Optional


class Customer:
    """고객 클래스 - 은행의 고객 정보를 담는 클래스"""

    def __init__(self, _name: str, _account_number: str, _balance: int = 0) -> None:
        self.name: str = _name  # 고객 이름
        self.account_number: str = _account_number  # 계좌번호
        self.balance: int = _balance  # 잔액

    def deposit(self, _amount: int) -> Tuple[bool, str]:
        """입금 - 돈을 계좌에 넣기"""
        # === 내용 써보기! ===
        # 1. _amount가 0보다 작거나 같으면, (False, "입금액은 0보다 커야 합니다.") 를 반환
        # 2. self.balance에 _amount를 더하기
        # 3. (True, "입금 완료 메시지") 반환 (아래 return 참고)
        
        return True, f"{_amount:,}원이 입금되었습니다. 현재 잔액: {self.balance:,}원"

    def withdraw(self, _amount: int) -> Tuple[bool, str]:
        """출금 - 돈을 계좌에서 빼기"""
        # === 내용 써보기! ===
        # 1. _amount가 0보다 작거나 같으면, (False, "출금액은 0보다 커야 합니다.") 를 반환
        # 2. self.balance가 _amount보다 작으면, (False, "잔액이 부족합니다. 현재 잔액: ...") 를 반환
        # 3. self.balance에서 _amount를 빼기
        # 4. (True, "출금 완료 메시지") 반환 (아래 return 참고)
        
        return True, f"{_amount:,}원이 출금되었습니다. 현재 잔액: {self.balance:,}원"

    def get_info(self) -> str:
        """고객 정보를 문자열로 반환"""
        return f"[{self.account_number}] {self.name}님 - 잔액: {self.balance:,}원"


class Bank:
    """은행 클래스 - 여러 고객을 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name  # 은행 이름
        self.customers: Dict[str, Customer] = {}  # 고객들을 저장하는 딕셔너리 {계좌번호: Customer}
        self.next_account_number: int = 1000  # 다음에 발급할 계좌번호

    def create_account(self, _name: str, _initial_deposit: int = 0) -> Tuple[bool, str]:
        """새 계좌 개설"""
        # === 내용 써보기! ===
        # 1. _initial_deposit이 0보다 작으면, (False, "초기 입금액은 0 이상이어야 합니다.") 를 반환
        # 2. account_number 변수를 만들고, str(self.next_account_number)를 저장
        # 3. new_customer 변수를 만들고, Customer(_name, account_number, _initial_deposit)를 저장
        # 4. self.customers[account_number]에 new_customer를 저장
        # 5. self.next_account_number를 1 증가시키기
        # 6. (True, "계좌가 개설되었습니다! 계좌번호: ...") 를 반환 (아래 return 참고)
        
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
        # === 내용 써보기! ===
        # 1. sender 변수를 만들고, self.find_customer(_from_account)를 저장
        # 2. receiver 변수를 만들고, self.find_customer(_to_account)를 저장
        # 3. sender가 None이면, (False, "보내는 계좌를 찾을 수 없습니다.") 를 반환
        # 4. receiver가 None이면, (False, "받는 계좌를 찾을 수 없습니다.") 를 반환
        # 5. success, message 변수를 만들고, sender.withdraw(_amount)를 저장
        # 6. success가 False이면, (False, message)를 반환
        # 7. receiver.deposit(_amount) 실행 (입금)
        # 8. (True, "송금 완료 메시지") 반환 (아래 return 참고)
        
        return True, f"{sender.name}님 → {receiver.name}님에게 {_amount:,}원 송금 완료"

    def get_all_customers(self) -> str:
        """모든 고객 정보를 문자열로 반환"""
        # === 내용 써보기! ===
        # 1. self.customers가 비어있으면, "등록된 고객이 없습니다." 를 반환
        # 2. result 변수를 만들고, f"=== {self.name} 고객 목록 ===\n" 를 저장
        # 3. for customer in self.customers.values(): 로 반복문 시작
        # 4. result에 customer.get_info() + "\n" 를 더하기 (result += ...)
        # 5. result를 반환 (아래 return 참고)
        
        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    bank = Bank("은행이름")  # 은행 개설!

    # === 아래 내용을 채워서 테스트 해보기! ===
    # 1. bank.create_account("홍길동", 10000) 실행하고 결과를 출력
    # 2. bank.create_account("김철수", 20000) 실행하고 결과를 출력
    # 3. bank.get_all_customers() 실행하고 결과를 출력
    # 4. bank.find_customer("1000")을 사용해서 홍길동 고객을 찾기
    # 5. 찾은 고객에게 deposit(5000) 실행
    # 6. bank.transfer("1000", "1001", 3000) 실행 (홍길동 → 김철수에게 송금)
    # 7. bank.get_all_customers() 실행하고 최종 결과 출력