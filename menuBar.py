from PySide6.QtWidgets import QMenuBar, QMenu, QFileDialog, QWidget, QSizePolicy
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt


# Creating the File button
class FileMenu(QMenu):
	def __init__(self, parent, textEditor):
		super().__init__()
		self.setTitle("File")
  
		self.textEditor = textEditor

		# Instantiating the buttons
		openAction = Open(self, self.textEditor)
		saveAction = Save(self, self.textEditor)
		saveAsAction = SaveAs(self, self.textEditor)

		self.addActions([openAction, saveAction, saveAsAction]) # Adding his buttons

# A option from the file button
class Open(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor

		self.setText("Open")
		
		# Connecting this button to the function wich deletes text of the text field and the function wich open a file
		self.triggered.connect(self.textEditor.clear)
		self.triggered.connect(self.openFile)

	# The function wich open a file
	def openFile(self):
		fileDialog = QFileDialog() # I create the file explorer
		filePath, _ = fileDialog.getOpenFileName(None, "Open File", "", "Text Files(*.txt)") # Opening the file explorer and picking up the path from the opened file
		
		file = open(filePath, "r") # Opening the file in "r" mode wich means we will read the file
		text = file.read() # Getting the text from the file
		file.close() # Closing the file to avoid problems

		self.textEditor.insertPlainText(text) # Putting the text on the text field
		self.textEditor.currentFilePath = filePath # Updating the actual open file

# A option from the file button
class Save(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor
		
		self.setText("Save")
  
		self.triggered.connect(self.saveFile) # I connect the button to his function
  
	def saveFile(self):
		text_ = self.textEditor.toPlainText() # Picking up the text wich is in QTextEdit
  
		filePath = self.textEditor.filePath # Take the path of the file wich was already open
		file = open(filePath, "w") # Opening the file in "w" mode wich means we will write in this file
		file.write(text_) # I write in the file
		file.close() # Closing the file to avoid problems

# A option from the file button
class SaveAs(QAction):
	def __init__(self, parent, textEditor):
		super().__init__(parent)
		self.textEditor = textEditor
		
		self.setText("Save As")
  
		self.triggered.connect(self.saveAsFile) # Connecting the button to his function
  
	def saveAsFile(self):
		fileDialog = QFileDialog()
		filePath, _ = fileDialog.getSaveFileName(None, "Save File", "NewFile", "Text Files(*.txt)")

		if filePath:
			text_ = self.textEditor.toPlainText() # Picking up the text wich is in QTextEdit
	
			# self.textEditor.filePath = filePath # Updating the actual open file
	
			file = open(filePath, "w") # Opening the file in "w" mode wich means we will write in this file
			file.write(text_) # I write in the file
			file.close() # Closing the file to avoid problems

			self.textEditor.currentFilePath = filePath # Updating the actual open file
		
class MenuBar(QMenuBar):
	def __init__(self, parent, textEditor, mainWindow):
		super().__init__(parent)
		self.textEditor = textEditor
		self.mainWindow = mainWindow

		fileMenu = FileMenu(self, textEditor)
		self.addMenu(fileMenu)
	
		# spacer = QWidget(self)
		# spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		# self.setCornerWidget(spacer, Qt.TopRightCorner)