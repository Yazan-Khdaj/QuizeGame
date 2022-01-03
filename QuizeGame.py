import sqlite3
import os
import random

class DataBase():
      "Class DataBase To Insert And Get Data"
      
      def __init__( self, path ):
          "Constractor"
          self.__path = path
          self.__connect = None
          self.__cursor = None
          self.__name = None
          self.__row_one = None
          self.__row_tow = None
          self.__row_three = None
         
           
      def open( self ):
          "make connect to DataBase"
          if(self.__connect is None):
              self.__connect = sqlite3.connect( self.__path )
              self.__cursor = self.__connect.cursor( )
         
           
      def close( self ):
          "Close connect to DataBase"
          if ( not ( self.__connect is None ) ):
              self.__cursor.close( )
              self.__connect.close( )
              self.__cursor = None
              self.__connect = None   
          
          
      def createTable( self, name, row_one, row_tow, row_three ):
          "Create DataBase with table and rows\n this method need name table\name row 1\nname row 2\nname row 3"
          self.__name = name
          self.__row_one = row_one
          self.__row_tow = row_tow
          self.__row_three = row_three
          if( not os.path.exists( self.__path ) ):
              self.open( )
              self.__cursor.execute( f"CREATE TABLE '{self.__name}' ( id INTEGER PRIMARY KEY AUTOINCREMENT, '{self.__row_one}' TEXT UNIQUE, '{self.__row_tow}' TEXT UNIQUE, '{self.__row_three}' TEXT )" )
              self.close( )
            
                        
      def insert( self, row_1,row_2,row_3 ):
          "Insert rows to BataBase\nthis method need three params"
          self.__cursor.execute( f"INSERT INTO '{self.__name}' ( '{self.__row_one}', '{self.__row_tow}', '{self.__row_three}' ) VALUES( '{row_1}', '{row_2}', '{row_3}' )" )
          self.__connect.commit( )      
         
          
      def get( self, id ):
          "Return rows as data Tuple"
          self.__cursor.execute( f"SELECT * FROM '{self.__name}' WHERE id={id}" )
          itemTupe = self.__cursor.fetchall( )
          return itemTupe[0]  
          
                      
      def info( self ):
          print( 'Path : ', self.__path )
          print( 'DataBase Connect : ', self.__connect )
          print( 'DataBase Cursor : ', self.__cursor )
          print( 'Table Name : ', self.__name )
          print( 'Row One Name : ', self.__row_one )
          print( 'Row Tow Name : ', self.__row_tow )
          print( 'Row Three Name : ', self.__row_three )
      
       
    
#======create files======#

def addCounter( path ):
    if not os.path.exists( path ):
        file = open( path, 'w' )
        file.write( '0' )
       
    file = open( path, 'r' )
    oldCounter = int( file.read( ) )
    newCounter = oldCounter + 1
    file = open( path, 'w' )
    file.write( str( newCounter ) )
    file.close( )
    
    
def getCounter( path ):
    if not os.path.exists( path ):
        file = open( path, 'w' )
        file.write( '0' )
        
    file = open( path, 'r' )
    counter = int( file.read( ) )
    file.close( )
    return counter
    
    
def getHighScore( path, score ):
    if not os.path.exists( path ):
        file = open( path, 'w' )
        file.write( '0' )   
        
    file = open( path, 'r' )
    highScore = int( file.read( ) )
    if score > highScore:
        file = open( path, 'w' )
        file.write( str( score ) )
        file.close( )
        return score
    else:
        return highScore
        
        
#======Random and Chack======#

def getRandom( ):
    counter = getCounter( FILE_COUNTER_PATH )
    randomNumber = random.randint( 1, counter )
    return randomNumber
  
  
def check( question_answer ):
    question = question_answer[0]
    answer = question_answer[1] 
    while True:
        userAnswer = input('Add Answer : ')
        userAnswer = userAnswer.lower( )
        if userAnswer == 'a':
            return answer == question[0]
        elif userAnswer == 'b':
            return answer == question[1]
        elif userAnswer == 'c':
            return answer == question[2]
        elif userAnswer == 'd':
            return answer == question[3]
        else:
            print( 'Enter a/b/c/d' )

    
#======get and add Qustions======#

def getQuestion( ):
    database.open()
    questionArray = database.get( getRandom( ) )
    database.close()
    question = questionArray[1]
    options = questionArray[2].split( '-' )
    answer = questionArray[3] 
    return [question, options, answer]   
    
    
def printQuestion( numberQuestion ):
    question_answer = getQuestion( )
    question = str( numberQuestion ) + "-" + question_answer[0] + '?'
    A_option = "A-" + question_answer[1][0]
    B_option = "B-" + question_answer[1][1]
    C_option = "C-" + question_answer[1][2]
    D_option = "D-" + question_answer[1][3]
    options = [A_option, B_option, C_option, D_option]
    answer = question_answer[2]
    print( question )
    print( *options )
    return [question_answer[1], answer]
       
     
def play( ):
    numberQuestion = 1
    score = 0
    while True:
       answer = printQuestion( numberQuestion )
       if check( answer ):
           numberQuestion += 1
           score += 1
       else:
           break
           
    highScour = getHighScore( FILE_SCORE_PATH, score )   
    print( 'High Score :', highScour )    
    print( 'Score :', score )


def addQuestion( ):
    question = input( 'Add Question : ' )
    options = ''
    
    for i in range( 4 ):
        options += input( f'Add option #{i+1} : ' ) + '-'
        
    answer = input( 'Add Answer : ' )
    
    database.open()
    database.insert( question, options, answer )
    database.close()
    
    addCounter( FILE_COUNTER_PATH )

      
def startScreen( ):
    print( '1-Add Question' )
    print( '2-Play' )
    print( '3-Exit' )
    chose = input( 'Chose : ' )
    return chose  
   
       
#======Satart Game======#

def startGame( ):
    chose = startScreen( )
    if chose == '1':
        addQuestion( )
        startGame( )
    elif chose == '2':
        play( )
        startGame( )
    elif chose == '3':
        print('exit')
        return
    else:
        print( 'Enter Correct Chose' )
        startGame( )
 
     
#======main======#

if __name__ == '__main__':
    
    FILE_COUNTER_PATH = 'Counter'
    FILE_SCORE_PATH = 'Score'
    DATABASE_PATH = 'Question.db'

    database = DataBase( DATABASE_PATH )
    database.createTable( 'Qustions', 'question', 'options', 'answer' )
    startGame( )
    