import sys

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QMouseEvent
from PyQt6.QtWidgets import QApplication, QWidget


# QWidget을 상속받아 QWidget내에 들어있는 것들도 사용가능.
class MyWidget(QWidget):
    # __init__: 클래스의 생성자. 이 경우에는 MyWidget의 초기화를 담당.
    def __init__(self):
        # QWidget 클래스를 초기화함
        super().__init__()
        self.setWindowTitle("PyQT 수업2 Hard")
        self.setAutoFillBackground(True)
        self.resize(600, 600)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(p)


if __name__ == "__main__":  # 이 파이썬 파일의 실행 진입점
    app = QApplication(sys.argv)
    window = MyWidget()  # 여기서 MyWidget의 __init__이 호출된다.
    window.show()

    sys.exit(app.exec())
