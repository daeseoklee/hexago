import pygame
pygame.font.init()
from hexago import *
from math import *

myfont=pygame.font.SysFont('Comic Sans MS',30)
HEIGHT=1.1
MENUHEIGHT=0.3
BOARDWIDTH=0.8
BLACKCOLOR=(0,0,0)
WHITECOLOR=(255,255,255)
BOARDCOLOR=(200,160,60)
LINECOLOR=(50,40,20)
def dist(loc1,loc2):
    return sqrt((loc1[0]-loc2[0])**2+(loc1[1]-loc2[1])**2)

    surface=myfont.render('abcde',False,(255,0,0))
    screen.blit(surface,(0,0))
def draw_menu(screen,width,game):
    pygame.draw.rect(screen,(200,200,255),(int(0.05*width),int((MENUHEIGHT-0.08)*width/2),int(0.2*width),int(0.08*width)),0)
    pygame.draw.rect(screen,(255,200,200),(int(0.3*width),int((MENUHEIGHT-0.08)*width/2),int(0.2*width),int(0.08*width)),0)
    pygame.draw.rect(screen,(150,150,150),(int(0.7*width),int((MENUHEIGHT-0.08)*width/2),int(0.2*width),int(0.08*width)),0)
    screen.blit(myfont.render(str(game.captured[0]),False,(0,0,0)),(int(0.07*width), int((MENUHEIGHT-0.08)*width/2)))
    screen.blit(myfont.render(str(game.captured[1]), False, (0, 0, 0)),(int(0.32 * width), int((MENUHEIGHT - 0.08) * width / 2)))
def draw_board(screen,width,game):
    n=game.n
    unit=width*BOARDWIDTH/((4*n-2)*sqrt(3))
    def unit2point(a,b):
        return (int(((1-BOARDWIDTH)/2)*width + unit*a),
                int(MENUHEIGHT*width + unit*b))
    def pos2point(pos):
        c,i,j=pos
        if c==1:
            return unit2point(n*sqrt(3)+2*sqrt(3)*j-sqrt(3)*i-sqrt(3),3*i-3)
        elif c==2:
            return unit2point(n*sqrt(3)+2*sqrt(3)*j-sqrt(3)*i-2*sqrt(3),3*i-2)
    def draw_stone(num,pos):
        if num==1:
            pygame.draw.circle(screen,BLACKCOLOR,pos2point(pos),int(1.0*unit),0)
        elif num==2:
            pygame.draw.circle(screen,WHITECOLOR,pos2point(pos),int(1.0*unit),0)
        else:
            pass
    for pos in game.poss:
        for neighb in game.neighb_d[pos]:
            pygame.draw.line(screen,LINECOLOR,pos2point(pos),pos2point(neighb))
    for pos in game.poss:
        draw_stone(game.state_d[pos],pos)


def main(width,n=9,komi=6.5,handicap=0):
    game=Game(n,komi=komi,handicap=handicap)
    n=game.n
    unit=width*BOARDWIDTH/((4*n-2)*sqrt(3))
    def unit2point(a,b):
        return (int(((1-BOARDWIDTH)/2)*width + unit*a),
                int(MENUHEIGHT*width + unit*b))
    def pos2point(pos):
        c,i,j=pos
        if c==1:
            return unit2point(n*sqrt(3)+2*sqrt(3)*j-sqrt(3)*i-sqrt(3),3*i-3)
        elif c==2:
            return unit2point(n*sqrt(3)+2*sqrt(3)*j-sqrt(3)*i-2*sqrt(3),3*i-2)
    screen=pygame.display.set_mode((width,int(HEIGHT*width)))
    screen.fill(BOARDCOLOR)
    running=1
    draw_menu(screen, width,game)
    draw_board(screen,width,game)
    while running:
        event=pygame.event.poll()
        if event.type==pygame.QUIT:
            running=0
        elif event.type==pygame.MOUSEBUTTONUP:
            loc,ty=event.pos,event.button
            if ty==1 and int(0.7*width)<=loc[0]<=int(0.2*width)+int(0.7*width)  and int((MENUHEIGHT-0.08)*width/2)<=loc[1]<=int(0.08*width)+int((MENUHEIGHT-0.08)*width/2):
                game.undo(1)
                screen.fill(BOARDCOLOR)
                draw_menu(screen, width, game)
                draw_board(screen, width, game)
            elif ty==1 and loc[1]>width*MENUHEIGHT:
                thepos=(1,1,1)
                mind=dist(pos2point((1,1,1)),loc)
                for pos in game.poss:
                    if dist(pos2point(pos),loc)<mind:
                        thepos=pos
                        mind=dist(pos2point(pos),loc)
                print(thepos)
                if mind<30 and game.subtle_valid_move(thepos):
                    game.mk_move(thepos)
                    screen.fill(BOARDCOLOR)
                    draw_menu(screen,width,game)
                    draw_board(screen,width,game)
        pygame.display.flip()
main(700,int(input("board size: ")))
