from typing import List, Tuple

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
    if _score >= 90:
        return "A"
    elif _score >= 80:
        return "B"
    elif _score >= 70:
        return "C"
    elif _score >= 60:
        return "D"
    else:
        return "F"


class Student:
    """학생 클래스 - 이름과 과목별 점수를 담는 클래스"""

    def __init__(self, _name: str, _scores: List[int]) -> None:
        self.name: str = _name          # 학생 이름
        self.scores: List[int] = _scores  # 과목별 점수 리스트

    def get_average(self) -> float:
        """전 과목 평균 점수 반환"""
        return sum(self.scores) / len(self.scores)

    def get_subject_scores(self, _subject_names: List[str]) -> str:
        """과목명과 점수를 zip 으로 묶어 출력"""
        result: str = ""
        for subject, score in zip(_subject_names, self.scores):
            result += f"  {subject}: {score}점\n"
        return result

    def get_info(self) -> str:
        """학생 요약 정보를 문자열로 반환"""
        avg: float = self.get_average()
        grade: str = score_to_grade(avg)
        return f"{self.name} - 평균: {avg:.1f}점 ({grade})"

class GradeBook:
    """성적부 클래스 - 학생 목록과 과목을 관리하는 클래스"""

    def __init__(self, _class_name: str, _subject_names: List[str]) -> None:
        self.class_name: str = _class_name              # 반 이름
        self.subject_names: List[str] = _subject_names  # 과목명 리스트
        self.students: List[Student] = []               # 학생 리스트

    def add_student(self, _name: str, _scores: List[int]) -> Tuple[bool, str]:
        """학생 추가"""
        if len(_scores) != len(self.subject_names):
            return False, f"점수 개수가 맞지 않습니다. ({len(self.subject_names)}개 필요)"

        new_student: Student = Student(_name, _scores)
        self.students.append(new_student)

        return True, f"'{_name}' 학생이 등록되었습니다."

    def get_all_averages(self) -> List[float]:
        """모든 학생의 평균 점수 리스트 반환 (map 활용)"""
        return list(map(lambda s: s.get_average(), self.students))

    def get_all_grades(self) -> List[str]:
        """모든 학생의 등급 리스트 반환 (map 활용)"""
        averages: List[float] = self.get_all_averages()
        return list(map(score_to_grade, averages))

    def get_rankings(self) -> str:
        """평균 기준 학생 순위 반환 (zip 활용)"""
        if not self.students:
            return "등록된 학생이 없습니다."

        averages: List[float] = self.get_all_averages()

        # zip 으로 학생과 평균을 쌍으로 묶은 뒤 평균 기준 내림차순 정렬
        ranked = sorted(
            zip(self.students, averages),
            key=lambda pair: pair[1],
            reverse=True
        )

        result: str = f"=== {self.class_name} 순위 ===\n"
        for rank, (student, avg) in enumerate(ranked, start=1):
            grade: str = score_to_grade(avg)
            result += f"  {rank}위: {student.name} - {avg:.1f}점 ({grade})\n"

        return result

    def get_subject_averages(self) -> str:
        """과목별 전체 평균 반환 (zip + map 활용)"""
        if not self.students:
            return "등록된 학생이 없습니다."

        # 과목별 점수 합산
        subject_totals: List[int] = [0] * len(self.subject_names)
        for student in self.students:
            for i, score in enumerate(student.scores):
                subject_totals[i] += score

        # map 으로 합계를 인원수로 나눠 평균 계산
        subject_avgs: List[float] = list(
            map(lambda total: total / len(self.students), subject_totals)
        )

        # zip 으로 과목명과 평균을 쌍으로 묶어 출력
        result: str = f"=== {self.class_name} 과목별 평균 ===\n"
        for subject, avg in zip(self.subject_names, subject_avgs):
            result += f"  {subject}: {avg:.1f}점\n"

        return result

    def show_report(self) -> str:
        """전체 성적표 출력"""
        if not self.students:
            return "등록된 학생이 없습니다."

        result: str = f"=== {self.class_name} 성적표 ===\n"
        for student in self.students:
            result += f"\n[{student.name}]\n"
            result += student.get_subject_scores(self.subject_names)
            result += f"  → {student.get_info()}\n"

        return result


if __name__ == "__main__":
    gradebook = GradeBook("D반", ["수학", "영어", "과학", "국어"])

    # 학생 추가
    gradebook.add_student("홍길동", [92, 85, 78, 90])
    gradebook.add_student("김철수", [70, 60, 88, 75])
    gradebook.add_student("이영희", [95, 98, 92, 97])
    gradebook.add_student("박민수", [55, 72, 61, 68])
    gradebook.add_student("최지우", [80, 77, 83, 79])

    # 전체 성적표
    print(gradebook.show_report())

    # map: 전 학생 평균 리스트
    averages = gradebook.get_all_averages()
    print(f"전체 평균 리스트: {[f'{a:.1f}' for a in averages]}")
    print()

    # map: 전 학생 등급 리스트
    grades = gradebook.get_all_grades()

    # zip: 이름과 등급을 쌍으로 묶어 출력
    print("=== 학생별 등급 ===")
    for name, grade in zip([s.name for s in gradebook.students], grades):
        print(f"  {name}: {grade}")
    print()

    # zip + map: 과목별 평균
    print(gradebook.get_subject_averages())

    # zip + sorted: 순위표
    print(gradebook.get_rankings())

    # 에러 테스트: 점수 개수 불일치
    success, message = gradebook.add_student("오류학생", [90, 80])
    print(f"에러 테스트: {message}")