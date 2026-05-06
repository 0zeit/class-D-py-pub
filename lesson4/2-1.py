from typing import List, Tuple

# 이번에 사용할 함수들!
#   zip(list1, list2)               두 리스트를 같은 인덱스끼리 쌍으로 묶어 순회
#                                            예) zip(["A","B"], [1, 2]) -> ("A",1), ("B",2)
#   map(함수, list)                  리스트의 모든 항목에 함수를 일괄 적용
#                                            예) map(str.upper, ["a","b"]) → "A", "B"
#   list(map(...))                  map 결과를 리스트로 변환
#   sorted(list, key=..., reverse=) key 기준으로 정렬된 새 리스트 반환
#   enumerate(list, start=)         (인덱스, 값) 쌍으로 순회, start 로 시작값 지정
#   sum(list)                       리스트 합계 반환
#   len(list)                       리스트 길이 반환

# 만들어보기!
# 전역함수(Global Function)
#   score_to_grade()
#
# 클래스(Class)
#   학생(Student)
#       __init__()
#       get_average()
#       get_subject_scores()
#       get_info()
#   성적부(GradeBook)
#       __init__()
#       add_student()
#       get_all_averages()
#       get_all_grades()
#       get_rankings()
#       get_subject_averages()
#       show_report()


def score_to_grade(_score: float) -> str:
    """점수를 등급 문자로 변환하는 함수 (map 에서 사용)"""
    # === 내용 써보기! ===
    # 1. _score 가 90 이상이면 "A" 반환
    # 2. _score 가 80 이상이면 "B" 반환
    # 3. _score 가 70 이상이면 "C" 반환
    # 4. _score 가 60 이상이면 "D" 반환
    # 5. 그 외에는 "F" 반환

    return "F"


class Student:
    """학생 클래스 - 이름과 과목별 점수를 담는 클래스"""

    def __init__(self, _name: str, _scores: List[int]) -> None:
        self.name: str = _name            # 학생 이름
        self.scores: List[int] = _scores  # 과목별 점수 리스트

    def get_average(self) -> float:
        """전 과목 평균 점수 반환"""
        # === 내용 써보기! ===
        # 1. sum(self.scores) 를 len(self.scores) 로 나눠서 반환

        return 0.0

    def get_subject_scores(self, _subject_names: List[str]) -> str:
        """과목명과 점수를 zip 으로 묶어 출력"""
        # === 내용 써보기! ===
        # 1. result 변수를 만들고 빈 문자열("") 로 초기화
        # 2. for subject, score in zip(_subject_names, self.scores): 로 반복문 시작
        #    result 에 f"  {subject}: {score}점\n" 를 더하기
        # 3. result 를 반환 (아래 return 참고)

        return result

    def get_info(self) -> str:
        """학생 요약 정보를 문자열로 반환"""
        # === 내용 써보기! ===
        # 1. avg 변수를 만들고 self.get_average() 를 저장
        # 2. grade 변수를 만들고 score_to_grade(avg) 를 저장
        # 3. f"{self.name} - 평균: {avg:.1f}점 ({grade})" 를 반환 (아래 return 참고)

        return f"{self.name} - 평균: {avg:.1f}점 ({grade})"


class GradeBook:
    """성적부 클래스 - 학생 목록과 과목을 관리하는 클래스"""

    def __init__(self, _class_name: str, _subject_names: List[str]) -> None:
        self.class_name: str = _class_name              # 반 이름
        self.subject_names: List[str] = _subject_names  # 과목명 리스트
        self.students: List[Student] = []               # 학생 리스트

    def add_student(self, _name: str, _scores: List[int]) -> Tuple[bool, str]:
        """학생 추가"""
        # === 내용 써보기! ===
        # 1. len(_scores) 가 len(self.subject_names) 와 다르면
        #    (False, "점수 개수가 맞지 않습니다. (... 개 필요)") 반환
        # 2. new_student 변수를 만들고 Student(_name, _scores) 를 저장
        # 3. self.students 에 new_student 를 append 로 추가
        # 4. (True, "... 학생이 등록되었습니다.") 반환 (아래 return 참고)

        return True, f"'{_name}' 학생이 등록되었습니다."

    def get_all_averages(self) -> List[float]:
        """모든 학생의 평균 점수 리스트 반환 (map 활용)"""
        # === 내용 써보기! ===
        # 1. list(map(lambda s: s.get_average(), self.students)) 를 반환
        #    → self.students 의 모든 학생에게 get_average() 를 일괄 적용

        return []

    def get_all_grades(self) -> List[str]:
        """모든 학생의 등급 리스트 반환 (map 활용)"""
        # === 내용 써보기! ===
        # 1. averages 변수를 만들고 self.get_all_averages() 를 저장
        # 2. list(map(score_to_grade, averages)) 를 반환
        #    → averages 의 모든 평균에 score_to_grade 함수를 일괄 적용

        return []

    def get_rankings(self) -> str:
        """평균 기준 학생 순위 반환 (zip + sorted 활용)"""
        # === 내용 써보기! ===
        # 1. self.students 가 비어있으면, "등록된 학생이 없습니다." 반환
        # 2. averages 변수를 만들고 self.get_all_averages() 를 저장
        # 3. ranked 변수를 만들고, zip 과 sorted 로 정렬된 (학생, 평균) 쌍 리스트를 저장
        #    sorted(zip(self.students, averages), key=lambda pair: pair[1], reverse=True)
        # 4. result 변수를 만들고, f"=== {self.class_name} 순위 ===\n" 를 저장
        # 5. for rank, (student, avg) in enumerate(ranked, start=1): 로 반복문 시작
        #    - grade 변수를 만들고 score_to_grade(avg) 를 저장
        #    - result 에 f"  {rank}위: {student.name} - {avg:.1f}점 ({grade})\n" 를 더하기
        # 6. result 를 반환 (아래 return 참고)

        return result

    def get_subject_averages(self) -> str:
        """과목별 전체 평균 반환 (zip + map 활용)"""
        # === 내용 써보기! ===
        # 1. self.students 가 비어있으면, "등록된 학생이 없습니다." 반환
        # 2. subject_totals 변수를 만들고, [0] * len(self.subject_names) 를 저장
        #    (과목 수만큼 0으로 채워진 리스트)
        # 3. for student in self.students: 로 반복문 시작
        #    for i, score in enumerate(student.scores): 로 내부 반복문 시작
        #      subject_totals[i] 에 score 를 더하기
        # 4. subject_avgs 변수를 만들고, map 으로 합계를 인원수로 나눠 평균 계산
        #    list(map(lambda total: total / len(self.students), subject_totals))
        # 5. result 변수를 만들고, f"=== {self.class_name} 과목별 평균 ===\n" 를 저장
        # 6. for subject, avg in zip(self.subject_names, subject_avgs): 로 반복문 시작
        #    result 에 f"  {subject}: {avg:.1f}점\n" 를 더하기
        # 7. result 를 반환 (아래 return 참고)

        return result

    def show_report(self) -> str:
        """전체 성적표 출력"""
        # === 내용 써보기! ===
        # 1. self.students 가 비어있으면, "등록된 학생이 없습니다." 반환
        # 2. result 변수를 만들고, f"=== {self.class_name} 성적표 ===\n" 를 저장
        # 3. for student in self.students: 로 반복문 시작
        #    - result 에 f"\n[{student.name}]\n" 를 더하기
        #    - result 에 student.get_subject_scores(self.subject_names) 를 더하기
        #    - result 에 f"  → {student.get_info()}\n" 를 더하기
        # 4. result 를 반환 (아래 return 참고)

        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    gradebook = GradeBook("D반", ["수학", "영어", "과학", "국어"])

    # === 아래 내용을 채워서 테스트 해보기! ===
    # 1. gradebook.add_student("홍길동", [92, 85, 78, 90]) 실행하고 결과를 출력
    # 2. gradebook.add_student("김철수", [70, 60, 88, 75]) 실행하고 결과를 출력
    # 3. gradebook.add_student("이영희", [95, 98, 92, 97]) 실행하고 결과를 출력
    # 4. gradebook.add_student("박민수", [55, 72, 61, 68]) 실행하고 결과를 출력
    # 5. gradebook.add_student("최지우", [80, 77, 83, 79]) 실행하고 결과를 출력
    #
    # 6. gradebook.show_report() 실행하고 결과를 출력 (전체 성적표)
    #
    # 7. gradebook.get_all_averages() 실행하고 결과를 출력 (map 결과 확인)
    # 8. gradebook.get_all_grades() 실행하고 결과를 출력 (map 결과 확인)
    #
    # 9. 학생 이름 리스트와 등급 리스트를 zip 으로 묶어서 출력
    #    for name, grade in zip([s.name for s in gradebook.students], gradebook.get_all_grades()):
    #        print(f"  {name}: {grade}")
    #
    # 10. gradebook.get_subject_averages() 실행하고 결과를 출력 (zip + map 결과 확인)
    # 11. gradebook.get_rankings() 실행하고 결과를 출력 (zip + sorted 결과 확인)
    #
    # 12. gradebook.add_student("오류학생", [90, 80]) 실행 (에러 확인)