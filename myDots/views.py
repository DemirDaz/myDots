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
bonus = 0
# our home page view
def home(request):    
    return render(request, 'index.html')


"""
def validate_ajax(request):
    boxes = request.POST.get('proba', False)
    data = Convert(str(boxes))
    odgovor = ChoseEasy(data)
    return HttpResponse(odgovor, content_type='text/plain')
   
"""
@csrf_protect
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


                
#this one is nice
def heuristikaM(board, Maximizer, depth,lastmove):
    global pointscomp
    global pointshuman
    global initdepth
    
    heur = 0

    if Maximizer :
        
        heur += pointscomp*5  # wins 
       
                  
    else:
        
        heur += pointshuman*5 # wins 
    
    heur = heur - (initdepth - depth)      
    
    
    if board[lastmove] == 3: 
            heur -=initdepth #potencijalno gubi bodove ako napravi trojku

        

   
    if Maximizer:  # maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return -heur

def flip(c):
    if(c ==0):
        return 1
    if(c ==1):
        return 0

def heuristikaE(board, Maximizer, depth,lastmove):
    global pointscomp
    global pointshuman
    global initdepth
    
    heur = 0
    

    if Maximizer :
        
        heur += pointscomp*initdepth   # wins 
       
                  
    else:
        
        heur += pointshuman*initdepth   # wins 
    


    heur = heur - (initdepth - depth)      

    if Maximizer:  # maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(+heur) + " M:" + str(Maximizer))
        return +heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return -heur

    

    
   # heur = heur - initdepth*pointscomp*2 #tezina kretanja
   
def heuristikaH(board, Maximizer, depth, lastmove):
    global pointscomp
    global pointshuman
    global initdepth
    #unfilled = len(serverbox) - pointshuman - pointscomp
    heur = 0
   
    if Maximizer :
        
        heur += pointscomp*5  # wins
        heur -= pointshuman*5 
       
                  
    else:
        
        heur += pointshuman*5 # wins 
        heur -= pointscomp*5 
    
    heur = heur - (initdepth - depth)      
    
    
    if board[lastmove] == 3: 
            heur -=initdepth #potencijalno gubi bodove ako napravi trojku

    
    if Maximizer: #maksimajzer ce biti minus,jer se zapravo poziva iz min funkcije
        print("kutija: " + str(board) + " hrs: " + str(-heur) + " M:" + str(Maximizer))
        return heur
    else:
        print("kutija: " + str(board) + " hrs: " + str(heur) + " M:" + str(Maximizer))
        return -heur



def isWinner(board):
    winner = 1
    for i in range(len(board)):
        if board[i] != 4:
            winner = 0
            break
    return winner



def heuristicWinner(Maximizer,depth):
    if Maximizer:
        heuristic = (100-(initdepth-depth))
    else:
        heuristic = -(100-(initdepth-depth))
    print("pobednicka heuristika: " + str(heuristic) + " maks: " + str(Maximizer))
    return heuristic

#!!!! morace da se doda promenljiva koja ce da kaze da li igra bonus rudnu ili ne.

def miniMaxMedium(board, depth, Maximizer, alfa, beta):  # Function for the minimax algorithm a,b pruning
    global choicer
    global bestmove
    global initdepth
    global pointscomp
    global pointshuman
    global bonus
    z = len(serverbox)
    #flip je jer ako se pozove minimax iz maksimajzera, okrenuce maksimajzer na 0..da bi vrednosti bile pozitivne, flipovacemo sta je poslato
        #a bonus regulise da li se flip desava..jer ako igra maksimajzer on ce opet htet da maksimajzuje,tako da mu trebaju pozitivne heuristike,bez bonusa bi birao minimalni potez
    if bonus==1:
        if isWinner(board):
            return heuristicWinner((Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaM(board, (Maximizer), depth,choicer)
    elif bonus==0:
        if isWinner(board):
            return heuristicWinner(flip(Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaM(board, flip(Maximizer), depth,choicer)
    #posle evaluacije, vrati bonus na 0..pomerice se ponovo ako upadne u serverbox[i]==4
    if bonus==1:
        bonus=0
    
 
    

    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                    choicer = i
                    bonus = 1
                    result = miniMaxMedium(serverbox, depth - 1, 1, alfa, beta)
                    
                else:
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
                    choicer = j
                    bonus = 1
                    result = miniMaxMedium(serverbox, depth - 1, 0, alfa, beta)
                    
                else:
                    choicer = j
                    result = miniMaxMedium(serverbox, depth - 1, 1, alfa, beta)
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
    global bonus

    z = len(serverbox)

    if bonus==1:
        if isWinner(board):
            return heuristicWinner((Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaH(board, (Maximizer), depth,choicer)
    elif bonus==0:
        if isWinner(board):
            return heuristicWinner(flip(Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaH(board, flip(Maximizer), depth,choicer)
    #posle evaluacije, vrati bonus na 0..pomerice se ponovo ako upadne u serverbox[i]==4
    if bonus==1:
        bonus=0
   
    
    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                    choicer = i
                    result = minimaxHard(serverbox, depth - 1, 1, alfa, beta)
                    
                else:
                    choicer = i
                    result = minimaxHard(serverbox, depth - 1, 0, alfa, beta)
                    
              
                if result > maxEval:
                    maxEval = result
                    bestmove = choicer
                if serverbox[i]==4: #ako je uzeo poen makni ga
                    pointscomp -= 1
                serverbox[i] = serverbox[i] - 1 #svakako vrati korak unazad
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
                    choicer = j
                    result = minimaxHard(serverbox, depth - 1, 0, alfa, beta)
                    
                else:
                    choicer = j
                    result = minimaxHard(serverbox, depth - 1, 1, alfa, beta)
                    
                # move happened
                
                # remove the move
                minEval = min(result, minEval)
                beta = min(beta,minEval)
                if serverbox[j]==4:
                    pointshuman -= 1
                serverbox[j] = serverbox[j] - 1
                if beta <= alfa: #skrati ako se desi!
                    break
        return minEval



def miniMax(board, depth, Maximizer):  # Function for the minimax algorithm
    global choicer
    global bestmove
    global initdepth
    global pointscomp
    global pointshuman
    global bonus
    z = len(serverbox)

    if bonus==1:
        if isWinner(board):
            return heuristicWinner((Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaE(board,(Maximizer),depth,choicer)
    elif bonus==0:
        if isWinner(board):
            return heuristicWinner(flip(Maximizer),depth)
        
        if depth == 0 :  # zadnji red dubine or end of game
            return heuristikaE(board,flip(Maximizer),depth,choicer)
    #posle evaluacije, vrati bonus na 0..pomerice se ponovo ako upadne u serverbox[i]==4
    if bonus==1:
        bonus=0

    #return heuristikaEzy(board,Maximizer,depth)
        

    if Maximizer:
        maxEval = -1000
        for i in range(z):
            # simulacija novog koraka , ako je dozvoljen, uradi
            #SIMULACIJAAA
            if serverbox[i] < 4:
                serverbox[i] = serverbox[i] + 1  # move happened
                if serverbox[i]==4:
                    pointscomp += 1
                    choicer = i
                    result = miniMax(serverbox, depth - 1, 1)
                    
                else:
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
                    choicer = j
                    result = miniMax(serverbox, depth - 1, 0)
                    
                else:
                    choicer = j
                    result = miniMax(serverbox, depth - 1, 1)
                # remove the move
                minEval = min(result, minEval)
                #SKLONI POTEZ
                if serverbox[j]==4:
                    pointshuman -= 1
                serverbox[j] = serverbox[j] - 1
        return minEval


"""
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
"""
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
"""

"""

def ChoseEasy(data):
    temp = []
    for i in range(len(data)):
        if data[i]<3:
            temp.append(i)
        if data[i]==3:
            return i
    return random.choice(temp)     
""" 
"""
    for i in range(len(board)):
        if board[i] == 4:
            if Maximizer:
                heur += 
                
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
"""
"""
    if Maximizer:
        heur += pointshuman*3 -pointscomp*2 + unfilled*1  # ako vodi, nagrada ALI ako ne vodi kazna :)
    else:
        heur += pointscomp*3 - pointshuman*2 + unfilled*1  # ako vodi, nagrada ALI ako ne vodi kazna :)    heur = heur -(initdepth
"""