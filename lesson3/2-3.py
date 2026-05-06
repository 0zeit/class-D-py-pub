import tkinter as tk
from tkinter import messagebox, scrolledtext
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
        self.customers: Dict[str, Customer] = {}  # 고객들을 저장하는 딕셔너리
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

    def order(
        self,
        _customer_id: Optional[str],
        _menu_name: str,
        _quantity: int = 1,
        _use_points: int = 0,
    ) -> Tuple[bool, str]:
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

            return (
                True,
                f"주문 완료! (회원) {_menu_name} x{_quantity} = {total_price:,}원",
            )
        else:
            # 비회원인 경우
            if _use_points > 0:
                return False, "비회원은 포인트를 사용할 수 없습니다."

            return (
                True,
                f"주문 완료! (비회원) {_menu_name} x{_quantity} = {total_price:,}원",
            )

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


class CafeSystemUI:
    """카페 시스템 - 카페 직원이 쓰는 유저 인터페이스(UI)"""

    FONT_TITLE = ("Arial", 20, "bold")
    FONT_LABEL = ("Arial", 12)
    FONT_ENTRY = ("Arial", 11)
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_RESULT = ("Arial", 10)

    def __init__(self, _cafe: Cafe) -> None:
        self.cafe: Cafe = _cafe

        # tkinter 메인 윈도우 생성
        self.root = tk.Tk()
        self.root.title(f"{self.cafe.name} 주문 시스템")
        self.root.geometry("800x700")

        self._init_ui()

    def _init_ui(self) -> None:
        """UI 초기화 - 버튼과 입력창 배치"""

        # === 제목 ===
        title_label = tk.Label(
            self.root, text=f"{self.cafe.name} 주문 시스템", font=self.FONT_TITLE, pady=10
        )
        title_label.pack()

        # === 고객 등록 섹션 ===
        register_frame = tk.Frame(self.root, pady=5)
        register_frame.pack(fill=tk.X, padx=10)

        tk.Label(
            register_frame, text="고객 이름:", width=10, font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)

        self.customer_name_input = tk.Entry(
            register_frame, width=15, font=self.FONT_ENTRY
        )
        self.customer_name_input.pack(side=tk.LEFT, padx=5)

        register_btn = tk.Button(
            register_frame,
            text="고객 등록",
            command=self._register_customer,
            bg="#4CAF50",
            fg="white",
            width=12,
            font=self.FONT_BUTTON,
        )
        register_btn.pack(side=tk.LEFT, padx=5)

        # === 주문 섹션 ===
        order_frame1 = tk.Frame(self.root, pady=5)
        order_frame1.pack(fill=tk.X, padx=10)

        tk.Label(order_frame1, text="고객번호:", width=10, font=self.FONT_LABEL).pack(
            side=tk.LEFT, padx=5
        )

        self.customer_id_input = tk.Entry(order_frame1, width=12, font=self.FONT_ENTRY)
        self.customer_id_input.pack(side=tk.LEFT, padx=5)

        tk.Label(
            order_frame1, text="(비회원은 비워두세요)", font=("Arial", 9), fg="gray"
        ).pack(side=tk.LEFT, padx=5)

        order_frame2 = tk.Frame(self.root, pady=5)
        order_frame2.pack(fill=tk.X, padx=10)

        tk.Label(order_frame2, text="메뉴명:", width=10, font=self.FONT_LABEL).pack(
            side=tk.LEFT, padx=5
        )

        self.menu_name_input = tk.Entry(order_frame2, width=15, font=self.FONT_ENTRY)
        self.menu_name_input.pack(side=tk.LEFT, padx=5)

        tk.Label(order_frame2, text="수량:", width=6, font=self.FONT_LABEL).pack(
            side=tk.LEFT, padx=5
        )

        self.quantity_input = tk.Entry(order_frame2, width=8, font=self.FONT_ENTRY)
        self.quantity_input.insert(0, "1")
        self.quantity_input.pack(side=tk.LEFT, padx=5)

        tk.Label(order_frame2, text="포인트 사용:", width=10, font=self.FONT_LABEL).pack(
            side=tk.LEFT, padx=5
        )

        self.points_input = tk.Entry(order_frame2, width=8, font=self.FONT_ENTRY)
        self.points_input.insert(0, "0")
        self.points_input.pack(side=tk.LEFT, padx=5)

        order_btn = tk.Button(
            order_frame2,
            text="주문하기",
            command=self._order,
            bg="#FF5722",
            fg="white",
            width=10,
            font=self.FONT_BUTTON,
        )
        order_btn.pack(side=tk.LEFT, padx=5)

        # === 조회 버튼 ===
        query_frame = tk.Frame(self.root, pady=5)
        query_frame.pack(fill=tk.X, padx=10)

        menu_btn = tk.Button(
            query_frame,
            text="메뉴판 보기",
            command=self._show_menu,
            bg="#2196F3",
            fg="white",
            width=15,
            font=self.FONT_BUTTON,
        )
        menu_btn.pack(side=tk.LEFT, padx=5)

        customer_info_btn = tk.Button(
            query_frame,
            text="고객 정보 조회",
            command=self._check_customer_info,
            bg="#9C27B0",
            fg="white",
            width=15,
            font=self.FONT_BUTTON,
        )
        customer_info_btn.pack(side=tk.LEFT, padx=5)

        all_customers_btn = tk.Button(
            query_frame,
            text="전체 고객 조회",
            command=self._show_all_customers,
            bg="#607D8B",
            fg="white",
            width=15,
            font=self.FONT_BUTTON,
        )
        all_customers_btn.pack(side=tk.LEFT, padx=5)

        # === 결과 출력 영역 ===
        result_frame = tk.Frame(self.root, pady=5)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        tk.Label(result_frame, text="결과:", font=self.FONT_LABEL).pack(anchor=tk.W)

        self.result_display = scrolledtext.ScrolledText(
            result_frame,
            width=90,
            height=20,
            bg="#2b2b2b",
            fg="white",
            font=self.FONT_RESULT,
        )
        self.result_display.pack(fill=tk.BOTH, expand=True)

    def _show_message(self, _message: str) -> None:
        """결과 출력 영역에 메시지 표시"""
        current_text = self.result_display.get("1.0", tk.END)
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert(
            "1.0", f"{_message}\n{'=' * 60}\n{current_text}"
        )

    def _register_customer(self) -> None:
        """고객 등록 버튼 클릭 시"""
        name = self.customer_name_input.get().strip()

        if not name:
            messagebox.showwarning("오류", "고객 이름을 입력하세요.")
            return

        success, message = self.cafe.register_customer(name)

        if success:
            self._show_message(f"[OK] {message}")
            self.customer_name_input.delete(0, tk.END)
        else:
            messagebox.showwarning("오류", message)

    def _order(self) -> None:
        """주문하기 버튼 클릭 시"""
        customer_id = self.customer_id_input.get().strip()
        menu_name = self.menu_name_input.get().strip()
        quantity_text = self.quantity_input.get().strip()
        points_text = self.points_input.get().strip()

        if not menu_name:
            messagebox.showwarning("오류", "메뉴명을 입력하세요.")
            return

        try:
            quantity = int(quantity_text) if quantity_text else 1
            use_points = int(points_text) if points_text else 0
        except ValueError:
            messagebox.showwarning("오류", "수량과 포인트는 숫자여야 합니다.")
            return

        # 고객번호가 비어있으면 None으로 (비회원 주문)
        customer_id_or_none = customer_id if customer_id else None

        success, message = self.cafe.order(
            customer_id_or_none, menu_name, quantity, use_points
        )

        if success:
            self._show_message(f"[OK] {message}")
            self.menu_name_input.delete(0, tk.END)
            self.quantity_input.delete(0, tk.END)
            self.quantity_input.insert(0, "1")
            self.points_input.delete(0, tk.END)
            self.points_input.insert(0, "0")
        else:
            messagebox.showwarning("오류", message)

    def _show_menu(self) -> None:
        """메뉴판 보기 버튼 클릭 시"""
        menu = self.cafe.show_menu()
        self._show_message(menu)

    def _check_customer_info(self) -> None:
        """고객 정보 조회 버튼 클릭 시"""
        customer_id = self.customer_id_input.get().strip()

        if not customer_id:
            messagebox.showwarning("오류", "고객번호를 입력하세요.")
            return

        customer = self.cafe.find_customer(customer_id)
        if customer is None:
            messagebox.showwarning("오류", "고객을 찾을 수 없습니다.")
            return

        info = f"[고객 정보]\n{customer.get_info()}\n\n"
        if customer.order_history:
            info += "주문 내역:\n"
            for i, order in enumerate(customer.order_history, 1):
                info += f"  {i}. {order}\n"
        else:
            info += "주문 내역이 없습니다."

        self._show_message(info)

    def _show_all_customers(self) -> None:
        """전체 고객 조회 버튼 클릭 시"""
        all_customers = self.cafe.get_all_customers()
        self._show_message(all_customers)

    def run(self) -> None:
        """프로그램 실행"""
        self.root.mainloop()


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    cafe = Cafe("뮤타벅스")  # Cafe 객체 생성
    ui = CafeSystemUI(cafe)  # UI 객체 생성
    ui.run()  # 프로그램 실행