import random
import math

def check_move(board, turn, col, pop):
    # implement your function here
    if col < 0 or col > 6:
        print('Error, exceed column index.') #column index is from 0 to 6 inclusive
        return False
    
    counter = 0
    if(pop == False):
        for i in range(0,int(len(board)/7)):
            if board[col+7*i] != 0: #check the column entry if fully filled
                counter += 1
            else:
                return True
                break
            
        if counter == int(len(board)/7): #this means the entire column is filled
            return False 
    counter = 0
    
    # check if pop is true and the column is empty
    if pop == True:
        # check if the column is empty (all 0s)
        colElements = []
        for i in range(col, len(board), 7): #generate_column_index(col):
            colElements.append(board[i])
        if(1 not in colElements and 2 not in colElements):
            print('Error, column is empty.')
            return False
        # check if the bottom piece belongs to the player
        if(board[col] != turn):
            print('Error, bottom piece does not belong to the player.')
            return False
        
        return True

def apply_move(board, turn, col, pop):
    # implement your function here
    if pop == False:
        for i in range(0,int(len(board)/7)):
            if board[col+(7*i)] == 0 :
                board1 = [x for x in board]
                board1[col+(7*i)] = turn
                break
            else:
                continue
    
        return board1
    else:
        # pop the bottom piece and move all pieces above it down
        # find the bottom most piece that belongs to the player
        bottomPiece = 0
        for i in range(col, len(board), 7):
            if(board[i] == turn):
                bottomPiece = i
                break
        # move all pieces above it down
        board1 = [x for x in board]
        for i in range(bottomPiece, len(board), 7):
            if(i + 7 < len(board)):
                board1[i] = board1[i + 7]
            else:
                board1[i] = 0
        return board1


def check_victory(board, who_played):
    # implement your function here
    # check if the player won
    # check if the player has 4 pieces in a row
    # check horizontal
    
    def check(who_played):
        # check horizontal
        for i in range(int(len(board)/7)):
            for j in range(4):
                if(board[i*7 + j] == who_played and board[i*7 + j + 1] == who_played and board[i*7 + j + 2] == who_played and board[i*7 + j + 3] == who_played):
                    return who_played
        # check vertical
        for i in range(int(len(board)/7)-3):
            for j in range(7):
                if(board[i*7 + j] == who_played and board[(i+1)*7 + j] == who_played and board[(i + 2)*7 + j] == who_played and board[(i+3)*7 + j] == who_played):
                    return who_played
        # check diagonal
        for i in range(int(len(board)/7)-3):
            for j in range(4):
                if(board[i*7 + j] == who_played and board[(i+1)*7 + j + 1] == who_played and board[(i+2)*7 + j + 2] == who_played and board[(i+3)*7 + j + 3] == who_played):
                    return who_played
        for i in range(int(len(board)/7)-3):
            for j in range(3,7):
                if(board[i*7 + j] == who_played and board[(i+1)*7 + j - 1] == who_played and board[(i+2)*7 + j - 2] == who_played and board[(i+3)*7 + j - 3] == who_played):
                    return who_played
    # player 1 pops and player 2 wins            
    if who_played == 1:
       if check(2) == 2:
           return 2
       elif check(1) == 1:
           return 1
       else:
           return 0
    # player 2 pops and player 1 wins   
    if who_played == 2:
       if check(1) == 1:
           return 1
       elif check(2) == 2:
           return 2
       else:
           return 0
            
            

def computer_move(board, turn, level):
    # implement your function here
    if level == 1:
        #choose a random column
        #random decision to pop
        pop = random.randint(0,1)
        # not popping
        if pop == 0:
            # check possible moves
            poss_move = []
            for i in range(0,7):
                for j in range(0, int(len(board)/7)):
                    if board[i+j*7] == 0:
                        poss_move.append(i)
                        break
            return (random.choice(poss_move), False)
        else:
            poss_move = []
            for i in range(0,7):
                # define computer as player 2
                if board[i] == 1:
                    poss_move.append(i)
            return (random.choice(poss_move), True)

    elif level == 2:
        # check possible moves
        poss_move = []
        for i in range(0,7):
            for j in range(0, int(len(board)/7)):
                if board[i+j*7] == 0:
                    poss_move.append(i)
                    break
        
        poss_move_pop = []
        for i in range(0,7):
            if board[i] == 1:
                poss_move_pop.append(i)
        
       

        for i in poss_move:
            new_board = apply_move(board, 1, i, False)
            # check for victory if not pop
            if check_victory(new_board, 1) == 1:
                return (i, False)
           
        # check for victory if pop
        
        for i in poss_move_pop:
            new_board = apply_move(board, 1, i, True)
            if check_victory(new_board, 1) == 1:
                return (i, True)
        
        # def block_player():
            
            for i in poss_move:
                # creates hypothetical board where computer places
                board_comp = apply_move(board, 2, i, False)
                
                # creates list of possible player moves (by placing) after computer plays
                poss_move_me = []
                for i in range(0,7):
                    for j in range(0, int(len(board)/7)):
                        if board[i+j*7] == 0:
                            poss_move_me.append(i)
                            break
                
                # creates list of possible player moves (by popping) after computer plays
                # poss_move_pop_me = []
                # for i in range(0,7):
                #     if board[i] == 1:
                #         poss_move_pop_me.append(i)
                
                for j in poss_move_me:
                    board_me = apply_move(board_comp, 1, j, False)
                    if check_victory(board_me, 1) == 1:
                        poss_move.remove(j)
            
                for j in poss_move:
                    board_me = apply_move(board_comp, 1, j, True)
                    if check_victory(board_me, 1) == 1:
                        poss_move.remove(j)
                
                board_comp_pop = apply_move(board, 2, i, True)

        
        
        
        
        
        
        
        

            
            
        
        
def display_board(board):
    # implement your function here
    for i in range(0,int(len(board)/7)):
        for i in range(0,7):
            print(board[i], ' ', end='')
        print()
    pass

def menu():
    # implement your function here
    # prompt user for the number of rows
    row = int(input('Enter the number of rows: '))
    # initialize the board
    board = [0] * row * 7
    # prompt user to check if they want to play against computer or player
    comp = input('Do you want to play against computer? (y/n): ')
    if(comp == 'y' or comp == 'Y'):
        comp = True
    # play against player
    elif (comp == 'n' or comp == 'N'):
        isPlayer1Turn = True
        # loop until someone wins
        while(True):
            turn = 1 if isPlayer1Turn else 2
            col = int(input('Player ' + str(turn) + ' enter column to play: '))
            # True if player wants to pop, False if player wants to place
            pop = input('Do you want to place or pop? (l/p): ')
            if(pop == 'l' or pop == 'l'):
                pop = False
            elif(pop == 'p' or pop == 'P'):
                pop = True
            else:
                print('Invalid input, please try again.')
                continue
            # check if move is valid
            if(check_move(board, turn, col, pop)):
                # apply move
                board = apply_move(board, turn, col, pop)
                # display board
                display_board(board)
                # check if player won
                if(check_victory(board, turn) == turn):
                    print('Player ' + str(turn) + ' wins!')
                    break
                elif(check_victory(board, 1) == 2):
                    print('Player 2 wins!')
                    break
                elif(check_victory(board,2) == 1):
                    print('Player 1 wins!')
                    break
                else:
                    # switch turns
                    isPlayer1Turn = not isPlayer1Turn
            else:
                print('Invalid move, please try again.')
                continue
    else:
        print('Error, invalid input.')
        return -1
    pass

    pass

if __name__ == "__main__":
    menu()




    
