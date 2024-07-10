from PyQt5.QtWidgets import QGridLayout, QWidget,QPushButton,QLineEdit,QGraphicsDropShadowEffect
import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QKeyEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from utils  import isValidNumber, isnumordot,isempty

class UiMyWindow(object):
    

    def setup_ui(self, parent):
        # Inicialização de variáveis de controle
        self.operato=None
        self.left=None
        self.right=None
        self.result=None
        self.new_input = True
        # Configuração do widget central
        self.centralwidget = QWidget(parent)
        self.centralwidget.setObjectName("centralwidget")
        
        # Configuração do layout principal
        self.layout =  QGridLayout(self.centralwidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Adicionando o display
        self.display_= Display()
        self.layout.addWidget(self.display_, 0, 0, 1, 3)

        self.gridLayoutWidget = QWidget(self.centralwidget)
        # Configuração do layout dos botões
        self.layout_buttons = QGridLayout(self.gridLayoutWidget)
        self.layout_buttons.setSpacing(0)
        self.layout_buttons.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.gridLayoutWidget, 1, 0, 1, 3)

        self.configButton()
        self.configSignal()
        

        
        parent.setCentralWidget(self.centralwidget)
    # estilizando os botões
    def stylebutton(self,button):
        qss=f"""
            QPushButton{{
               
              font-size: 25px; background-color:#E0E0E0;
                
                border: 2px solid #404040 ; 
                padding: 10px
            }}
            QPushButton:hover{{
             font-size: 30px; background-color:#323232; 
                
                 border-width: 2px; border-color:#a0a0a0
            }}
             QPushButton:pressed {{
           font-size: 25px; background-color:#038C3E; 
                 
                 border-width: 6px; border-color:#02735E
         }}
           """
        qss2=f"""
            QPushButton{{
                font-size: 25px; background-color:#262626;
                
                border: 2px solid #C0C0C0 ; 
                padding: 10px
                 
                 }}
            QPushButton:hover{{
             font-size: 30px; background-color:#E0E0E0; 
                border-style: outset; 
                 border-width: 2px; border-color:#a0a0a0
            }}
             QPushButton:pressed {{
           font-size: 25px; background-color:#038C3E; 
                border-style: outset; 
                 border-width: 6px; border-color:#02735E
         }}
           """
        # colocando efeito sombra
        sombra= QGraphicsDropShadowEffect()
        sombra.setBlurRadius(7)
        sombra.setXOffset(7)
        sombra.setYOffset(7)
        sombra.setColor(QtGui.QColor(0,0,0,160))
        button.setGraphicsEffect(sombra)
        n=button.text()
        if isnumordot(n):
             button.setStyleSheet(qss)
        else:
             button.setStyleSheet(qss2)

 
    #tratamento de signal ao digitar no teclado
    def configSignal(self):
        self.display_.enterPressed.connect(self.equacao)
        self.display_.backpressed.connect(self._backSpace)
        self.display_.clearpressed.connect(self.clear)
        self.display_.oppressed.connect(self.op_)
        self.display_.inputpressed.connect(self.presedInsertDisplay)
        
        
    def configButton(self):
        # Configuração dos botões da calculadora
        #   
        self.cal=[
            
            ['C','%', '^', '/'],
            ['7','8', '9', '*'],
            ['4','5', '6', '-'],
            ['1','2', '3', '+'],
            ['N', '0', '.', '='],
        ]
        
        
        for i,row in enumerate (self.cal):
            for j,text in enumerate(row):

                
                button = QPushButton(text)
                button.setMinimumSize(60,50)
                button.setMaximumSize(60,50)
        
                self.stylebutton(button)
                
                self.layout_buttons.addWidget(button,i,j)
                slot=self.Clicked(self.presedInsertDisplay,text)
                self.connectButtonClicked(button,slot)
                
                
    
    def Clicked(self,fun,*args,**kwargs):
        def realslot():
            fun(*args,**kwargs)
        return realslot
    
    # Conectando os botoes ao clicar
    def connectButtonClicked(self,button,slot):
           button.clicked.connect(slot)

    
    def op_(self,text):
        # Tratamento de operadores
        if not isValidNumber(self.display_.text()) and self.left is None:
                print('Não há calculos para fazer')
                return
        
        self.operato=text
        self.left = self.display_.text()
        self.display_.clear()
        self.new_input = True
       
    
    def presedInsertDisplay(self,text):
        # Tratamento de entrada de texto
        if self.new_input:
            self.display_.clear()
            self.new_input = False
            
        if isnumordot(text):
            self.display_.insert(text)
        self.op= ['+', '-', '*', '/', '^','%']
        if text  in self.op and self.left is None:
            self.op_(text)
        if text  in self.op and  isValidNumber(self.display_.text()):
            self.equacao(text)
        if text =='=' :
            self.equacao(text)
        if 'N' in text:
            self.isNegative()
        if 'C' in text:
            self.clear()

    def _backSpace(self):
        # Tratamento de backspace
        self.display_.backspace()
        self.display_.setFocus()


    def isNegative(self):
        # Tratamento de números negativos
          displaytext= self.display_.text() 
          if not isValidNumber(displaytext):
            return
          number= float(displaytext)
          number1=-number
          self.display_.setText(str(number1))
          self.display_.setFocus()
         
    # Limpeza do display e variáveis     
    def clear(self):
         self.display_.clear()
         self.left=None
         self.right=None
         self.display_.setFocus()
             
    # Tratamento da equação
    def equacao(self,text):
        if not isValidNumber(self.display_.text()) and self.left is None:
                print('Não há calculos para fazer')
                return
     
           
        self.right=  self.display_.text()
        
        if self.operato == '+':
            self.result = float(self.left) + float(self.right)
        elif self.operato == '-':
            self.result = float(self.left) - float(self.right)
        elif self.operato == '*':
            self.result = float(self.left) * float(self.right)
        elif self.operato == '/':
            self.result = float(self.left) / float(self.right)
        elif self.operato == '%':
            self.result = (float(self.left) / float(100)) * float(self.right)
        elif self.operato == '^':
            self.result = float(self.left) ** float(self.right)
        
        self.left = self.result
        self.display_.setText(str(self.result))
        self.operato= text
        self.new_input = True
        self.display_.setFocus()
    
        
class Display(QLineEdit):
    enterPressed=pyqtSignal()
    backpressed=pyqtSignal()
    clearpressed=pyqtSignal()
    inputpressed= pyqtSignal(str)
    oppressed= pyqtSignal(str)



    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        self.confistyle()
        

    # Configuração do estilo do display
    def confistyle(self):
        
        MARGIN=5
        MEDIUM_SIZER=40
        MINIMUN_WIDTH=10
        margin=[MARGIN for m in  range(4)]
        self.setStyleSheet('font-size: 40px; background-color: #0e0e0e; color: white;border: 2px solid gray;')
        self.setMinimumHeight(MEDIUM_SIZER*2)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*margin)
        self.setMinimumWidth(MINIMUN_WIDTH)
    
    def keyPressEvent(self, event: QKeyEvent | None) -> None:
        key=event.key()
        text=event.text().strip()

        KEYS=Qt.Key
        isenter= key in [KEYS.Key_Enter, KEYS.Key_Return]
        isbackSpace=key in[KEYS.Key_Delete, KEYS.Key_Backspace]
        isesc=key in[KEYS.Key_Escape]
        isoperator= key in[KEYS.Key_Plus, KEYS.Key_Minus, KEYS.Key_Slash, KEYS.Key_Asterisk,KEYS.Key_P]
       
        
        if isenter:
            self.enterPressed.emit()
            return event.ignore()
        
        if isbackSpace:
            self.backpressed.emit()
            return event.ignore()
        
        if isesc:
            self.clearpressed.emit()
            return event.ignore()
        
        if isoperator:
            self.oppressed.emit(text)
            return event.ignore()
        
        if isempty(text):

            return event.ignore()
        
        if isnumordot(text):
        
            self.inputpressed.emit(text)
            return event.ignore()
     


        