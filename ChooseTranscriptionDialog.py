from aqt.qt import QAction, QMessageBox, QVBoxLayout, QLabel, QDialog, QPushButton, QComboBox, QHBoxLayout

from .utils import SpecialWord

from .utils import get_transcription_of_the, get_transcription_of_to, make_a_word_without_transcription
from .FlowLayout import FlowLayout
from .debug import debug
from .local_dictionary import cache_transcription


class VariantsOfTranscription(QComboBox):
    def __init__(self, indexInTranscription, *args, **kwargs):
        super(VariantsOfTranscription, self).__init__(*args, **kwargs)
        self.indexInTranscription = indexInTranscription
        self.addItem('Keep it as is')

    def addItems(self, *args, **kwargs):
        super().addItems(*args, **kwargs)
        self.setCurrentIndex(1)


class ChooseTranscriptionDialog (QDialog):
    def __init__(self, words:list, transcriptions:list, *args, max_width=300, **kwargs):
        super(ChooseTranscriptionDialog, self).__init__(*args, **kwargs)
        self.max_width = max_width
        self.flow_layout = FlowLayout(max_width)
        self.transcriptions = transcriptions
        self.doneTranscriptions = []
        self.words = words
        
        for i in range(len(transcriptions)):
            # 'the'
            if isinstance(transcriptions[i], SpecialWord):
                if transcriptions[i].word == 'the':
                    if i == len(transcriptions) - 1:
                        self.flow_layout.addWidget(QLabel(get_transcription_of_the(None)))
                    else:
                        if isinstance(transcriptions[i+1], list):
                            self.flow_layout.addWidget(QLabel(get_transcription_of_the(transcriptions[i+1][0])))
                        else:
                            self.flow_layout.addWidget(QLabel(get_transcription_of_the(transcriptions[i+1])))
                elif transcriptions[i].word == 'to':
                    if i == len(transcriptions) - 1:
                        self.flow_layout.addWidget(QLabel(get_transcription_of_to(None)))
                    else:
                        if isinstance(transcriptions[i+1], list):
                            self.flow_layout.addWidget(QLabel(get_transcription_of_to(transcriptions[i+1][0])))
                        else:
                            self.flow_layout.addWidget(QLabel(get_transcription_of_to(transcriptions[i+1])))
            
            elif isinstance(transcriptions[i], str):
                #self.flow_layout.addWidget(QLabel(transcriptions[i]))
                cb_variants = VariantsOfTranscription(self)
                cb_variants.addItems([transcriptions[i]])
                cb_variants.indexInTranscriptions = i
                cb_variants.currentIndexChanged.connect(self.on_combobox_changed)
                self.flow_layout.addWidget(cb_variants)
            elif isinstance(transcriptions[i], list):
                cb_variants = VariantsOfTranscription(self)
                cb_variants.addItems(transcriptions[i])
                cb_variants.indexInTranscriptions = i
                cb_variants.currentIndexChanged.connect(self.on_combobox_changed)
                self.flow_layout.addWidget(cb_variants)

        self.ok_button = QPushButton('ok')
        self.ok_button.clicked.connect(self.on_ok_clicked)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(' '.join(words)))
        layout.addWidget(self.flow_layout)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def on_combobox_changed(self):
        i = self.sender().indexInTranscriptions
        if i != 0:
            if self.transcriptions[i-1] == None:
                self.flow_layout.getWidgetById(i-1).setText(get_transcription_of_the(self.sender().currentText()))
    
    def on_ok_clicked(self):
        for i in range(len(self.transcriptions)):
            if isinstance(self.flow_layout.getWidgetById(i), QLabel):
                self.doneTranscriptions.append(self.flow_layout.getWidgetById(i).text())
            else: #list
                curText = self.flow_layout.getWidgetById(i).currentText() if self.flow_layout.getWidgetById(i).currentIndex() != 0 else make_a_word_without_transcription(self.words[i])
                self.doneTranscriptions.append(curText)
                cache_transcription(self.words[i], curText)

        self.close()

    def getDoneTranscriptions(self):
        return self.doneTranscriptions
    

    

    