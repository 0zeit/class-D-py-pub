import sys
from typing import Dict, Tuple, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QTextEdit,
    QMessageBox,
)


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


class BankSystemUI(QWidget):
    """은행 시스템 - 은행원이 쓰는 유저 인터페이스(UI)"""

    def __init__(self, _bank):
        super().__init__()
        self.bank = _bank
        self._init_ui()

    def _init_ui(self):
        """UI 초기화 - 버튼과 입력창 배치"""
        self.setWindowTitle("뮤타블 은행 시스템")
        self.setGeometry(100, 100, 600, 500)

        # 메인 레이아웃
        main_layout = QVBoxLayout()

        # 제목
        title = QLabel("🏦 뮤타블 은행 시스템")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # === 계좌 개설 섹션 ===
        create_layout = QHBoxLayout()
        create_layout.addWidget(QLabel("고객 이름:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("홍길동")
        create_layout.addWidget(self.name_input)

        create_layout.addWidget(QLabel("초기 입금액:"))
        self.initial_deposit_input = QLineEdit()
        self.initial_deposit_input.setPlaceholderText("10000")
        create_layout.addWidget(self.initial_deposit_input)

        create_btn = QPushButton("계좌 개설")
        create_btn.clicked.connect(self._create_account)
        create_layout.addWidget(create_btn)

        main_layout.addLayout(create_layout)

        # === 입금/출금 섹션 ===
        transaction_layout = QHBoxLayout()
        transaction_layout.addWidget(QLabel("계좌번호:"))
        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("1001")
        transaction_layout.addWidget(self.account_input)

        transaction_layout.addWidget(QLabel("금액:"))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("5000")
        transaction_layout.addWidget(self.amount_input)

        deposit_btn = QPushButton("입금")
        deposit_btn.clicked.connect(self._deposit)
        transaction_layout.addWidget(deposit_btn)

        withdraw_btn = QPushButton("출금")
        withdraw_btn.clicked.connect(self._withdraw)
        transaction_layout.addWidget(withdraw_btn)

        main_layout.addLayout(transaction_layout)

        # === 송금 섹션 ===
        transfer_layout = QHBoxLayout()
        transfer_layout.addWidget(QLabel("보내는 계좌:"))
        self.from_account_input = QLineEdit()
        self.from_account_input.setPlaceholderText("1001")
        transfer_layout.addWidget(self.from_account_input)

        transfer_layout.addWidget(QLabel("받는 계좌:"))
        self.to_account_input = QLineEdit()
        self.to_account_input.setPlaceholderText("1002")
        transfer_layout.addWidget(self.to_account_input)

        transfer_layout.addWidget(QLabel("금액:"))
        self.transfer_amount_input = QLineEdit()
        self.transfer_amount_input.setPlaceholderText("3000")
        transfer_layout.addWidget(self.transfer_amount_input)

        transfer_btn = QPushButton("송금")
        transfer_btn.clicked.connect(self._transfer)
        transfer_layout.addWidget(transfer_btn)

        main_layout.addLayout(transfer_layout)

        # === 조회 버튼 ===
        query_layout = QHBoxLayout()

        check_balance_btn = QPushButton("잔액 조회")
        check_balance_btn.clicked.connect(self._check_balance)
        query_layout.addWidget(check_balance_btn)

        show_all_btn = QPushButton("전체 고객 조회")
        show_all_btn.clicked.connect(self._show_all_customers)
        query_layout.addWidget(show_all_btn)

        main_layout.addLayout(query_layout)

        # === 결과 출력 영역 ===
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setStyleSheet("background-color: #686868; padding: 10px;")
        main_layout.addWidget(self.result_display)

        self.setLayout(main_layout)

    def _show_message(self, _message):
        """결과 출력 영역에 메시지 표시"""
        current_text = self.result_display.toPlainText()
        self.result_display.setText(f"{_message}\n{'='*50}\n{current_text}")

    def _create_account(self):
        """계좌 개설 버튼 클릭 시"""
        name = self.name_input.text().strip()
        initial_deposit_text = self.initial_deposit_input.text().strip()

        if not name:
            QMessageBox.warning(self, "오류", "고객 이름을 입력하세요.")
            return

        try:
            initial_deposit = int(initial_deposit_text) if initial_deposit_text else 0
        except ValueError:
            QMessageBox.warning(self, "오류", "초기 입금액은 숫자여야 합니다.")
            return

        success, message = self.bank.create_account(name, initial_deposit)

        if success:
            self._show_message(f"✅ {message}")
            self.name_input.clear()
            self.initial_deposit_input.clear()
        else:
            QMessageBox.warning(self, "오류", message)

    def _deposit(self):
        """입금 버튼 클릭 시"""
        account_number = self.account_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not account_number or not amount_text:
            QMessageBox.warning(self, "오류", "계좌번호와 금액을 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, "오류", "금액은 숫자여야 합니다.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            QMessageBox.warning(self, "오류", "계좌를 찾을 수 없습니다.")
            return

        success, message = customer.deposit(amount)

        if success:
            self._show_message(f"✅ {message}")
            self.amount_input.clear()
        else:
            QMessageBox.warning(self, "오류", message)

    def _withdraw(self):
        """출금 버튼 클릭 시"""
        account_number = self.account_input.text().strip()
        amount_text = self.amount_input.text().strip()

        if not account_number or not amount_text:
            QMessageBox.warning(self, "오류", "계좌번호와 금액을 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, "오류", "금액은 숫자여야 합니다.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            QMessageBox.warning(self, "오류", "계좌를 찾을 수 없습니다.")
            return

        success, message = customer.withdraw(amount)

        if success:
            self._show_message(f"✅ {message}")
            self.amount_input.clear()
        else:
            QMessageBox.warning(self, "오류", message)

    def _transfer(self):
        """송금 버튼 클릭 시"""
        from_account = self.from_account_input.text().strip()
        to_account = self.to_account_input.text().strip()
        amount_text = self.transfer_amount_input.text().strip()

        if not from_account or not to_account or not amount_text:
            QMessageBox.warning(self, "오류", "모든 필드를 입력하세요.")
            return

        try:
            amount = int(amount_text)
        except ValueError:
            QMessageBox.warning(self, "오류", "금액은 숫자여야 합니다.")
            return

        success, message = self.bank.transfer(from_account, to_account, amount)

        if success:
            self._show_message(f"✅ {message}")
            self.transfer_amount_input.clear()
        else:
            QMessageBox.warning(self, "오류", message)

    def _check_balance(self):
        """잔액 조회 버튼 클릭 시"""
        account_number = self.account_input.text().strip()

        if not account_number:
            QMessageBox.warning(self, "오류", "계좌번호를 입력하세요.")
            return

        customer = self.bank.find_customer(account_number)
        if customer is None:
            QMessageBox.warning(self, "오류", "계좌를 찾을 수 없습니다.")
            return

        self._show_message(f"💰 {customer.get_info()}")

    def _show_all_customers(self):
        """전체 고객 조회 버튼 클릭 시"""
        all_customers = self.bank.get_all_customers()
        self._show_message(all_customers)


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    app = QApplication(sys.argv)
    bank = Bank("뮤타블 은행")  # Bank 객체 생성
    window = BankSystemUI(bank) # 만들어진 은행 객체 넘겨주기
    window.show()

    sys.exit(app.exec())
