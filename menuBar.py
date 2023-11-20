from PySide6.QtWidgets import QMenuBar, QMenu, QFileDialog, QWidget, QSizePolicy
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt


class FileMenu(QMenu):
	def __init__(self, parent, textEditor):
		super().__init__()
		self.setTitle("File")
  
		self.textEditor = textEditor
  
		openAction = Open(self, self.textEditor)
		saveAction = Save(self, self.textEditor)
		saveAsAction = SaveAs(self, self.textEditor)

		self.addActions([openAction, saveAction, saveAsAction])

class Open(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor

		self.setText("Open")
		
		self.triggered.connect(self.textEditor.clear)
		self.triggered.connect(self.openFile)

	def openFile(self):
		fileDialog = QFileDialog()
		filePath, _ = fileDialog.getOpenFileName(None, "Open File", "", "Text Files(*.txt)")
		
		file = open(filePath, "r")
		text = file.read()
		file.close()

		self.textEditor.insertPlainText(text)
		self.textEditor.currentFilePath = filePath
  
class Save(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor
		
		self.setText("Save")
  
		self.triggered.connect(self.saveFile) # Conecto o botão a função correspondente
  
	def saveFile(self):
		text_ = self.textEditor.toPlainText() # Pega o texto que esta no QTextEdit
  
		filePath = self.textEditor.filePath # Pega o arquivo atual que já estava aberto
		file = open(filePath, "w") # Abro o arquivo no modo "w" que significa que eu vou escrever nesse arquivo
		file.write(text_) # Escrevo no arquivo
		file.close() # Fecho o arquivo pra evitar problemas
  
class SaveAs(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor
		
		self.setText("Save As")
  
		self.triggered.connect(self.saveAsFile) # Conecto o botão a função correspondente
  
	def saveAsFile(self):
		fileDialog = QFileDialog()
		filePath, _ = fileDialog.getSaveFileName(None, "Save File", "", "Text Files(*.txt)")

		if filePath:
			text_ = self.textEditor.toPlainText() # Pega o texto que esta no QTextEdit
	
			self.textEditor.filePath = filePath
	
			file = open(filePath, "w")
			file.write(text_)
			file.close()

			self.textEditor.currentFilePath = filePath
		
class MenuBar(QMenuBar):
	def __init__(self, parent, textEditor, mainWindow):
		super().__init__(parent)
		self.textEditor = textEditor
		self.mainWindow = mainWindow

		fileMenu = FileMenu(self, textEditor)
		self.addMenu(fileMenu)
	
		spacer = QWidget(self)
		spacer.setStyleSheet("QWidget { background-color: red; }")
		spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.setCornerWidget(spacer, Qt.TopRightCorner)
	
		self.addMenu(self.exitMenu)