from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QUrl

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap("assets/images/sMHxi9-removebg-preview.png"))
        self.setScaledContents(True)
        self.setFixedSize(500, 500)


        self.oldPos = None
        self.pressPos = None
        self.is_dragging = False

        self.player = QSoundEffect()
        self.player.setSource(QUrl.fromLocalFile("assets/sounds/styk.wav"))
        self.player.setVolume(1.0)

        self.move_sound = QSoundEffect()
        self.move_sound.setSource(QUrl.fromLocalFile("assets/sounds/move.wav"))
        self.move_sound.setLoopCount(QSoundEffect.Infinite)
        self.move_sound.setVolume(5.0)  # можно настроить громкость

        self.animation = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            self.pressPos = event.globalPos()
            self.is_dragging = False

            # Сброс звуков при новом нажатии
            self.player.stop()
            self.move_sound.stop()

    def mouseMoveEvent(self, event):
        if self.oldPos is None:
            return

        move_threshold = 5  # порог для определения перемещения
        if (event.globalPos() - self.pressPos).manhattanLength() > move_threshold:
            if not self.is_dragging:
                self.is_dragging = True

                self.move_sound.play()

        delta = event.globalPos() - self.oldPos
        self.parent().move(self.parent().pos() + delta)
        self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if self.move_sound.isPlaying():
            self.move_sound.stop()

        self.jump()
        self.is_dragging = False
        self.oldPos = None

    def jump(self):
        self.player.play()

        arrowwindow = self.parent()
        start_pos = arrowwindow.pos()
        end_pos = QPoint(start_pos.x(), start_pos.y() - 20)  # смещение вверх на 20 пикселей

        self.animation = QPropertyAnimation(arrowwindow, b'pos', self)
        self.animation.setDuration(200)
        self.animation.setKeyValueAt(0.0, start_pos)
        self.animation.setKeyValueAt(0.5, end_pos)
        self.animation.setKeyValueAt(1.0, start_pos)
        self.animation.start()