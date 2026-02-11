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
        earned_points = _amount // 10
        self.points += earned_points
        
        return True, f"{earned_points}P 적립되었습니다! 현재 포인트: {self.points}P"

    def use_points(self, _points: int) -> Tuple[bool, str]:
        """포인트 사용 - 보유한 포인트로 할인 받기"""
        if _points <= 0:
            return False, "사용할 포인트는 0보다 커야 합니다."
        
        if self.points < _points:
            return False, f"포인트가 부족합니다. 현재 포인트: {self.points}P"
        
        self.points -= _points
        
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
        customer_id = f"C{self.next_customer_id:04d}"
        new_customer = Customer(_name, customer_id, 0)
        self.customers[customer_id] = new_customer
        self.next_customer_id += 1
        
        return True, f"고객 등록이 완료되었습니다! 고객번호: {customer_id}"

    def find_customer(self, _customer_id: str) -> Optional[Customer]:
        """고객번호로 고객 찾기"""
        if _customer_id in self.customers:
            return self.customers[_customer_id]

        return None

    def order(self, _customer_id: Optional[str], _menu_name: str, _quantity: int = 1, _use_points: int = 0) -> Tuple[bool, str]:
        """주문하기 - 메뉴를 주문하고 포인트 적립/사용 (비회원도 주문 가능)"""
        if _menu_name not in self.menu:
            return False, "존재하지 않는 메뉴입니다."
        
        if _quantity < 1:
            return False, "주문 수량은 1개 이상이어야 합니다."
        
        total_price = self.menu[_menu_name] * _quantity
        
        customer = None
        if _customer_id is not None:
            customer = self.find_customer(_customer_id)
        
        if customer is not None:
            # 회원인 경우
            if _use_points > 0:
                success, message = customer.use_points(_use_points)
                if not success:
                    return False, message
                total_price -= _use_points
            
            customer.earn_points(total_price)
            order_info = f"{_menu_name} x{_quantity}"
            customer.order_history.append(order_info)
            
            return True, f"주문 완료! (회원) {_menu_name} x{_quantity} = {total_price:,}원"
        else:
            # 비회원인 경우
            if _use_points > 0:
                return False, "비회원은 포인트를 사용할 수 없습니다."
            
            return True, f"주문 완료! (비회원) {_menu_name} x{_quantity} = {total_price:,}원"

    def show_menu(self) -> str:
        """메뉴판 보여주기"""
        result = f"=== {self.name} 메뉴 ===\n"
        for menu_name, price in self.menu.items():
            result += f"{menu_name}: {price:,}원\n"
        
        return result

    def get_all_customers(self) -> str:
        """모든 고객 정보를 문자열로 반환"""
        if not self.customers:
            return "등록된 고객이 없습니다."
        
        result = f"=== {self.name} 고객 목록 ===\n"
        for customer in self.customers.values():
            result += customer.get_info() + "\n"
        
        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    cafe = Cafe("뮤타벅스")  # 카페 개설!

    print(cafe.show_menu())
    print()

    success, message = cafe.order(None, "아메리카노", 1)
    print(message)
    print()

    success, message = cafe.register_customer("홍길동")
    print(message)

    success, message = cafe.register_customer("김철수")
    print(message)
    print()

    print(cafe.get_all_customers())

    success, message = cafe.order("C0001", "아메리카노", 2)
    print(message)

    success, message = cafe.order("C0002", "카페라떼", 1)
    print(message)
    print()

    customer = cafe.find_customer("C0001")

    if customer:
        print(customer.get_info())
    print()

    success, message = cafe.order("C0001", "카푸치노", 1, 450)
    print(message)
    print()

    success, message = cafe.order(None, "카라멜마끼아또", 1, 100)
    print(f"에러 테스트: {message}")
    print()

    print(cafe.get_all_customers())