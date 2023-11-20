from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QStatusBar, QFileDialog, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QShortcut, QKeySequence, QFont, QTextOption
from menuBar import MenuBar
import qdarkstyle


# Creating the status bar
class StatusBar(QStatusBar):
    def __init__(self, textEditor) -> None:
        super().__init__()

        self.fileLabel = QLabel(textEditor.currentFilePath)
        self.addWidget(self.fileLabel)

#region TEXTEDITOR
class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setUndoRedoEnabled(True) # Activating the Ctrl + C to copy and Ctrl + V to paste
        self.setWordWrapMode(QTextOption.NoWrap) # Deactivating the world wrap

        self.currentFilePath = "" # Picking up the currently open file

#endregion

#region MAINWINDOW
class MainWindow(QMainWindow): # Main Window
	"""
    Todo: Fix the text enconding when opening a file
    """
    
	def __init__(self) -> None:
		super().__init__()
		
		self.initUI() # Builder command of the UI
		
	def initUI(self):
		self.setWindowTitle("PyCode Studio") # Title of the window
		self.resize(QApplication.primaryScreen().size().width() - 20, QApplication.primaryScreen().size().height() - 75) # Resizing the window to te screen size minus 20, 75
		self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6()) # Setting the theme

		self.textEditorLayout = QVBoxLayout()

		#region SHORCUT KEYS
		self.newFileShortcut = QShortcut(QKeySequence("Ctrl+N"), self) # Tecla de atalho pra abrir um novo arquivo
		self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self) # Tecla de atalho pra salvar o arquivo
		#endregion

		#region CONNECTING THE SHORCUT KEYS TO HIS COMMANDS
		self.newFileShortcut.activated.connect(self.newFile)
		self.saveShortcut.activated.connect(self.saveFile)
		#endregion

		# Creating the text field
		self.textEditor = TextEditor()
		self.textEditorLayout.addWidget(self.textEditor)
   
		# Creating the status bar
		self.myStatusBar = StatusBar(self.textEditor)
		self.setStatusBar(self.myStatusBar)
    
		# Creating the menu bar
		self.myMenuBar = MenuBar(self, self.textEditor, self)
		self.setMenuBar(self.myMenuBar)

		# Creating the text editor container
		textEditorContainer = QWidget()
		textEditorContainer.setLayout(self.textEditorLayout)

		self.setCentralWidget(textEditorContainer) # Setting the text editor as the central widget of the app

		self.show()
  
	def saveFile(self): # Function of the shorcut key saveShorcut
		text_ = self.textEditor.toPlainText() # Get the text wich is in QTextEdit
  
		filePath = self.textEditor.filePath # Picking up the currently open file
		file = open(filePath, "w") # Open the file in the mode "w" wich means i will write in this file
		file.write(text_) # Write in the file
		file.close() # Closing the file to avoid problems
  
	def newFile(self): # Function of the shorcut key newFileShorcut
		fileDialog = QFileDialog() # I create the file explorer
		path, _ = fileDialog.getSaveFileName(None, "Create a new file", "NewFile", "All Files(*.txt)") # Opening the file explorer and picking up the path from the new file

		self.textEditor.currentFilePath = path # Setting the actual open file as the new file
		self.textEditor.clear() # Clearing the text of previous files

#endregion

if __name__ == "__main__":
	app = QApplication()

	app.setFont(QFont("Consolas", 16))

	window = MainWindow()

	app.exec()