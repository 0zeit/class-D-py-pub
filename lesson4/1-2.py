from typing import List, Tuple

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
        self.title: str = _title   # 노래 제목
        self.artist: str = _artist # 아티스트

    def get_info(self) -> str:
        """노래 정보를 문자열로 반환"""
        return f"{self.title} - {self.artist}"

class Playlist:
    """플레이리스트 클래스 - 노래 목록과 재생 위치를 관리하는 클래스"""

    def __init__(self, _name: str) -> None:
        self.name: str = _name      # 플레이리스트 이름
        self.songs: List[Song] = [] # 노래들을 저장하는 리스트
        self.current_index: int = 0 # 현재 재생 중인 노래의 인덱스

    def add_song(self, _title: str, _artist: str) -> Tuple[bool, str]:
        """노래를 플레이리스트 맨 끝에 추가"""
        new_song: Song = Song(_title, _artist)
        self.songs.append(new_song)

        return True, f"'{_title}' 이(가) 추가되었습니다. (총 {len(self.songs)}곡)"

    def insert_song(self, _index: int, _title: str, _artist: str) -> Tuple[bool, str]:
        """특정 위치에 노래를 삽입"""
        if _index < 0 or _index > len(self.songs):
            return False, f"유효하지 않은 위치입니다. (0 ~ {len(self.songs)} 사이여야 합니다)"

        new_song: Song = Song(_title, _artist)
        self.songs.insert(_index, new_song)

        # 삽입 위치가 현재 재생 위치보다 앞이면 current_index를 한 칸 밀어야 함
        # (삽입 전에 노래가 있었던 경우에만)
        if len(self.songs) > 1 and _index <= self.current_index:
            self.current_index += 1

        return True, f"'{_title}' 이(가) [{_index}]번 위치에 삽입되었습니다."

    def remove_song(self, _index: int) -> Tuple[bool, str]:
        """특정 위치의 노래를 제거"""
        if len(self.songs) == 0:
            return False, "플레이리스트가 비어있습니다."

        if _index < 0 or _index >= len(self.songs):
            return False, f"유효하지 않은 위치입니다. (0 ~ {len(self.songs) - 1} 사이여야 합니다)"

        removed: Song = self.songs.pop(_index)

        # 제거된 위치에 따라 current_index 조정
        if _index < self.current_index:
            # 현재 곡 앞이 제거됐으면 한 칸 당기기
            self.current_index -= 1
        elif self.current_index >= len(self.songs) and self.current_index > 0:
            # 현재 곡이 제거되거나, 리스트 끝을 넘어서면 마지막 곡으로 이동
            self.current_index = len(self.songs) - 1

        return True, f"'{removed.title}' 이(가) 제거되었습니다."

    def play_current(self) -> Tuple[bool, str]:
        """현재 인덱스의 노래 정보를 반환"""
        if len(self.songs) == 0:
            return False, "플레이리스트가 비어있습니다."

        current: Song = self.songs[self.current_index]

        return True, f"[{self.current_index + 1}/{len(self.songs)}] 재생 중: {current.get_info()}"

    def next_song(self) -> Tuple[bool, str]:
        """다음 노래로 이동"""
        if len(self.songs) == 0:
            return False, "플레이리스트가 비어있습니다."

        if self.current_index >= len(self.songs) - 1:
            return False, "마지막 곡입니다."

        self.current_index += 1

        return self.play_current()

    def prev_song(self) -> Tuple[bool, str]:
        """이전 노래로 이동"""
        if len(self.songs) == 0:
            return False, "플레이리스트가 비어있습니다."

        if self.current_index <= 0:
            return False, "첫 번째 곡입니다."

        self.current_index -= 1

        return self.play_current()

    def jump_to(self, _index: int) -> Tuple[bool, str]:
        """특정 인덱스로 바로 이동"""
        if len(self.songs) == 0:
            return False, "플레이리스트가 비어있습니다."

        if _index < 0 or _index >= len(self.songs):
            return False, f"유효하지 않은 위치입니다. (0 ~ {len(self.songs) - 1} 사이여야 합니다)"

        self.current_index = _index

        return self.play_current()

    def get_upcoming(self, _n: int = 3) -> str:
        """현재 곡 이후 n곡을 미리보기 (슬라이싱 활용)"""
        if len(self.songs) == 0:
            return "플레이리스트가 비어있습니다."

        upcoming: List[Song] = self.songs[self.current_index + 1 : self.current_index + 1 + _n]

        if len(upcoming) == 0:
            return "다음 곡이 없습니다."

        result: str = f"=== 다음 {len(upcoming)}곡 ===\n"
        for i, song in enumerate(upcoming):
            result += f"  {i + 1}. {song.get_info()}\n"

        return result

    def show_all(self) -> str:
        """전체 플레이리스트를 출력 (현재 곡에 ▶ 표시)"""
        if len(self.songs) == 0:
            return "플레이리스트가 비어있습니다."

        result: str = f"=== {self.name} ({len(self.songs)}곡) ===\n"

        for i, song in enumerate(self.songs):
            marker: str = "▶ " if i == self.current_index else "  "
            result += f"{marker}[{i}] {song.get_info()}\n"

        return result


if __name__ == "__main__":
    pl = Playlist("내 플레이리스트")

    # 노래 추가
    pl.add_song("Bohemian Rhapsody", "Queen")
    pl.add_song("Hotel California", "Eagles")
    pl.add_song("Stairway to Heaven", "Led Zeppelin")
    pl.add_song("Imagine", "John Lennon")
    pl.add_song("Smells Like Teen Spirit", "Nirvana")

    print(pl.show_all())

    # 현재 곡 재생 및 넘기기
    success, message = pl.play_current()
    print(message)

    success, message = pl.next_song()
    print(message)

    success, message = pl.next_song()
    print(message)
    print()

    # 다음 곡 미리보기 (슬라이싱)
    print(pl.get_upcoming(2))

    # 중간에 노래 삽입
    success, message = pl.insert_song(2, "Yesterday", "The Beatles")
    print(message)
    print(pl.show_all())

    # 특정 위치 노래 제거
    success, message = pl.remove_song(0)
    print(message)
    print(pl.show_all())

    # 바로 이동
    success, message = pl.jump_to(3)
    print(message)

    success, message = pl.prev_song()
    print(message)
    print()

    # 경계값 테스트
    pl.jump_to(0)
    success, message = pl.prev_song()
    print(f"에러 테스트 (첫 곡에서 이전): {message}")

    success, message = pl.jump_to(99)
    print(f"에러 테스트 (범위 초과): {message}")