import tkinter as tk
from tkinter import messagebox, scrolledtext
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
        self.customers: Dict[str, Customer] = (
            {}
        )  # 고객들을 저장하는 딕셔너리 {계좌번호: Customer}
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


class BankSystemUI:
    """은행 시스템 - 은행원이 쓰는 유저 인터페이스(UI)"""
    
    FONT_TITLE = ("Arial", 20, "bold")
    FONT_LABEL = ("Arial", 12)
    FONT_ENTRY = ("Arial", 11)
    FONT_BUTTON = ("Arial", 11, "bold")
    FONT_RESULT = ("Arial", 10)

    def __init__(self, _bank: Bank) -> None:
        self.bank: Bank = _bank

        # tkinter 메인 윈도우 생성
        self.root = tk.Tk()
        self.root.title("뮤타블 은행 시스템")
        self.root.geometry("700x600")

        self._init_ui()

    def _init_ui(self) -> None:
        """UI 초기화 - 버튼과 입력창 배치"""

        # === 제목 ===
        title_label = tk.Label(
            self.root,
            text="은행 시스템",
            font=self.FONT_TITLE,
            pady=10
        )
        title_label.pack()

        # === 계좌 개설 섹션 ===
        create_frame = tk.Frame(self.root, pady=5)
        create_frame.pack(fill=tk.X, padx=10)

        tk.Label(
            create_frame,
            text="고객 이름:",
            width=10,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.name_input = tk.Entry(create_frame, width=15, font=self.FONT_ENTRY)
        self.name_input.pack(side=tk.LEFT, padx=5)

        tk.Label(
            create_frame,
            text="초기 입금액:",
            width=10,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.initial_deposit_input = tk.Entry(create_frame, width=15, font=self.FONT_ENTRY)
        self.initial_deposit_input.pack(side=tk.LEFT, padx=5)

        create_btn = tk.Button(
            create_frame,
            text="계좌 개설",
            command=self._create_account,
            bg="#4CAF50",
            fg="white",
            width=10,
            font=self.FONT_BUTTON
        )
        create_btn.pack(side=tk.LEFT, padx=5)

        # === 입금/출금 섹션 ===
        transaction_frame = tk.Frame(self.root, pady=5)
        transaction_frame.pack(fill=tk.X, padx=10)

        tk.Label(
            transaction_frame,
            text="계좌번호:",
            width=10,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.account_input = tk.Entry(transaction_frame, width=15, font=self.FONT_ENTRY)
        self.account_input.pack(side=tk.LEFT, padx=5)

        tk.Label(
            transaction_frame,
            text="금액:",
            width=10,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.amount_input = tk.Entry(transaction_frame, width=15, font=self.FONT_ENTRY)
        self.amount_input.pack(side=tk.LEFT, padx=5)

        deposit_btn = tk.Button(
            transaction_frame,
            text="입금",
            command=self._deposit,
            bg="#2196F3",
            fg="white",
            width=8,
            font=self.FONT_BUTTON
        )
        deposit_btn.pack(side=tk.LEFT, padx=5)

        withdraw_btn = tk.Button(
            transaction_frame,
            text="출금",
            command=self._withdraw,
            bg="#FF9800",
            fg="white",
            width=8,
            font=self.FONT_BUTTON
        )
        withdraw_btn.pack(side=tk.LEFT, padx=5)

        # === 송금 섹션 ===
        transfer_frame = tk.Frame(self.root, pady=5)
        transfer_frame.pack(fill=tk.X, padx=10)

        tk.Label(
            transfer_frame,
            text="보내는 계좌:",
            width=12,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.from_account_input = tk.Entry(transfer_frame, width=10, font=self.FONT_ENTRY)
        self.from_account_input.pack(side=tk.LEFT, padx=5)

        tk.Label(
            transfer_frame,
            text="받는 계좌:",
            width=10,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.to_account_input = tk.Entry(transfer_frame, width=10, font=self.FONT_ENTRY)
        self.to_account_input.pack(side=tk.LEFT, padx=5)

        tk.Label(
            transfer_frame,
            text="금액:",
            width=6,
            font=self.FONT_LABEL
        ).pack(side=tk.LEFT, padx=5)
        
        self.transfer_amount_input = tk.Entry(transfer_frame, width=10, font=self.FONT_ENTRY)
        self.transfer_amount_input.pack(side=tk.LEFT, padx=5)

        transfer_btn = tk.Button(
            transfer_frame,
            text="송금",
            command=self._transfer,
            bg="#9C27B0",
            fg="white",
            width=8,
            font=self.FONT_BUTTON
        )
        transfer_btn.pack(side=tk.LEFT, padx=5)

        # === 조회 버튼 ===
        query_frame = tk.Frame(self.root, pady=5)
        query_frame.pack(fill=tk.X, padx=10)

        check_balance_btn = tk.Button(
            query_frame,
            text="잔액 조회",
            command=self._check_balance,
            bg="#607D8B",
            fg="white",
            width=15,
            font=self.FONT_BUTTON
        )
        check_balance_btn.pack(side=tk.LEFT, padx=5)

        show_all_btn = tk.Button(
            query_frame,
            text="전체 고객 조회",
            command=self._show_all_customers,
            bg="#607D8B",
            fg="white",
            width=15,
            font=self.FONT_BUTTON
        )
        show_all_btn.pack(side=tk.LEFT, padx=5)

        # === 결과 출력 영역 ===
        result_frame = tk.Frame(self.root, pady=5)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        tk.Label(
            result_frame,
            text="결과:",
            font=self.FONT_LABEL
        ).pack(anchor=tk.W)
        
        self.result_display = scrolledtext.ScrolledText(
            result_frame,
            width=80,
            height=15,
            bg="#2b2b2b",
            fg="white",
            font=self.FONT_RESULT,
        )
        self.result_display.pack(fill=tk.BOTH, expand=True)

    def _show_message(self, _message: str) -> None:
        """결과 출력 영역에 메시지 표시"""
        current_text = self.result_display.get("1.0", tk.END)
        self.result_display.delete("1.0", tk.END)
        self.result_display.insert("1.0", f"{_message}\n{'='*50}\n{current_text}")

    def _create_account(self) -> None:
        """계좌 개설 버튼 클릭 시"""
        name = self.name_input.get().strip()
        initial_deposit_text = self.initial_deposit_input.get().strip()

        if not name:
            messagebox.showwarning("오류", "고객 이름을 입력하세요.")
            return

        try:
            initial_deposit = int(initial_deposit_text) if initial_deposit_text else 0
        except ValueError:
            messagebox.showwarning("오류", "초기 입금액은 숫자여야 합니다.")
            return

        success, message = self.bank.create_account(name, initial_deposit)

        if success:
            self._show_message(f"[OK] {message}")
            self.name_input.delete(0, tk.END)
            self.initial_deposit_input.delete(0, tk.END)
        else:
            messagebox.showwarning("오류", message)

    def _deposit(self) -> None:
        """입금 버튼 클릭 시"""
        account_number = self.account_input.get().strip()
        amount_text = self.amount_input.get().strip()

        if not account_number or not amount_text:
            messagebox.showwarning("오류", "계좌번호와 금액을 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            messagebox.showwarning("오류", "금액은 숫자여야 합니다.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            messagebox.showwarning("오류", "계좌를 찾을 수 없습니다.")
            return

        success, message = customer.deposit(amount)

        if success:
            self._show_message(f"[OK] {message}")
            self.amount_input.delete(0, tk.END)
        else:
            messagebox.showwarning("오류", message)

    def _withdraw(self) -> None:
        """출금 버튼 클릭 시"""
        account_number = self.account_input.get().strip()
        amount_text = self.amount_input.get().strip()

        if not account_number or not amount_text:
            messagebox.showwarning("오류", "계좌번호와 금액을 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            messagebox.showwarning("오류", "금액은 숫자여야 합니다.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            messagebox.showwarning("오류", "계좌를 찾을 수 없습니다.")
            return

        success, message = customer.withdraw(amount)

        if success:
            self._show_message(f"[OK] {message}")
            self.amount_input.delete(0, tk.END)
        else:
            messagebox.showwarning("오류", message)

    def _transfer(self) -> None:
        """송금 버튼 클릭 시"""
        from_account = self.from_account_input.get().strip()
        to_account = self.to_account_input.get().strip()
        amount_text = self.transfer_amount_input.get().strip()

        if not from_account or not to_account or not amount_text:
            messagebox.showwarning("오류", "모든 필드를 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            messagebox.showwarning("오류", "금액은 숫자여야 합니다.")
            return

        success, message = self.bank.transfer(from_account, to_account, amount)

        if success:
            self._show_message(f"[OK] {message}")
            self.transfer_amount_input.delete(0, tk.END)
        else:
            messagebox.showwarning("오류", message)

    def _check_balance(self) -> None:
        """잔액 조회 버튼 클릭 시"""
        account_number = self.account_input.get().strip()

        if not account_number:
            messagebox.showwarning("오류", "계좌번호를 입력하세요.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            messagebox.showwarning("오류", "계좌를 찾을 수 없습니다.")
            return

        self._show_message(f"[잔액] {customer.get_info()}")

    def _show_all_customers(self) -> None:
        """전체 고객 조회 버튼 클릭 시"""
        all_customers = self.bank.get_all_customers()
        self._show_message(all_customers)

    def run(self) -> None:
        """프로그램 실행"""
        self.root.mainloop()


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    bank = Bank("뮤타블 은행")  # Bank 객체 생성
    ui = BankSystemUI(bank)  # UI 객체 생성
    ui.run()  # 프로그램 실행