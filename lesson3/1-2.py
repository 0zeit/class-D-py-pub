import sys
from typing import Dict, Tuple, Optional, List

# 만들어보기!
# 클래스(Class)
#   카페(Cafe)
#       __init__()
#       register_customer()
#       find_customer()
#       order()
#       show_menu()
#       get_all_customers()
#
#   고객(Customer)
#       __init__()
#       earn_points()
#       use_points()
#       get_info()


from typing import Dict, Tuple, Optional, List


class Customer:
    """고객 클래스 - 카페의 고객 정보를 담는 클래스"""

    def __init__(self, _name: str, _customer_id: str, _points: int = 0) -> None:
        self.name: str = _name  # 고객 이름
        self.customer_id: str = _customer_id  # 고객 번호
        self.points: int = _points  # 포인트
        self.order_history: List[str] = []  # 주문 내역

    def earn_points(self, _amount: int) -> Tuple[bool, str]:
        """포인트 적립 - 주문 금액의 10%를 포인트로 적립"""
        # === 내용 써보기! ===
        # 1. earned_points 변수를 만들고, _amount를 10으로 나눈 값을 저장 (_amount // 10)
        # 2. self.points에 earned_points를 더하기
        # 3. (True, "포인트 적립 메시지") 반환 (아래 return 참고)
        
        return True, f"{earned_points}P 적립되었습니다! 현재 포인트: {self.points}P"

    def use_points(self, _points: int) -> Tuple[bool, str]:
        """포인트 사용 - 보유한 포인트로 할인 받기"""
        # === 내용 써보기! ===
        # 1. _points가 0보다 작거나 같으면, (False, "사용할 포인트는 0보다 커야 합니다.") 를 반환
        # 2. self.points가 _points보다 작으면, (False, "포인트가 부족합니다. 현재 포인트: ...") 를 반환
        # 3. self.points에서 _points를 빼기
        # 4. (True, "포인트 사용 메시지") 반환 (아래 return 참고)
        
        return True, f"{_points}P 사용했습니다. 남은 포인트: {self.points}P"

    def get_info(self) -> str:
        """고객 정보를 문자열로 반환"""
        return f"[{self.customer_id}] {self.name}님 - 포인트: {self.points}P"


class Cafe:
    """카페 클래스 - 여러 고객과 메뉴를 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name  # 카페 이름
        self.customers: Dict[str, Customer] = {}  # 고객들을 저장하는 딕셔너리 {고객번호: Customer}
        self.menu: Dict[str, int] = {  # 메뉴 {메뉴명: 가격}
            "아메리카노": 4500,
            "카페라떼": 5000,
            "카푸치노": 5500,
            "바닐라라떼": 5500,
            "카라멜마끼아또": 6000,
            "초코라떼": 5500,
            "녹차라떼": 5500,
            "딸기스무디": 6500,
            "치즈케이크": 6000,
            "티라미수": 6500,
        }
        self.next_customer_id: int = 1  # 다음에 발급할 고객번호

    def register_customer(self, _name: str) -> Tuple[bool, str]:
        """새 고객 등록"""
        # === 내용 써보기! ===
        # 1. customer_id 변수를 만들고, f"C{self.next_customer_id:04d}"를 저장 (예: C0001)
        # 2. new_customer 변수를 만들고, Customer(_name, customer_id, 0)를 저장
        # 3. self.customers[customer_id]에 new_customer를 저장
        # 4. self.next_customer_id를 1 증가시키기
        # 5. (True, "고객 등록 메시지") 를 반환 (아래 return 참고)
        
        return True, f"고객 등록이 완료되었습니다! 고객번호: {customer_id}"

    def find_customer(self, _customer_id: str) -> Optional[Customer]:
        """고객번호로 고객 찾기"""
        if _customer_id in self.customers:
            return self.customers[_customer_id]

        return None

    def order(self, _customer_id: Optional[str], _menu_name: str, _quantity: int = 1, _use_points: int = 0) -> Tuple[bool, str]:
        """주문하기 - 메뉴를 주문하고 포인트 적립/사용 (비회원도 주문 가능)"""
        # === 내용 써보기! ===
        # 1. _menu_name이 self.menu에 없으면, (False, "존재하지 않는 메뉴입니다.") 를 반환
        # 2. _quantity가 1보다 작으면, (False, "주문 수량은 1개 이상이어야 합니다.") 를 반환
        # 3. total_price 변수를 만들고, self.menu[_menu_name] * _quantity를 저장
        # 
        # 4. customer 변수를 None으로 초기화
        # 5. _customer_id가 None이 아니면:
        #    - customer를 self.find_customer(_customer_id)로 찾기
        # 
        # 6. customer가 None이 아니면 (회원인 경우):
        #    - _use_points가 0보다 크면:
        #      * success, message 변수를 만들고, customer.use_points(_use_points)를 저장
        #      * success가 False이면, (False, message)를 반환
        #      * total_price에서 _use_points를 빼기
        #    - customer.earn_points(total_price) 실행 (포인트 적립)
        #    - order_info 변수를 만들고, f"{_menu_name} x{_quantity}"를 저장
        #    - customer.order_history에 order_info를 추가
        #    - (True, "주문 완료 메시지 (회원)") 반환
        # 
        # 7. customer가 None이면 (비회원인 경우):
        #    - _use_points가 0보다 크면, (False, "비회원은 포인트를 사용할 수 없습니다.") 반환
        #    - (True, "주문 완료 메시지 (비회원)") 반환 (아래 return 참고)
        
        return True, f"주문 완료! (비회원) {_menu_name} x{_quantity} = {total_price:,}원"

    def show_menu(self) -> str:
        """메뉴판 보여주기"""
        # === 내용 써보기! ===
        # 1. result 변수를 만들고, f"=== {self.name} 메뉴 ===\n" 를 저장
        # 2. for menu_name, price in self.menu.items(): 로 반복문 시작
        # 3. result에 f"{menu_name}: {price:,}원\n" 를 더하기 (result += ...)
        # 4. result를 반환 (아래 return 참고)
        
        return result

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
    cafe = Cafe("스타벅스")  # 카페 개설!

    # === 아래 내용을 채워서 테스트 해보기! ===
    # 1. cafe.show_menu() 실행하고 결과를 출력 (메뉴판 확인)
    # 2. cafe.order(None, "아메리카노", 1) 실행 (비회원이 아메리카노 1잔 주문)
    # 3. cafe.register_customer("홍길동") 실행하고 결과를 출력
    # 4. cafe.register_customer("김철수") 실행하고 결과를 출력
    # 5. cafe.get_all_customers() 실행하고 결과를 출력
    # 6. cafe.order("C0001", "아메리카노", 2) 실행 (홍길동이 아메리카노 2잔 주문)
    # 7. cafe.order("C0002", "카페라떼", 1) 실행 (김철수가 카페라떼 1잔 주문)
    # 8. cafe.find_customer("C0001")을 사용해서 홍길동 고객 찾기
    # 9. 찾은 고객의 정보 출력 (customer.get_info())
    # 10. cafe.order("C0001", "카푸치노", 1, 450) 실행 (홍길동이 포인트 450P 사용해서 카푸치노 주문)
    # 11. cafe.order(None, "카라멜마끼아또", 1, 100) 실행 (비회원이 포인트 사용 시도 - 에러 확인)
    # 12. cafe.get_all_customers() 실행하고 최종 결과 출력