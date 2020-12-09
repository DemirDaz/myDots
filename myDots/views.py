from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import json
from django.views.decorators.csrf import csrf_protect
import random
import time


choicer = 5
bestmove = 6
initdepth = 0
pointshuman = 0
pointscomp = 0
# our home page view
def home(request):    
    return render(request, 'index.html')

@csrf_protect
def validate_ajax(request):
    boxes = request.POST.get('proba', False)
    data = Convert(str(boxes))
    odgovor = ChoseEasy(data)
    return HttpResponse(odgovor, content_type='text/plain')

def set_dubina(request):
    global initdepth
    global pointscomp
    global pointshuman
    initdepth = int(request.POST.get('d', False))
    pointshuman=0
    pointscomp=0
    return HttpResponse(200)

def set_comp(request):
    global pointscomp
    pointscomp = int(request.POST.get('comp', False))
    return HttpResponse(200)

def set_comp2(request):
    global pointscomp
    pointscomp = int(request.POST.get('comp2', False))
    return HttpResponse(200)

def set_comp3(request):
    global pointscomp
    pointscomp = int(request.POST.get('comp3', False))
    return HttpResponse(200)

def set_human(request):
    global pointshuman
    pointshuman = int(request.POST.get('you', False))
    return HttpResponse(200)
    
def validate_minimax(request):
    boxes = request.POST.get('proba', False)
    global serverbox 
    serverbox = Convert(str(boxes))
    global bestmove
    global initdepth
    score = miniMax(serverbox,initdepth,1)
    #
    # time.sleep(2)
    print("best value: " + str(score) + " best move: " + str(bestmove))
    return HttpResponse(bestmove, content_type='text/plain')

def validate_minimaxMedium(request):
    boxes = request.POST.get('proba', False)
    global serverbox 
    serverbox = Convert(str(boxes))
    global bestmove
    global initdepth
    score = miniMaxMedium(serverbox,initdepth,1,-1000,1000)
    #
    # time.sleep(2)
    print("best value: " + str(score) + " best move: " + str(bestmove))
    return HttpResponse(bestmove, content_type='text/plain')

def validate_minimaxHard(request):
    boxes = request.POST.get('proba', False)
    global serverbox 
    serverbox = Convert(str(boxes))
    global bestmove
    global initdepth
    score = minimaxHard(serverbox,initdepth,1,-1000,1000)
    #
    # time.sleep(2)
    print("best value: " + str(score) + " best move: " + str(bestmove))
    return HttpResponse(bestmove, content_type='text/plain')
    
    #return JsonResponse(boxes,safe=False)
def Convert(string): 
    li = list(string.split(",")) 
    for i in range(len(li)):
        li[i] = int(li[i])
    return li 


    

def ChoseEasy(data):
    temp = []
    for i in range(len(data)):
        if data[i]<3:
            temp.append(i)
        if data[i]==3:
            return i
    return random.choice(temp)      
                

def heuristikaEzy(board, Maximizer, depth):
    global pointscomp
    global pointshuman
    global initdepth
    heur = 0
    for i in range(len(board)):
        if board[i] == 4:
            if Maximizer:
                heur += (pointshuman-pointscomp)*initdepth  # ako vodi, nagrada ALI ako ne vodi kazna :)
            else:
                heur += (pointscomp-pointshuman)*initdepth   # ako vodi, nagrada ALI ako ne vodi kazna :)    heur = heur -(initdepth
   
    heur = heur -initdepth
    if Maximizer: #maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return -heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return heur


def heuristikaMed(board, Maximizer, depth):
    global pointscomp
    global pointshuman
    global initdepth
    heur = 0
    """
    if Maximizer:
        
        heur += pointshuman*(initdepth)   # wins + loses - ties
        heur -= (initdepth-1)*pointshuman
                  
    else:
        
        heur += pointscomp*(initdepth)   # wins + loses - ties
        heur -= (initdepth-1)*pointscomp
    """
    for i in range(len(board)):
        if board[i] == 4:
            if Maximizer:
                if pointshuman>pointscomp:
                    heur += (pointshuman-pointscomp)*1
                else:
                    heur += abs(pointshuman-pointscomp)*1
                      # ako vodi, nagrada ALI ako ne vodi kazna :)
            else:
                if pointscomp>pointshuman:
                    heur += (pointscomp-pointshuman)*1   # ako vodi, nagrada ALI ako ne vodi kazna :)    heur = heur -(initdepth
                else:
                    heur += abs(pointscomp-pointshuman)*1 
    
    heur = heur -initdepth      
    for i in range(len(board)):
        if board[i] == 3: 
            heur -=1 #potencijalno gubi bodove
    
   # heur = heur - initdepth*pointscomp*2 #tezina kretanja
    if Maximizer:  # maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return -heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return heur

def heuristikaH(board, Maximizer, depth, lastmove):
    global pointscomp
    global pointshuman
    global initdepth
    #unfilled = len(serverbox) - pointshuman - pointscomp
    heur = 0
    """
    if Maximizer:
        heur += pointshuman*3 -pointscomp*2 + unfilled*1  # ako vodi, nagrada ALI ako ne vodi kazna :)
    else:
        heur += pointscomp*3 - pointshuman*2 + unfilled*1  # ako vodi, nagrada ALI ako ne vodi kazna :)    heur = heur -(initdepth
    """
    for i in range(len(board)):
        if board[i] == 4:
            if Maximizer:
                if pointshuman>pointscomp:
                    heur += (pointshuman-pointscomp)*1
                else:
                    heur += abs(pointshuman-pointscomp)*1
                      # ako vodi, nagrada ALI ako ne vodi kazna :)
            else:
                if pointscomp>pointshuman:
                    heur += (pointscomp-pointshuman)*1   # ako vodi, nagrada ALI ako ne vodi kazna :)    heur = heur -(initdepth
                else:
                    heur += abs(pointscomp-pointshuman)*1 
    if board[lastmove] ==4:
        for i in range(len(board)):
            if board[i] ==3:
                heur +=2
    else:
        for i in range(len(board)):
            if board[i] ==3:
                heur -=2
    heur = heur -(initdepth-depth)
    if Maximizer: #maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return -heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return heur

def heuristikaHard(board, Maximizer, lastmove): #NOT DONE
    global pointscomp
    global pointshuman
    global initdepth
    heur = 0
    for i in range(len(board)):
        if board[i] == 4:
            if board[lastmove]==4:
                if pointscomp>=pointshuman:
                    heur += (pointscomp-pointshuman)*1 +2
                else:
                    heur += (pointscomp-pointshuman)*1 +2
            else: # ako nije uzeo poen
                if pointscomp>=pointshuman:
                    heur += (pointscomp-pointshuman)*1 +2
                else:
                    heur += (pointscomp-pointshuman)*1 
                
        if board[i] == 3:
            if board[lastmove]==4:  # ako vodi, verovatno je uzeo jednu od 4
                heur += 1  # nagrada za trojku koju ce da juri u sledecem koraku
            else:
                heur -= 1  # ako ne,onda je ostavio trojke protivniku
    if Maximizer: #maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return -heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return heur


def isWinner(board):
    winner = 1
    for i in range(len(board)):
        if board[i] != 4:
            winner = 0
            break
    return winner



def heuristicWinner(Maximizer,depth):
    if Maximizer:
        heuristic = -(100-(initdepth-depth))
    else:
        heuristic = +(100-(initdepth-depth))
    print("pobednicka heuristika: " + str(heuristic) + " maks: " + str(Maximizer))
    return heuristic


def miniMaxMedium(board, depth, Maximizer, alfa, beta):  # Function for the minimax algorithm a,b pruning
    global choicer
    global bestmove
    global initdepth
    global pointscomp
    global pointshuman
    z = len(serverbox)
    if isWinner(board):
        return heuristicWinner(Maximizer,depth)
        
    if depth == 0 :  # zadnji red dubine or end of game
        return heuristikaEzy(board, Maximizer, depth)
    
    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                choicer = i
                result = miniMaxMedium(serverbox, depth - 1, 0, alfa, beta)
                if result > maxEval:
                    maxEval = result
                    bestmove = choicer
                if serverbox[i]==4:
                    pointscomp -= 1
                serverbox[i] = serverbox[i] - 1
                alfa = max(alfa,maxEval)
                if beta <= alfa:
                    break
                # remove the move
                
                # maxEval = max(result, maxEval)
        return maxEval

    else:
        minEval = +1000
        for j in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[j] < 4:
                serverbox[j] = serverbox[j] + 1
                if serverbox[j]==4:
                    pointshuman += 1
                # move happened
                result = miniMaxMedium(serverbox, depth - 1, 1,alfa,beta)
                # remove the move
                minEval = min(result, minEval)
                beta = min(beta,minEval)
                if serverbox[j]==4:
                    pointshuman -= 1
                serverbox[j] = serverbox[j] - 1
                if beta <= alfa:
                    break
        return minEval

def minimaxHard(board, depth, Maximizer, alfa, beta):  # Function for the minimax algorithm a,b pruning
    global choicer
    global bestmove
    global initdepth
    global pointscomp
    global pointshuman
    z = len(serverbox)
    if isWinner(board):
        return heuristicWinner(Maximizer,depth)
        
    if depth == 0 :  # zadnji red dubine or end of game
        return heuristikaH(board, Maximizer, depth,choicer)
    
    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                choicer = i
                result = miniMaxMedium(serverbox, depth - 1, 0, alfa, beta)
                if result > maxEval:
                    maxEval = result
                    bestmove = choicer
                if serverbox[i]==4:
                    pointscomp -= 1
                serverbox[i] = serverbox[i] - 1
                alfa = max(alfa,maxEval)
                if beta <= alfa:
                    break
                # remove the move
                
                # maxEval = max(result, maxEval)
        return maxEval

    else:
        minEval = +1000
        for j in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[j] < 4:
                serverbox[j] = serverbox[j] + 1
                if serverbox[j]==4:
                    pointshuman += 1
                # move happened
                result = miniMaxMedium(serverbox, depth - 1, 1,alfa,beta)
                # remove the move
                minEval = min(result, minEval)
                beta = min(beta,minEval)
                if serverbox[j]==4:
                    pointshuman -= 1
                serverbox[j] = serverbox[j] - 1
                if beta <= alfa:
                    break
        return minEval


def miniMax(board, depth, Maximizer):  # Function for the minimax algorithm
    global choicer
    global bestmove
    global initdepth
    global pointscomp
    global pointshuman
    z = len(serverbox)
    if isWinner(board):
        return heuristicWinner(Maximizer,depth)
    if depth == 0 : #zadnji red dubine
        return heuristikaMed(board,Maximizer,depth) #return heuristikaEzy(board,Maximizer,depth)
        

    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                choicer = i
                result = miniMax(serverbox, depth - 1, 0)
                if result >= maxEval:
                    maxEval = result
                    bestmove = choicer
                # remove the move
                if serverbox[i]==4:
                    pointscomp -= 1
                serverbox[i] = serverbox[i] - 1
                # maxEval = max(result, maxEval)
        return maxEval

    else:
        minEval = +1000
        for j in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[j] < 4:
                serverbox[j] = serverbox[j] + 1
                if serverbox[j]==4:
                    pointshuman += 1
                # move happened
                result = miniMax(serverbox, depth - 1, 1)
                # remove the move
                minEval = min(result, minEval)
                if serverbox[j]==4:
                    pointshuman -= 1
                serverbox[j] = serverbox[j] - 1
        return minEval


""""
 for i in range(len(board)):
        if board[i] == 4:
            if board[lastmove]==4:
                if pointscomp>=pointshuman:
                    heur += (pointscomp-pointshuman)*1 +2
                else:
                    heur += (pointscomp-pointshuman)*1 +2
            else: # ako nije uzeo poen
                if pointscomp>=pointshuman:
                    heur += (pointscomp-pointshuman)*1 +2
                else:
                    heur += (pointscomp-pointshuman)*1 
                
        if board[i] == 3:
            if board[lastmove]==4:  # ako vodi, verovatno je uzeo jednu od 4
                heur += 1  # nagrada za trojku koju ce da juri u sledecem koraku
            else:
                heur -= 1  # ako ne,onda je ostavio trojke protivniku
                """