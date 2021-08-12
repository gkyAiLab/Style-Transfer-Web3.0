import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def slotPrint(self):
        self.image = QImage()

        photo = os.path.join(os.getcwd(),'static')
        photo = os.path.join(photo, 'picture')
        photo_path = os.path.join(photo, 'picture.png')
            
        self.image.load(photo_path)

        # 实例化打印图像对象
        printer = QPrinter()

        painter = QPainter(printer)
        # 实例化视图窗口
        rect = painter.viewport()
        #set paper w and h
        rect.setWidth(640)
        rect.setHeight(320)
        # 获取图片的尺寸
        size = self.image.size()
        size.scale(rect.size(),Qt.KeepAspectRatio)#keep the ratio of w and h

        # 设置视图窗口的属性
        painter.setViewport(rect.x(), rect.y(), size.width(), size.height())

        # #设置窗口的大小为图片的尺寸，并在窗口内绘制图片
        painter.setWindow(0, 0, size.width(), size.height())
        painter.drawImage(0, 0, self.image)
        painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.slotPrint()
    sys.exit(app.exec_())