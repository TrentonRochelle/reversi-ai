import time

def getmsec():
  return int(round(time.time() * 1000))

def main():
  depth = 3
  
  board = [['*' for x in range(8)] for y in range(8)]
  board[3][3] = "X"
  board[3][4] = "O"
  board[4][3] = "O"
  board[4][4] = "X"
  ai = "h"
  print("Welcome to Reversi!")
  while(ai != "y"  and ai != "n"):
    ai = raw_input("Would you like for the AI to play against itself? Type y or n:").lower()
  if ai=="y":
    p1_name = "Computer1"
  else:
    p1_name = raw_input("P1 name:")
  
  #p2_name = raw_input("P2 name:")
  p2_name = "Computer2"
  p1_pieces = 2
  p2_pieces = 2
  response = raw_input(p1_name + ", start as X or O? X will have first move.\n").upper()
  while (response != "O" and response != "X"):
    response = raw_input(p1_name + ", start as X or O? X will have first move.\n").upper()
  p1 = [p1_name, response, p1_pieces]
  if(response == "X"):
    p2 = [p2_name, "O", p2_pieces]
    turn = p1[0] #turn will be the player's name
  else:
    p2 = [p2_name, "X", p2_pieces]
    turn = p2[0]
  print p1[0], ' is ', p1[1], ' and ', p2[0], ' is ', p2[1]
  
  X=[0,0]
  while X != [1,1]:
    print_board(board,p1,p2)



    
    if turn ==p1[0] and ai == "y":
      print 'It is ', p1[0], '\'s turn. Legal moves are ' ,legal_moves(board,p2)
      if legal_moves(board,p1) == []:
        turn = p2[0]
        X[1]=1
        break
      #response = move_input(board,p2)
      max_points = -99999
      for i in legal_moves(board,p1):
        i[0]-=1
        i[1]-=1
        #tempboard = [['*' for x in range(8)] for y in range(8)]
        #for x in range(8):
        #  for y in range(8):
        #    tempboard[x][y] = board[x][y]
        #move(tempboard,p1,i[0],i[1])
        #points = alpha_beta(tempboard,p1,p2,depth,1,min_val,max_val)
        points = alpha_beta(board,p1,p2,depth,1,min_val,max_val)

        if points>max_points:
          max_points = points
          best_x = i[0]
          best_y = i[1]
      response = [best_x,best_y]
      print response
      #response = legal_moves(board,p2)[0]
      #response = [response[0]-1,response[1]-1]
      X[1]=0
      move(board,p1,response[0],response[1])
      turn = p2[0]
    
    

    
    if turn == p1[0] and ai == "n": #player1s turn
      print 'It is ', p1[0], '\'s turn. Legal moves are ' ,graphical_moves(legal_moves(board,p1))
      if legal_moves(board,p1) == []:
        turn = p2[0]
        X[0]=1
        break
      response = move_input(board,p1)

      #response = legal_moves(board,p1)[0]
      #response = [response[0]-1,response[1]-1]
      
      X[0]=0
      move(board,p1,response[0],response[1])
      turn = p2[0]

  
      
  
    else: #player2s turn
      print 'It is ', p2[0], '\'s turn. Legal moves are ' ,graphical_moves(legal_moves(board,p2))
      start = getmsec()
      if legal_moves(board,p2) == []:
        turn = p1[0]
        X[1]=1
        break
      #response = move_input(board,p2)
      max_points = -99999
      for i in legal_moves(board,p2):
        i[0]-=1
        i[1]-=1
        #tempboard = [['*' for x in range(8)] for y in range(8)]
        #for x in range(8):
        #  for y in range(8):
        #    tempboard[x][y] = board[x][y]
        #move(tempboard,p2,i[0],i[1])
        #print("\n\t\t***RUNNING COMP MAXIMIZATION\n\n")
        #points = alpha_beta(tempboard,p2,p1,depth,1,min_val,max_val)
        points = alpha_beta(board,p2,p1,depth,1,min_val,max_val)

        if points>max_points:
          max_points = points
          best_x = i[0]
          best_y = i[1]
      response = [best_x,best_y]
      print("Time to respond: " + str(getmsec() - start))
      #response = legal_moves(board,p2)[0]
      #response = [response[0]-1,response[1]-1]
      X[1]=0
      move(board,p2,response[0],response[1])
      turn = p1[0]
      
  if p1[2]>p2[2]:
    print p1[0], 'won the game with', p1[2], 'pieces versus', p2[0]+ '\'s', str(p2[2]) + ' pieces.'
  if p2[2]>p1[2]:
    print p2[0], 'won the game with', p2[2], 'pieces versus', p1[0] + '\'s', str(p1[2]) + ' pieces.'
  if p1[2]==p2[2]:
    print 'It\'s a tie!'

def leaf_node_bool(board,player):
  if legal_moves(board,player) == []:
    return True
  else:
    return False


def cost_func(board,player): #reward corners and sides, discourage next to sides.
  value = 0
  for x in range(8):
    for y in range(8):
      if board[x][y] == player[1]:
        if (x==0 or x==7) and (y==0 or y==7): #corner
          value +=100
          continue
        if (x==0 or x==7) or (y==0 or y==7): #wall
          value +=33
          continue
        if ((x==0 or x==7) and (y==1 or y==6)) or ((x==1 or x==6) and (y==0 or y==7)):
          value -= 100
        if (x==1 or x==6) and (y==1 or y==6): #corner diagonal
          value -=30
          continue
        if (x==1 or x==6) and (y!=0 or y!=7): #next to wall
          value -=20
          continue
        if (y==1 or y==6) and (x!=0 or x!=7): #next to wall
          value -=20
          continue
        else:
          value+=1
  return value

min_val = -99999 #the smallest value possible. Found through cost_func
max_val = 99999 #biggest value possible
          
def minimax(board,player,depth,computer_move_bool):
  if leaf_node_bool(board,player) or depth==0:
    return cost_func(board,player)
  if computer_move_bool == True: #max/computer
    optimal_decision = min_val
    moves = legal_moves(board,player) #list of legal moves
    for m in moves:
      temp_board = board #copy of board
      move(temp_board,player,m[0],m[1]) #make move on copy
      temp = minimax(temp_board,player,depth-1,False) #recursive call and switch to Min
      optimal_decision = max(bestValue,temp)
  else: #min/hooman
    optimal_decision = max_val #set the limit
    moves = legal_moves(board,player) #list of legal moves
    for m in moves:
      temp_board = board #copy of board
      move(temp_board,player,m[0],m[1]) #make move on copy
      temp = minimax(temp_board,player,depth-1,True) #recursive call and switch to Max
      optimal_decision = min(bestValue,temp) #Find minimum
  return optimal_decision

def alpha_beta(board,player,opponent,depth,computer_move_bool,alpha,beta):
  #print("Current depth: " + str(depth))
  thingy = ""
  if (computer_move_bool == 1):
    thingy = "MAX"
  if (computer_move_bool == 0):
    thingy = "MIN"
  print("\n*****CURRENTLY " + thingy + "\n")
  print_board(board,player,opponent)
  
  
  if leaf_node_bool(board,player) or depth==0:
    print("\n\t\t NO MOVE \n")
    return cost_func(board,player)
  if computer_move_bool==1: #max/computer
    v = min_val
    moves = legal_moves(board,player) #list of legal moves
    print(moves)
    for m in moves:
      m[0]-=1
      m[1]-=1
      print("Max attempting move on " + str(m))
      temp_board = [['*' for x in range(8)] for y in range(8)]
      for x in range(8):
        for y in range(8):
          temp_board[x][y] = board[x][y]
      move(temp_board,player,m[0],m[1]) #make move on copy
      v = max(v, alpha_beta(temp_board,player,opponent,depth-1,0,alpha,beta)) #recursive call and switch to Min
      #if v>=beta:
      #  break
      #alpha = max(alpha,v)
      alpha = max(alpha,v)
      if beta<= alpha:
        break
    return v
  
  if computer_move_bool==0: #min/hooman
    v = max_val #set the limit
    moves = legal_moves(board,opponent) #list of legal moves
    for m in moves:
      m[0]-=1
      m[1]-=1
      print("Attempting move on " + str(m))
      temp_board = [['*' for x in range(8)] for y in range(8)]
      for x in range(8):
        for y in range(8):
          temp_board[x][y] = board[x][y]
      move(temp_board,opponent,m[0],m[1]) #make move on copy
      v = min(v, alpha_beta(temp_board,player,opponent,depth-1,1,alpha,beta)) #recursive call and switch to Max
      #if v<= alpha:
      #  break
      #beta = min(v,beta)
      beta = min(beta,v)
      if beta <= alpha:
        break
  return v


    
      
def move(board,player,x,y):
  tiles = tile_flip_array(board,player,x,y)
  if tiles == False:
    return False
  board[x][y] = player[1]
  for a,b in tiles:
    board[a][b]= player[1]
  return len(tiles)



def move_input(board, player):
  X = ['1' ,'2', '3', '4' ,'5', '6' ,'7' ,'8']
  Y = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  while True:
    response = raw_input('Type move as XY, where X and Y are 1-8: ')
    print response[0].lower()
    if len(response)==2 and response[1] in X and response[0].lower() in Y:
      x = int(response[1]) - 1
      y = ord(response[0].lower()) - ord('a')
      if tile_flip_array(board,player,x,y) == False:
        print 'This move is illegal'
        continue
      else:
        break
    else:
      print 'Not a valid input'
  return [x,y]

  
def print_board(board,player1,player2):
  print ""
  print "          X"
  row = "  \ A B C D E F G H"
  print (row)
  row_num = "0"
  score(board,player1,player2)
  for i, x in enumerate(board):
    row = chr(ord("1") + i)
    for y in board[i]:
      row = row + " " + y
    if i == 3:
      print ("Y " + row)
      continue
    print ("  " + row)
  print player1[0], ' has ', player1[2], ' pieces and ', player2[0], ' has ', player2[2], ' pieces.'

def score(board,player1,player2):
  player1[2] = 0
  player2[2] = 0
  for x in range(8):
    for y in range(8):
      if board[x][y] == player1[1]:
        player1[2] +=1
      if board[x][y] == player2[1]:
        player2[2] +=1
      else:
        continue

def board_limit_bool(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <=7

def tile_flip_array(board,player,x,y):
  #for an xy empty spot on a map, show what tiles would be flipped
  #return false if illegal move
  if board[x][y]!= '*' or not board_limit_bool:
    return False
  board[x][y] = player[1]
  tile_flip_array =[]
  if player[1] == "O":
    opponent = "X"
  else:
    opponent = "O"
  for direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]: #check surrounding pieces
    tempx = x + direction[0]
    tempy = y + direction[1]
    if board_limit_bool(tempx,tempy) and board[tempx][tempy]==opponent:
      tempx = tempx + direction[0]
      tempy = tempy + direction[1]
      if not board_limit_bool(tempx,tempy):
        continue
      while board[tempx][tempy]==opponent:
        tempx = tempx + direction[0]
        tempy = tempy + direction[1]
        if not board_limit_bool(tempx,tempy):
          break
      if not board_limit_bool(tempx,tempy): #if edge piece is opponent, check next direction
        continue
      if board[tempx][tempy] == player[1]:
        while True:
          tempx -= direction[0]
          tempy -= direction[1]
          if tempx == x and tempy == y:
            break
          tile_flip_array.append([tempx,tempy])   
  board[x][y] = '*'
  if len(tile_flip_array) == 0:
     return False
  return tile_flip_array

def legal_moves(board,player):
  moves =[]
  for x in range(8):
    for y in range(8):
      if tile_flip_array(board,player,x,y) != False:
        moves.append([x+1,y+1])
  return moves

def graphical_moves(moves):
  moves_column = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  retmoves = []
  for x in moves:
    retmoves.append(moves_column[x[1] - 1] + str(x[0]))
  return retmoves



main()
