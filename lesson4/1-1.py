from typing import List, Tuple, Optional

# 이번에 사용할 리스트 함수들!
#   list.append(item)        리스트 맨 끝에 항목 추가
#   list.insert(index, item) 특정 위치(index)에 항목 삽입
#   list.pop(index)          특정 위치(index)의 항목을 제거하고 반환
#   list[index]              인덱스로 항목에 접근
#   list[start : end]        슬라이싱: start 이상 end 미만의 항목들을 잘라내기
#   len(list)                리스트에 담긴 항목의 개수 반환
#   enumerate(list)          (인덱스, 값) 쌍으로 "열거". 루프 순회할 때 사용

# 만들어보기!
# 클래스(Class)
#   노래(Song)
#       __init__()
#       get_info()
#   플레이리스트(Playlist)
#       __init__()
#       add_song()
#       insert_song()
#       remove_song()
#       play_current()
#       next_song()
#       prev_song()
#       jump_to()
#       get_upcoming()
#       show_all()


class Song:
    """노래 클래스 - 플레이리스트에 담기는 노래 정보를 담는 클래스"""

    def __init__(self, _title: str, _artist: str) -> None:
        self.title: str = _title    # 노래 제목
        self.artist: str = _artist  # 아티스트

    def get_info(self) -> str:
        """노래 정보를 문자열로 반환"""
        return f"{self.title} - {self.artist}"


class Playlist:
    """플레이리스트 클래스 - 노래 목록과 재생 위치를 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name          # 플레이리스트 이름
        self.songs: List[Song] = []     # 노래들을 저장하는 리스트
        self.current_index: int = 0     # 현재 재생 중인 노래의 인덱스

    def add_song(self, _title: str, _artist: str) -> Tuple[bool, str]:
        """노래를 플레이리스트 맨 끝에 추가"""
        # === 내용 써보기! ===
        # 1. new_song 변수를 만들고, Song(_title, _artist) 를 저장
        # 2. self.songs 에 new_song 을 append 로 추가
        # 3. (True, "추가 완료 메시지") 반환 (아래 return 참고)

        return True, f"'{_title}' 이(가) 추가되었습니다. (총 {len(self.songs)}곡)"

    def insert_song(self, _index: int, _title: str, _artist: str) -> Tuple[bool, str]:
        """특정 위치에 노래를 삽입"""
        # === 내용 써보기! ===
        # 1. _index 가 0보다 작거나, len(self.songs) 보다 크면
        #    (False, "유효하지 않은 위치입니다. (0 ~ ... 사이여야 합니다)") 반환
        # 2. new_song 변수를 만들고, Song(_title, _artist) 를 저장
        # 3. self.songs 에 insert 를 사용해 _index 위치에 new_song 을 삽입
        # 4. 삽입 위치가 현재 재생 위치보다 앞이면 current_index 를 1 증가시키기
        #    (조건: len(self.songs) > 1 and _index <= self.current_index)
        # 5. (True, "삽입 완료 메시지") 반환 (아래 return 참고)

        return True, f"'{_title}' 이(가) [{_index}]번 위치에 삽입되었습니다."

    def remove_song(self, _index: int) -> Tuple[bool, str]:
        """특정 위치의 노래를 제거"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, (False, "플레이리스트가 비어있습니다.") 반환
        # 2. _index 가 0보다 작거나, len(self.songs) 이상이면
        #    (False, "유효하지 않은 위치입니다. (0 ~ ... 사이여야 합니다)") 반환
        # 3. removed 변수를 만들고, self.songs.pop(_index) 로 해당 노래를 제거하고 저장
        # 4. current_index 조정하기:
        #    - _index < self.current_index 이면 → self.current_index 를 1 감소
        #    - self.current_index >= len(self.songs) and self.current_index > 0 이면
        #      → self.current_index 를 len(self.songs) - 1 로 설정
        # 5. (True, "제거 완료 메시지") 반환 (아래 return 참고)

        return True, f"'{removed.title}' 이(가) 제거되었습니다."

    def play_current(self) -> Tuple[bool, str]:
        """현재 인덱스의 노래 정보를 반환"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, (False, "플레이리스트가 비어있습니다.") 반환
        # 2. current 변수를 만들고, self.songs[self.current_index] 를 저장
        # 3. (True, "재생 중 메시지") 반환 (아래 return 참고)

        return True, f"[{self.current_index + 1}/{len(self.songs)}] 재생 중: {current.get_info()}"

    def next_song(self) -> Tuple[bool, str]:
        """다음 노래로 이동"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, (False, "플레이리스트가 비어있습니다.") 반환
        # 2. self.current_index 가 len(self.songs) - 1 이상이면, (False, "마지막 곡입니다.") 반환
        # 3. self.current_index 를 1 증가시키기
        # 4. self.play_current() 를 반환 (아래 return 참고)

        return self.play_current()

    def prev_song(self) -> Tuple[bool, str]:
        """이전 노래로 이동"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, (False, "플레이리스트가 비어있습니다.") 반환
        # 2. self.current_index 가 0 이하이면, (False, "첫 번째 곡입니다.") 반환
        # 3. self.current_index 를 1 감소시키기
        # 4. self.play_current() 를 반환 (아래 return 참고)

        return self.play_current()

    def jump_to(self, _index: int) -> Tuple[bool, str]:
        """특정 인덱스로 바로 이동"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, (False, "플레이리스트가 비어있습니다.") 반환
        # 2. _index 가 0보다 작거나, len(self.songs) 이상이면
        #    (False, "유효하지 않은 위치입니다. (0 ~ ... 사이여야 합니다)") 반환
        # 3. self.current_index 에 _index 를 저장
        # 4. self.play_current() 를 반환 (아래 return 참고)

        return self.play_current()

    def get_upcoming(self, _n: int = 3) -> str:
        """현재 곡 이후 n곡을 미리보기"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, "플레이리스트가 비어있습니다." 반환
        # 2. upcoming 변수를 만들고, 슬라이싱으로 다음 _n 곡을 잘라내기
        #    self.songs[ self.current_index + 1 : self.current_index + 1 + _n ]
        # 3. len(upcoming) 이 0이면, "다음 곡이 없습니다." 반환
        # 4. result 변수를 만들고, f"=== 다음 {len(upcoming)}곡 ===\n" 를 저장
        # 5. for i, song in enumerate(upcoming): 로 반복문 시작
        #    result 에 f"  {i + 1}. {song.get_info()}\n" 를 더하기
        # 6. result 를 반환 (아래 return 참고)

        return result

    def show_all(self) -> str:
        """전체 플레이리스트를 출력 (현재 곡에 ▶ 표시)"""
        # === 내용 써보기! ===
        # 1. len(self.songs) 가 0이면, "플레이리스트가 비어있습니다." 반환
        # 2. result 변수를 만들고, f"=== {self.name} ({len(self.songs)}곡) ===\n" 를 저장
        # 3. for i, song in enumerate(self.songs): 로 반복문 시작
        #    - marker 변수를 만들고: i == self.current_index 이면 "▶ ", 아니면 "  " 저장
        #    - result 에 f"{marker}[{i}] {song.get_info()}\n" 를 더하기
        # 4. result 를 반환 (아래 return 참고)

        return result


if __name__ == "__main__":  # 이 파일 내에서만 실행됨!
    pl = Playlist("내 플레이리스트")  # 플레이리스트 생성!

    # === 아래 내용을 채워서 테스트 해보기! ===
    # 1. pl.add_song("Bohemian Rhapsody", "Queen") 실행하고 결과를 출력
    # 2. pl.add_song("Hotel California", "Eagles") 실행하고 결과를 출력
    # 3. pl.add_song("Stairway to Heaven", "Led Zeppelin") 실행하고 결과를 출력
    # 4. pl.add_song("Imagine", "John Lennon") 실행하고 결과를 출력
    # 5. pl.add_song("Smells Like Teen Spirit", "Nirvana") 실행하고 결과를 출력
    # 6. pl.show_all() 실행하고 결과를 출력
    #
    # 7. pl.play_current() 실행하고 결과를 출력 (현재 곡 확인)
    # 8. pl.next_song() 실행하고 결과를 출력
    # 9. pl.next_song() 실행하고 결과를 출력
    # 10. pl.get_upcoming(2) 실행하고 결과를 출력 (다음 2곡 미리보기)
    #
    # 11. pl.insert_song(2, "Yesterday", "The Beatles") 실행하고 결과를 출력
    # 12. pl.show_all() 실행하고 결과를 출력 (삽입 후 ▶ 위치 확인)
    #
    # 13. pl.remove_song(0) 실행하고 결과를 출력
    # 14. pl.show_all() 실행하고 결과를 출력 (제거 후 ▶ 위치 확인)
    #
    # 15. pl.jump_to(3) 실행하고 결과를 출력
    # 16. pl.prev_song() 실행하고 결과를 출력
    #
    # 17. pl.jump_to(0) 실행 후, pl.prev_song() 실행 (에러 확인)
    # 18. pl.jump_to(99) 실행 (에러 확인)