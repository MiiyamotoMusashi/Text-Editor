from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QStatusBar, QFileDialog, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QShortcut, QKeySequence, QFont, QTextOption
from menuBar import MenuBar
import qdarkstyle


class StatusBar(QStatusBar):
    def __init__(self, textEditor) -> None:
        super().__init__()

        self.fileLabel = QLabel(textEditor.currentFilePath)
        self.addWidget(self.fileLabel)

#region TEXTEDITOR
class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setUndoRedoEnabled(True)
        self.setWordWrapMode(QTextOption.NoWrap)

        self.currentFilePath = "" # Caminho do arquivo que está aberto atualmente

#endregion

#region MAINWINDOW
class MainWindow(QMainWindow): # Janela principal
	"""
    Todo: Arrumar o encoding do texto ao abrir um arquivo
    """
    
	def __init__(self) -> None:
		super().__init__()
		
		self.initUI() # Chamando o construtor do UI
		
	def initUI(self):
		self.setWindowTitle("PyCode Studio")
		self.resize(QApplication.primaryScreen().size().width() - 20, QApplication.primaryScreen().size().height() - 75)
		self.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
		print(self.styleSheet())

		self.textEditorLayout = QVBoxLayout()

		#region TECLAS DE ATALHO
		self.newFileShortcut = QShortcut(QKeySequence("Ctrl+N"), self) # Tecla de atalho pra abrir um novo arquivo
		self.saveShortcut = QShortcut(QKeySequence("Ctrl+S"), self) # Tecla de atalho pra salvar o arquivo
		#endregion

		#region CONETCTANDO AS TECLAS DE ATALHO AOS COMANDOS
		self.newFileShortcut.activated.connect(self.newFile)
		self.saveShortcut.activated.connect(self.saveFile)
		#endregion

		# Criando o campo de texto
		self.textEditor = TextEditor()
		self.textEditorLayout.addWidget(self.textEditor)
   
		# Criando a barra de status
		self.myStatusBar = StatusBar(self.textEditor)
		self.setStatusBar(self.myStatusBar)
    
		# Criando a barra de menu
		self.myMenuBar = MenuBar(self, self.textEditor, self)
		self.setMenuBar(self.myMenuBar)

		textEditorContainer = QWidget()
		textEditorContainer.setLayout(self.textEditorLayout)

		self.setCentralWidget(textEditorContainer)

		self.show()
  
	def saveFile(self): # Função da tecla de atalho saveShorcut
		text_ = self.textEditor.toPlainText() # Pega o texto que esta no QTextEdit
  
		filePath = self.textEditor.filePath # Pega o arquivo atual que já estava aberto
		file = open(filePath, "w") # Abro o arquivo no modo "w" que significa que eu vou escrever nesse arquivo
		file.write(text_) # Escrevo no arquivo
		file.close() # Fecho o arquivo pra evitar problemas
  
	def newFile(self):
		fileDialog = QFileDialog()
		path, _ = fileDialog.getSaveFileName(None, "Create a new file", "NewFile", "All Files(*.txt)")

		self.textEditor.currentFilePath = path
		self.textEditor.clear()

#endregion
        
app = QApplication()

# app.setStyleSheet(qdarkstyle.load_stylesheet_pyside6())
app.setFont(QFont("Consolas", 16))

window = MainWindow()

app.exec()