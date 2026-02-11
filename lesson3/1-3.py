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
        # === 내용 써보기! ===
        # 1. self.is_borrowed가 False이면 True 반환, 아니면 False 반환
        # (대출 중이 아니면 대출 가능)
        
        return not self.is_borrowed

    def borrow(self, _member_id: str, _borrow_date: datetime) -> Tuple[bool, str]:
        """책 대출하기"""
        # === 내용 써보기! ===
        # 1. self.is_available()이 False이면, (False, "이미 대출 중인 책입니다.") 반환
        # 2. self.is_borrowed를 True로 설정
        # 3. self.borrower_id를 _member_id로 설정
        # 4. self.borrow_date를 _borrow_date로 설정
        # 5. (True, "대출 완료 메시지") 반환 (아래 return 참고)
        
        return True, f"'{self.title}' 책이 대출되었습니다."

    def return_book(self) -> Tuple[bool, str]:
        """책 반납하기"""
        # === 내용 써보기! ===
        # 1. self.is_borrowed가 False이면, (False, "대출 중이 아닌 책입니다.") 반환
        # 2. self.is_borrowed를 False로 설정
        # 3. self.borrower_id를 None으로 설정
        # 4. self.borrow_date를 None으로 설정
        # 5. (True, "반납 완료 메시지") 반환 (아래 return 참고)
        
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
        # === 내용 써보기! ===
        # 1. len(self.borrowed_books)가 MAX_BORROW_LIMIT보다 작으면 True, 아니면 False 반환
        
        return len(self.borrowed_books) < self.MAX_BORROW_LIMIT

    def borrow(self, _book_id: str) -> Tuple[bool, str]:
        """책 대출하기 (회원 측 처리)"""
        # === 내용 써보기! ===
        # 1. self.can_borrow()가 False이면, (False, f"대출 한도 초과! 최대 {MAX_BORROW_LIMIT}권까지...") 반환
        # 2. self.borrowed_books에 _book_id를 추가 (self.borrowed_books.append(_book_id))
        # 3. (True, "대출 성공 메시지") 반환 (아래 return 참고)
        
        return True, f"책 대출이 완료되었습니다. (현재 대출: {len(self.borrowed_books)}권)"

    def return_book(self, _book_id: str) -> Tuple[bool, str]:
        """책 반납하기 (회원 측 처리)"""
        # === 내용 써보기! ===
        # 1. _book_id가 self.borrowed_books에 없으면, (False, "대출하지 않은 책입니다.") 반환
        # 2. self.borrowed_books에서 _book_id를 제거 (self.borrowed_books.remove(_book_id))
        # 3. (True, "반납 성공 메시지") 반환 (아래 return 참고)
        
        return True, f"책 반납이 완료되었습니다. (현재 대출: {len(self.borrowed_books)}권)"

    def calculate_late_fee(self, _borrow_date: datetime, _return_date: datetime) -> int:
        """연체료 계산"""
        # === 내용 써보기! ===
        # 1. due_date 변수를 만들고, _borrow_date + timedelta(days=BORROW_PERIOD_DAYS)를 저장
        # 2. _return_date가 due_date보다 작거나 같으면, 0을 반환 (연체 없음)
        # 3. late_days 변수를 만들고, (_return_date - due_date).days를 저장
        # 4. late_fee 변수를 만들고, late_days * LATE_FEE_PER_DAY를 저장
        # 5. late_fee를 반환 (아래 return 참고)
        
        return 0

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
        # === 내용 써보기! ===
        # 1. book_id 변수를 만들고, f"B{self.next_book_id:04d}"를 저장 (예: B0001)
        # 2. new_book 변수를 만들고, Book(_title, book_id, _author)를 저장
        # 3. self.books[book_id]에 new_book을 저장
        # 4. self.next_book_id를 1 증가시키기
        # 5. (True, "책 추가 완료 메시지") 를 반환 (아래 return 참고)
        
        return True, f"책이 등록되었습니다! 책 번호: {book_id}"

    def register_member(self, _name: str) -> Tuple[bool, str]:
        """새 회원 등록"""
        # === 내용 써보기! ===
        # 1. member_id 변수를 만들고, f"M{self.next_member_id:04d}"를 저장 (예: M0001)
        # 2. new_member 변수를 만들고, Member(_name, member_id)를 저장
        # 3. self.members[member_id]에 new_member를 저장
        # 4. self.next_member_id를 1 증가시키기
        # 5. (True, "회원 등록 완료 메시지") 를 반환 (아래 return 참고)
        
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
        # === 내용 써보기! ===
        # 1. member 변수를 만들고, self.find_member(_member_id)를 저장
        # 2. book 변수를 만들고, self.find_book(_book_id)를 저장
        # 3. member가 None이면, (False, "회원을 찾을 수 없습니다.") 반환
        # 4. book이 None이면, (False, "책을 찾을 수 없습니다.") 반환
        # 5. _borrow_date가 None이면, _borrow_date를 datetime.now()로 설정
        # 6. success, message 변수를 만들고, member.borrow(_book_id)를 저장
        # 7. success가 False이면, (False, message) 반환
        # 8. success, message 변수를 만들고, book.borrow(_member_id, _borrow_date)를 저장
        # 9. success가 False이면:
        #    - member.return_book(_book_id) 실행 (대출 취소)
        #    - (False, message) 반환
        # 10. (True, "대출 완료 메시지") 반환 (아래 return 참고)
        
        return True, f"{member.name}님이 '{book.title}' 책을 대출했습니다."

    def return_book(
        self, _member_id: str, _book_id: str, _return_date: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """책 반납하기"""
        # === 내용 써보기! ===
        # 1. member 변수를 만들고, self.find_member(_member_id)를 저장
        # 2. book 변수를 만들고, self.find_book(_book_id)를 저장
        # 3. member가 None이면, (False, "회원을 찾을 수 없습니다.") 반환
        # 4. book이 None이면, (False, "책을 찾을 수 없습니다.") 반환
        # 5. _return_date가 None이면, _return_date를 datetime.now()로 설정
        # 6. book.borrow_date가 None이면, (False, "대출 기록이 없습니다.") 반환
        # 7. late_fee 변수를 만들고, member.calculate_late_fee(book.borrow_date, _return_date)를 저장
        # 8. success, message 변수를 만들고, member.return_book(_book_id)를 저장
        # 9. success가 False이면, (False, message) 반환
        # 10. success, message 변수를 만들고, book.return_book()를 저장
        # 11. success가 False이면, (False, message) 반환
        # 12. late_fee가 0보다 크면, (True, f"반납 완료! 연체료: {late_fee:,}원") 반환
        # 13. 그렇지 않으면, (True, "반납 완료! 연체료 없음") 반환 (아래 return 참고)
        
        return True, f"{member.name}님이 '{book.title}' 책을 반납했습니다."

    def get_all_members(self) -> str:
        """모든 회원 정보를 문자열로 반환"""
        # === 내용 써보기! ===
        # 1. self.members가 비어있으면, "등록된 회원이 없습니다." 를 반환
        # 2. result 변수를 만들고, f"=== {self.name} 회원 목록 ===\n" 를 저장
        # 3. for member in self.members.values(): 로 반복문 시작
        # 4. result에 member.get_info() + "\n" 를 더하기 (result += ...)
        # 5. result를 반환 (아래 return 참고)
        
        return result

    def get_all_books(self) -> str:
        """모든 책 정보를 문자열로 반환"""
        # === 내용 써보기! ===
        # 1. self.books가 비어있으면, "등록된 책이 없습니다." 를 반환
        # 2. result 변수를 만들고, f"=== {self.name} 도서 목록 ===\n" 를 저장
        # 3. for book in self.books.values(): 로 반복문 시작
        # 4. result에 book.get_info() + "\n" 를 더하기 (result += ...)
        # 5. result를 반환 (아래 return 참고)
        
        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    library = Library("부산 시립 도서관")  # 도서관 개설!

    # === 아래 내용을 채워서 테스트 해보기! ===
    # 1. library.add_book("파이썬 프로그래밍", "홍길동") 실행하고 결과를 출력
    # 2. library.add_book("자료구조와 알고리즘", "김철수") 실행하고 결과를 출력
    # 3. library.add_book("Clean Code", "로버트 마틴") 실행하고 결과를 출력
    # 4. library.get_all_books() 실행하고 결과를 출력
    # 5. library.register_member("이영희") 실행하고 결과를 출력
    # 6. library.register_member("박민수") 실행하고 결과를 출력
    # 7. library.get_all_members() 실행하고 결과를 출력
    # 8. library.borrow_book("M0001", "B0001") 실행 (이영희가 파이썬 프로그래밍 대출)
    # 9. library.borrow_book("M0001", "B0002") 실행 (이영희가 자료구조 대출)
    # 10. library.get_all_books() 실행하고 결과를 출력 (대출 상태 확인)
    # 11. library.find_member("M0001")을 사용해서 이영희 회원 찾기
    # 12. 찾은 회원의 정보 출력 (member.get_info())
    # 13. library.return_book("M0001", "B0001") 실행 (이영희가 파이썬 프로그래밍 반납)
    # 14. library.get_all_members() 실행하고 최종 결과 출력