import copy
def mk_posname(alph,i,j):
    if alph==1:
        return "A"+str(i)+";"+str(j)
    elif alph==2:
        return "B"+str(i)+";"+str(j)
    else:
        raise Exception("invalid position declaration")
class GameState():
    def __init__(self,n,komi=6.5,handicap=0,turn=1,move_num=0,captured=(0,0),ko_pos=None,passed=(False,False),state_d=dict()):
        self.n=n
        self.komi=komi
        self.handicap=handicap
        self.turn=turn
        self.move_num=move_num
        self.captured=captured
        self.ko_pos=ko_pos
        self.passed=passed
        self.state_d=state_d
class Game():
    def __init__(self,n,komi=6.5,handicap=0):
        self.n=n
        self.komi=komi
        self.handicap=0
        if handicap==0:
            self.turn=1 #1:black's turn, 2:white's turn
            self.move_num=0
        elif handicap>=2:
            self.turn=2
            self.move_num=handicap
        else:
            raise Exception("invalid handicap")
        self.captured=(0,0)
        self.ko_pos=None
        self.passed=(False,False)
        #position listing
        self.poss=[]
        for i in range(1,1+2*n):
            if i<=n+1:
                for j in range(1,n+i):
                    self.poss.append((1,i,j))
            else:
                for j in range(1+(i-n-1),1+2*n):
                    self.poss.append((1,i,j))
        for i in range(1,1+2*n):
            if i<=n:
                for j in range(1,1+n+i):
                    self.poss.append((2,i,j))
            else:
                for j in range(1+i-n,1+2*n):
                    self.poss.append((2,i,j))
        #state dictionary
        self.state_d=dict() #value 0: blank, 1: black, 2:white
        for pos in self.poss:
            self.state_d[pos]=0
        """
        handicap initial position!! 
        """
        #neighbor dictionary
        self.neighb_d=dict()
        for pos in self.poss:
            i,j,k=pos
            if i==1 and j==1:
                neighb=[(2,1,k),(2,1,k+1)]
            elif i==2 and k==1:
                neighb=[(1,j,1),(1,j+1,1)]
            elif i==1 and j-k==n:
                neighb=[(2,j-1,k),(2,j,k+1)]
            elif i==2 and j==2*n:
                neighb=[(1,2*n,k-1),(1,2*n,k)]
            elif i==1 and k==2*n:
                neighb=[(2,j-1,2*n),(2,j,2*n)]
            elif i==2 and j-k==-n:
                neighb=[(1,j,k-1),(1,j+1,k)]
            else:
                if i==1:
                    neighb=[(2,j,k),(2,j-1,k),(2,j,k+1)]
                elif i==2:
                    neighb=[(1,j,k),(1,j+1,k),(1,j,k-1)]
            self.neighb_d[pos]=neighb
        self.history=[self.copy_gamestate()]
    #gamestate handle
    def copy_gamestate(self):
        return GameState(n=self.n,komi=self.komi,handicap=self.handicap,turn=self.turn,
                         move_num=self.move_num,captured=self.captured,ko_pos=self.ko_pos,passed=self.passed,state_d=copy.copy(self.state_d))
    def load_gamestate(self,gs):
        self.n=gs.n
        self.komi=gs.komi
        self.handicap=gs.handicap
        self.turn=gs.turn
        self.move_num=gs.move_num
        self.captured=gs.captured
        self.ko_pos=gs.ko_pos
        self.passed=gs.passed
        self.state_d=copy.copy(gs.state_d)
    #position validity
    def filled(self, pos):
        return self.state_d[pos]!=0
    def blank(self,pos):
        return self.state_d[pos]==0
    def valid_pos(self,pos):
        return pos in self.poss
    def invalid_pos(self,pos):
        return not pos in self.poss
    def valid_move(self,pos):
        return self.valid_pos(pos) and self.blank(pos)
    def invalid_move(self,pos):
        return self.invalid_pos(pos) or self.filled(pos)
    #helpful algorithms
    def group(self,pos):
        if self.invalid_pos(pos):
            raise Exception("invalid position",pos)
        if self.blank(pos):
            return []
        color = self.state_d[pos]
        included = [pos]
        stack = [pos]
        while stack != []:
            cur = stack.pop()
            for neighb in self.neighb_d[cur]:
                if self.state_d[neighb] == color and not neighb in included:
                    included.append(neighb)
                    stack.append(neighb)
        return included
    def capturedif(self,pos,move): #whether the group of "pos" is captured if the move is performed. given (the move color)!=(the "pos" color)
        assert self.filled(pos) and self.valid_move(move) and self.state_d[pos]!=self.turn
        gp=self.group(pos)
        captured=True
        for elem in gp:
            for neighb in self.neighb_d[elem]:
                if self.blank(neighb) and neighb!=move:
                    captured=False
                    break
            if not captured:
                break
        return captured
    def captureif(self,move):
        captured=[]
        for neighb in self.neighb_d[move]:
            if self.state_d[neighb]==3-self.turn:
                if self.capturedif(neighb,move):
                    for elem in self.group(neighb):
                        if not elem in captured:
                            captured.append(elem)
        return captured
    def capturableif(self,move):
        for neighb in self.neighb_d[move]:
            if self.state_d[neighb]==3-self.turn:
                if self.capturedif(neighb,move):
                    return True
        return False

    def groupif(self,pos,move): # the group of "pos" when the move is performed. given (the move color)==(the "pos" color).
        color=self.turn
        assert self.valid_move(move) and self.state_d[pos]!=3-color
        included=[pos]
        stack=[pos]
        while stack!=[]:
            cur=stack.pop()
            for neighb in self.neighb_d[cur]:
                if (pos==neighb or self.state_d[neighb]==color) and not neighb in included:
                    included.append(neighb)
                    stack.append(neighb)
        return included
    def surroundedif(self,move): #whether the group of "move" is surrounded by the other color if the move is performed
        assert self.valid_move(move)
        gp=self.groupif(move,move)
        surrounded=True
        for elem in gp:
            for neighb in self.neighb_d[elem]:
                if self.blank(neighb) and neighb!=move:
                    surrounded=False
                    break
            if not surrounded:
                break
        return surrounded
    def koposif(self,move): #if the move doesn't make ko, return None, otherwise return the position invalidated by the ko.
        if len(self.captureif(move))==1 and len(self.groupif(move,move))==1 and self.surroundedif(move):
            return self.captureif(move)[0]
        return None
    def subtle_invalid_move(self,move):
        return self.invalid_move(move) or (self.surroundedif(move) and not self.capturableif(move)) or (move==self.ko_pos)
    def subtle_valid_move(self,move):
        return not self.subtle_invalid_move(move)
    #possible operations
    def mk_move(self,move): #used only when subtle_valid_move(move)
        #ko handling
        self.ko_pos=self.koposif(move)
        print("ko_pos:",self.ko_pos)
        #capturing
        captured=self.captureif(move)
        for elem in captured:
            self.state_d[elem]=0
        if self.turn==1:
            self.captured=(self.captured[0]+len(captured),self.captured[1])
        elif self.turn==2:
            self.captured=(self.captured[0],self.captured[1]+len(captured))
        #putting the stone
        self.state_d[move]=self.turn
        self.turn=3-self.turn
        self.move_num+=1
        #history update
        self.history.append(self.copy_gamestate())
    def passes(self):
        self.passed[self.turn-1]=True
        self.ko_pos=None
        self.turn=3-self.turn
        self.move_num+=1
        self.history.append(self.copy_gamestate())
    def undo(self,num):
        assert len(self.history)>num
        self.history=self.history[:-num]
        self.load_gamestate(self.history[-1])

