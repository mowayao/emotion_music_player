from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.phonon import *
import os
import cv2
import dlib
import sys
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s



class MainWindow(QWidget):


    def __init__(self):
        QWidget.__init__(self)
        self.resize(1088, 688)
        self.setWindowTitle("Emotion Player")
        self.capBtn = QPushButton("capture", self)
        self.capBtn.clicked.connect(self.caputure_emotion)
        #self.connect(self.capBtn, SIGNAL("clicked"), self.caputure_emotion)
        self.capBtn.setGeometry(QRect(250, 500, 100, 40))
        self.videoImg = QLabel(self)
        self.videoImg.setGeometry(QRect(100, 80, 400, 400))
        self.videoImg.setPixmap(QPixmap("1.jpg").scaled(400, 400))
        self.faceImg = QLabel(self)
        self.faceImg.setGeometry(QRect(550, 150, 100, 100))

        self.emotionImg = QLabel(self)
        self.emotionImg.setGeometry(QRect(550, 300, 100, 100))
        self.emotionImg.setPixmap(QPixmap("./nahan.jpg"))

        self.musicTable = QTableWidget(0, 4)
        #self.musicTable.setHorizontalHeaderLabels(headers)
        self.musicTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.musicTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.musicTable.setGeometry(QRect(700, 80, 300, 400))
        self.musicTable.resizeColumnsToContents()
        if self.musicTable.columnWidth(0) > 300:
            self.musicTable.setColumnWidth(0, 300)
        self.volumeSlider = Phonon.VolumeSlider(self)
        self.volumeSlider.setGeometry(QRect(900, 550, 100, 35))
        self.volumeSlider.setObjectName(_fromUtf8("volumeSlider"))
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.mediaObject = Phonon.MediaObject(self)
        self.mediaObject.stateChanged.connect(self.stateChanged)

        self.metaInformationResolver = Phonon.MediaObject(self)
        self.metaInformationResolver.setCurrentSource(Phonon.MediaSource(u'/Users/mowayao/Desktop/code/emotion_player/songs/My Love - Westlife.mp3'))
        self.mediaObject.setTickInterval(1000)
        self.mediaObject.tick.connect(self.tick)
        Phonon.createPath(self.mediaObject, self.audioOutput)

        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.volumeSlider.setAudioOutput(self.audioOutput)
        self.seekSlider = Phonon.SeekSlider(self)
        self.seekSlider.setMediaObject(self.mediaObject)
        self.seekSlider.setGeometry(QRect(700, 500, 250, 35))
        self.timeLcd = QLCDNumber(self)
        self.timeLcd.display('00:00')
        self.timeLcd.setGeometry(QRect(950, 500, 50, 35))

        self.setupActions()
        self.bar = QToolBar(self)
        self.bar.addAction(self.playAction)
        self.bar.addAction(self.pauseAction)
        self.bar.addAction(self.stopAction)
        self.bar.setGeometry(QRect(750, 600, 160, 40))

        self.sources = []
        metaData = self.metaInformationResolver.metaData()
        title = metaData.get('TITLE', [''])[0]
        currentRow = self.musicTable.rowCount()
        self.musicTable.insertRow(currentRow)
        if not title:
            title = self.metaInformationResolver.currentSource().fileName()
        titleItem = QTableWidgetItem(title)
        #titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)

        artist = metaData.get('ARTIST', [''])[0]
        artistItem = QTableWidgetItem(artist)
        #artistItem.setFlags(artistItem.flags() ^ Qt.ItemIsEditable)

        album = metaData.get('ALBUM', [''])[0]
        albumItem = QTableWidgetItem(album)
        #albumItem.setFlags(albumItem.flags() ^ Qt.ItemIsEditable)

        year = metaData.get('DATE', [''])[0]
        yearItem = QTableWidgetItem(year)
        #yearItem.setFlags(yearItem.flags() ^ Qt.ItemIsEditable)
        self.musicTable.setItem(currentRow, 0, titleItem)
        self.musicTable.setItem(currentRow, 1, artistItem)
        self.musicTable.setItem(currentRow, 2, albumItem)
        self.musicTable.setItem(currentRow, 3, yearItem)
        self.mediaObject.setCurrentSource(self.metaInformationResolver.currentSource())
        #self.listSongs.addItems('test.mp3')
    def caputure_emotion(self):
        detector=dlib.get_frontal_face_detector()
        img = cv2.imread('1.jpg')
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = detector(img, 2)
        if len(faces) > 0:
            face=max(faces, key=lambda rect: rect.width() * rect.height())
        [x1,x2,y1,y2]=[face.left(),face.right(),face.top(),face.bottom()]
        face = img[y1: y2, x1: x2]
        cv2.imwrite("face.jpg", face)
        self.faceImg.setPixmap(QPixmap("face.jpg").scaled(100, 100))
    def setupActions(self):
        self.playAction = QAction(
            self.style().standardIcon(QStyle.SP_MediaPlay), "Play",
            self, shortcut="Ctrl+P", enabled=False,
            triggered=self.mediaObject.play)

        self.pauseAction = QAction(
            self.style().standardIcon(QStyle.SP_MediaPause),
            "Pause", self, shortcut="Ctrl+A", enabled=False,
            triggered=self.mediaObject.pause)

        self.stopAction = QAction(
            self.style().standardIcon(QStyle.SP_MediaStop), "Stop",
            self, shortcut="Ctrl+S", enabled=False,
            triggered=self.mediaObject.stop)
    def sourceChanged(self, source):
        self.musicTable.selectRow(self.sources.index(source))
        self.timeLcd.display('00:00')
    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.mediaObject.errorType() == Phonon.FatalError:
                QMessageBox.warning(self, "Fatal Error",
                                          self.mediaObject.errorString())
            else:
                QMessageBox.warning(self, "Error",
                                          self.mediaObject.errorString())

        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)

        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.timeLcd.display("00:00")

        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)
    def tick(self, time):
        displayTime = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.timeLcd.display(displayTime.toString('mm:ss'))
        #self.setCursor(Qt.PointingHandCursor)
        #self.btnStart.setText(_fromUtf8(""))
        #self.btnStart.setObjectName(_fromUtf8("btnStart"))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
