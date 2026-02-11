import sys
from typing import Dict, Tuple, Optional, List
from datetime import datetime, timedelta

# 만들어보기!
# 클래스(Class)
#   도서관(Library)
#       __init__()
#       add_book()
#       register_member()
#       find_member()
#       find_book()
#       borrow_book()
#       return_book()
#       get_all_members()
#       get_all_books()
#
#   회원(Member)
#       __init__()
#       can_borrow()
#       borrow()
#       return_book()
#       calculate_late_fee()
#       get_info()
#
#   책(Book)
#       __init__()
#       is_available()
#       borrow()
#       return_book()
#       get_info()


from typing import Dict, Tuple, Optional, List
from datetime import datetime, timedelta


class Book:
    """책 클래스 - 도서관의 책 정보를 담는 클래스"""

    def __init__(self, _title: str, _book_id: str, _author: str) -> None:
        self.title: str = _title  # 책 제목
        self.book_id: str = _book_id  # 책 번호
        self.author: str = _author  # 저자
        self.is_borrowed: bool = False  # 대출 중인지 여부
        self.borrower_id: Optional[str] = None  # 대출한 회원 ID
        self.borrow_date: Optional[datetime] = None  # 대출 날짜

    def is_available(self) -> bool:
        """대출 가능한지 확인"""
        return not self.is_borrowed

    def borrow(self, _member_id: str, _borrow_date: datetime) -> Tuple[bool, str]:
        """책 대출하기"""
        if not self.is_available():
            return False, "이미 대출 중인 책입니다."
        
        self.is_borrowed = True
        self.borrower_id = _member_id
        self.borrow_date = _borrow_date
        
        return True, f"'{self.title}' 책이 대출되었습니다."

    def return_book(self) -> Tuple[bool, str]:
        """책 반납하기"""
        if not self.is_borrowed:
            return False, "대출 중이 아닌 책입니다."
        
        self.is_borrowed = False
        self.borrower_id = None
        self.borrow_date = None
        
        return True, f"'{self.title}' 책이 반납되었습니다."

    def get_info(self) -> str:
        """책 정보를 문자열로 반환"""
        status = "대출 중" if self.is_borrowed else "대출 가능"
        return f"[{self.book_id}] {self.title} (저자: {self.author}) - {status}"


class Member:
    """회원 클래스 - 도서관 회원 정보를 담는 클래스"""

    MAX_BORROW_LIMIT = 5  # 최대 대출 가능 권수
    BORROW_PERIOD_DAYS = 14  # 대출 기간 (일)
    LATE_FEE_PER_DAY = 100  # 하루당 연체료 (원)

    def __init__(self, _name: str, _member_id: str) -> None:
        self.name: str = _name  # 회원 이름
        self.member_id: str = _member_id  # 회원 번호
        self.borrowed_books: List[str] = []  # 대출한 책 ID 목록

    def can_borrow(self) -> bool:
        """대출 가능한지 확인 (최대 5권 제한)"""
        return len(self.borrowed_books) < self.MAX_BORROW_LIMIT

    def borrow(self, _book_id: str) -> Tuple[bool, str]:
        """책 대출하기 (회원 측 처리)"""
        if not self.can_borrow():
            return False, f"대출 한도 초과! 최대 {self.MAX_BORROW_LIMIT}권까지 대출 가능합니다."
        
        self.borrowed_books.append(_book_id)
        
        return True, f"책 대출이 완료되었습니다. (현재 대출: {len(self.borrowed_books)}권)"

    def return_book(self, _book_id: str) -> Tuple[bool, str]:
        """책 반납하기 (회원 측 처리)"""
        if _book_id not in self.borrowed_books:
            return False, "대출하지 않은 책입니다."
        
        self.borrowed_books.remove(_book_id)
        
        return True, f"책 반납이 완료되었습니다. (현재 대출: {len(self.borrowed_books)}권)"

    def calculate_late_fee(self, _borrow_date: datetime, _return_date: datetime) -> int:
        """연체료 계산"""
        due_date = _borrow_date + timedelta(days=self.BORROW_PERIOD_DAYS)
        
        if _return_date <= due_date:
            return 0
        
        late_days = (_return_date - due_date).days
        late_fee = late_days * self.LATE_FEE_PER_DAY
        
        return late_fee

    def get_info(self) -> str:
        """회원 정보를 문자열로 반환"""
        return f"[{self.member_id}] {self.name}님 - 대출 중: {len(self.borrowed_books)}권"


class Library:
    """도서관 클래스 - 책과 회원을 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name  # 도서관 이름
        self.books: Dict[str, Book] = {}  # 책들을 저장하는 딕셔너리 {책ID: Book}
        self.members: Dict[str, Member] = {}  # 회원들을 저장하는 딕셔너리 {회원ID: Member}
        self.next_book_id: int = 1  # 다음에 발급할 책 번호
        self.next_member_id: int = 1  # 다음에 발급할 회원 번호

    def add_book(self, _title: str, _author: str) -> Tuple[bool, str]:
        """새 책 추가"""
        book_id = f"B{self.next_book_id:04d}"
        new_book = Book(_title, book_id, _author)
        self.books[book_id] = new_book
        self.next_book_id += 1
        
        return True, f"책이 등록되었습니다! 책 번호: {book_id}"

    def register_member(self, _name: str) -> Tuple[bool, str]:
        """새 회원 등록"""
        member_id = f"M{self.next_member_id:04d}"
        new_member = Member(_name, member_id)
        self.members[member_id] = new_member
        self.next_member_id += 1
        
        return True, f"회원 등록이 완료되었습니다! 회원번호: {member_id}"

    def find_member(self, _member_id: str) -> Optional[Member]:
        """회원번호로 회원 찾기"""
        if _member_id in self.members:
            return self.members[_member_id]

        return None

    def find_book(self, _book_id: str) -> Optional[Book]:
        """책 번호로 책 찾기"""
        if _book_id in self.books:
            return self.books[_book_id]

        return None

    def borrow_book(
        self, _member_id: str, _book_id: str, _borrow_date: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """책 대출하기"""
        member = self.find_member(_member_id)
        book = self.find_book(_book_id)
        
        if member is None:
            return False, "회원을 찾을 수 없습니다."
        
        if book is None:
            return False, "책을 찾을 수 없습니다."
        
        if _borrow_date is None:
            _borrow_date = datetime.now()
        
        success, message = member.borrow(_book_id)
        if not success:
            return False, message
        
        success, message = book.borrow(_member_id, _borrow_date)
        if not success:
            member.return_book(_book_id)
            return False, message
        
        return True, f"{member.name}님이 '{book.title}' 책을 대출했습니다."

    def return_book(
        self, _member_id: str, _book_id: str, _return_date: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """책 반납하기"""
        member = self.find_member(_member_id)
        book = self.find_book(_book_id)
        
        if member is None:
            return False, "회원을 찾을 수 없습니다."
        
        if book is None:
            return False, "책을 찾을 수 없습니다."
        
        if _return_date is None:
            _return_date = datetime.now()
        
        if book.borrow_date is None:
            return False, "대출 기록이 없습니다."
        
        late_fee = member.calculate_late_fee(book.borrow_date, _return_date)
        
        success, message = member.return_book(_book_id)
        if not success:
            return False, message
        
        success, message = book.return_book()
        if not success:
            return False, message
        
        if late_fee > 0:
            return True, f"반납 완료! 연체료: {late_fee:,}원"
        else:
            return True, "반납 완료! 연체료 없음"

    def get_all_members(self) -> str:
        """모든 회원 정보를 문자열로 반환"""
        if not self.members:
            return "등록된 회원이 없습니다."
        
        result = f"=== {self.name} 회원 목록 ===\n"
        for member in self.members.values():
            result += member.get_info() + "\n"
        
        return result

    def get_all_books(self) -> str:
        """모든 책 정보를 문자열로 반환"""
        if not self.books:
            return "등록된 책이 없습니다."
        
        result = f"=== {self.name} 도서 목록 ===\n"
        for book in self.books.values():
            result += book.get_info() + "\n"
        
        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    library = Library("뮤타블 시립 도서관")  # 도서관 개설!

    success, message = library.add_book("파이썬 프로그래밍", "홍길동")
    print(message)

    success, message = library.add_book("자료구조와 알고리즘", "김철수")
    print(message)

    success, message = library.add_book("Clean Code", "로버트 마틴")
    print(message)
    print()

    print(library.get_all_books())

    success, message = library.register_member("이영희")
    print(message)

    success, message = library.register_member("박민수")
    print(message)
    print()

    print(library.get_all_members())

    success, message = library.borrow_book("M0001", "B0001")
    print(message)

    success, message = library.borrow_book("M0001", "B0002")
    print(message)
    print()

    print(library.get_all_books())

    member = library.find_member("M0001")

    if member:
        print(member.get_info())
    print()

    success, message = library.return_book("M0001", "B0001")
    print(message)
    print()

    print(library.get_all_members())

    print("\n=== 연체 테스트 ===")
    past_date = datetime.now() - timedelta(days=20)
    success, message = library.borrow_book("M0002", "B0003", past_date)
    print(message)

    success, message = library.return_book("M0002", "B0003")
    print(message)