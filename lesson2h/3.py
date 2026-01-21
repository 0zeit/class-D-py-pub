import sys

from PyQt6.QtCore import Qt, QPointF, QTimer
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent
from PyQt6.QtWidgets import QApplication, QWidget


class Ball:
    def __init__(self, _radius, _pos, _vel=(0, 0)):
        self.r = _radius
        self.pos = QPointF(float(_pos[0]), float(_pos[1]))  # 위치 (Position)
        self.vel = QPointF(float(_vel[0]), float(_vel[1]))  # 속도 (Velocity)
        self.m = _radius * 2                                # 질량 (Mass)

    def contains(self, _c_pos: QPointF) -> bool:
        """마우스 커서가 공 안에 있는지 확인"""
        dx = _c_pos.x() - self.pos.x()
        dy = _c_pos.y() - self.pos.y()

        return (dx * dx + dy * dy) <= (self.r * self.r)

    def update_position(self, _dt):
        """시간(_dt)만큼 공의 위치를 업데이트"""
        self.pos += self.vel * _dt

# QWidget을 상속받아 QWidget내에 들어있는 것들도 사용가능.
# 클래스명에 괄호 () 를 쓰면 상속받을 클래스 지정 가능.
# 클래스명은 자유롭게 지정가능!
class MyWidget(QWidget):
    # __init__ 은 클래스의 생성자. 이 경우에는 MyWidget의 초기화를 담당.
    def __init__(self):
        # QWidget 클래스를 초기화함
        super().__init__()
        self.setWindowTitle("PyQT 수업2 Hard")
        self.setAutoFillBackground(True)
        self.resize(600, 600)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)

        self.balls = [                       # Ball()을 할때마다 Ball의 __init__이 불러짐
            Ball(20, (150, 150), (100, 1)),    # 속도: 오른쪽 + 아래
            Ball(25, (400, 200), (-1, 200)),   # 속도: 왼쪽 + 아래
            Ball(30, (300, 400), (1.5, -100)), # 속도: 오른쪽 + 위
        ]
        self.drag_idx = None
        self.drag_offset = QPointF()
        self.last_mouse_pos = QPointF()      # 마지막 마우스 위치 저장
        self.drag_velocity = QPointF(0, 0)   # 드래그 속도 저장        
        self.elasticity = 0.95  # 탄성 계수 e, 0.95의 경우 조금씩 에너지를 손실.

        self.timer = QTimer()
        self.timer.timeout.connect(self.physics_update)
        self.timer.start(16) # 타이머 설정: 16ms마다 업데이트 (약 60 FPS)

    def physics_update(self):
        """물리 시뮬레이션 업데이트 코드"""
        if self.drag_idx is not None: # 드래그 중에는 물리 시뮬레이션 멈춤
            return                    # 이와 같이 코드가 실행되기 전에 if로 체크하는걸 "이른 반환(Early Return)" 이라함!

        dt = 0.016  # 시간 간격 (약 60 FPS)

        for ball in self.balls:      # in 키워드를 활용하면 배열안의 오브젝트들을 하나씩 꺼낼수 있음!   
            ball.update_position(dt) # 1. 모든 공의 위치 업데이트

        self.handle_wall_collision() # 2. 벽 충돌 처리
        self.handle_ball_collision() # 3. 공-공 충돌 처리
        self.update()                # 4. 화면 다시 그리기

    def handle_wall_collision(self):
        """벽과의 충돌 처리"""
        width = self.width()
        height = self.height()

        for ball in self.balls:
            # 왼쪽 벽
            if ball.pos.x() - ball.r < 0:
                ball.pos.setX(ball.r)
                ball.vel.setX(-ball.vel.x() * self.elasticity)

            # 오른쪽 벽
            if ball.pos.x() + ball.r > width:
                ball.pos.setX(width - ball.r)
                ball.vel.setX(-ball.vel.x() * self.elasticity)

            # 위쪽 벽
            if ball.pos.y() - ball.r < 0:
                ball.pos.setY(ball.r)
                ball.vel.setY(-ball.vel.y() * self.elasticity)

            # 아래쪽 벽
            if ball.pos.y() + ball.r > height:
                ball.pos.setY(height - ball.r)
                ball.vel.setY(-ball.vel.y() * self.elasticity)

    def handle_ball_collision(self):
        """공-공 충돌 처리 (탄성충돌 물리 적용)"""
        n = len(self.balls)

        for i in range(n):
            for j in range(i + 1, n):
                ball1 = self.balls[i]
                ball2 = self.balls[j]

                # 두 공 사이의 거리 벡터
                dx = ball2.pos.x() - ball1.pos.x()
                dy = ball2.pos.y() - ball1.pos.y()
                distance = (dx * dx + dy * dy) ** 0.5 # 유클리드 거리(Euclidean Distance)

                # 충돌 감지: 두 공의 반지름 합보다 거리가 작으면 충돌
                if (distance < (ball1.r + ball2.r)) and (0 < distance):
                    # 충돌 방향의 단위벡터 (Normal vector)
                    nx = dx / distance
                    ny = dy / distance

                    # 공들이 겹친 만큼 분리 (Separation)
                    overlap = (ball1.r + ball2.r) - distance
                    ball1.pos.setX(ball1.pos.x() - nx * overlap * 0.5)
                    ball1.pos.setY(ball1.pos.y() - ny * overlap * 0.5)
                    ball2.pos.setX(ball2.pos.x() + nx * overlap * 0.5)
                    ball2.pos.setY(ball2.pos.y() + ny * overlap * 0.5)

                    # 충돌 방향의 상대 속도
                    dvx = ball2.vel.x() - ball1.vel.x()
                    dvy = ball2.vel.y() - ball1.vel.y()
                    dvn = dvx * nx + dvy * ny

                    # 이미 멀어지고 있으면 충돌 처리 안함
                    if dvn > 0:
                        continue

                    # 충돌 임펄스 계산 (Impulse)
                    # 공의 에너지 J = -(1 + e) * dvn / (1/m1 + 1/m2)
                    impulse = -(1 + self.elasticity) * dvn / (1 / ball1.m + 1 / ball2.m)

                    # 속도 변경 (F = ma, v = v + a*dt, a = F/m)
                    ball1.vel.setX(ball1.vel.x() - impulse * nx / ball1.m)
                    ball1.vel.setY(ball1.vel.y() - impulse * ny / ball1.m)
                    ball2.vel.setX(ball2.vel.x() + impulse * nx / ball2.m)
                    ball2.vel.setY(ball2.vel.y() + impulse * ny / ball2.m)

    def paintEvent(self, _e):
        """공을 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)

        for ball in self.balls:
            # 공의 크기에 따라 색상 변경 (시각적 효과)
            gray_value = int(200 - ball.r * 3)
            ball_color = QColor(gray_value, gray_value, gray_value)
            painter.setBrush(QBrush(ball_color))
            painter.drawEllipse(ball.pos, ball.r, ball.r)

    def mouseMoveEvent(self, _e: QMouseEvent):
        """마우스 드래그 시 공 이동"""
        if self.drag_idx is None:
            return

        cursor = _e.position()
        ball = self.balls[self.drag_idx]

        if self.last_mouse_pos.x() != 0 or self.last_mouse_pos.y() != 0: # 현재 위치와 이전 위치의 차이로 속도 계산
            self.drag_velocity = (cursor - self.last_mouse_pos) * 3      # 마우스 이동 속도 = (현재 위치 - 이전 위치) * 속도 배율

        ball.pos = cursor - self.drag_offset # 공의 위치 업데이트

        self.last_mouse_pos = cursor # 이전 마우스 위치 저장 (다음 프레임에서 사용)
        self.update()

    def mousePressEvent(self, _e: QMouseEvent):
        """마우스 클릭으로 공 선택"""
        if _e.button() != Qt.MouseButton.LeftButton:
            return

        cursor = _e.position()

        for idx, ball in enumerate(self.balls):
            if ball.contains(cursor):
                self.drag_idx = idx
                self.drag_offset = cursor - ball.pos
                self.last_mouse_pos = cursor          # 마우스 위치 초기화
                self.drag_velocity = QPointF(0, 0)    # 드래그 속도 초기화
                ball.vel = QPointF(0, 0)              # 잡는 순간 공의 속도 0으로

                break

    def mouseReleaseEvent(self, _e: QMouseEvent):
        """마우스를 놓으면 공 놓기 + 드래그 속도 적용"""
        if _e.button() == Qt.MouseButton.LeftButton:
            if self.drag_idx is not None:
                self.balls[self.drag_idx].vel = self.drag_velocity # 공을 놓을 때 드래그 속도를 공의 속도로 설정
                
            self.drag_idx = None
            self.last_mouse_pos = QPointF()       # 마우스 위치 초기화
            self.drag_velocity = QPointF(0, 0)    # 드래그 속도 초기화


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    
    sys.exit(app.exec())