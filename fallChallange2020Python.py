import sys

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


# game loop
turn=0
myPotNr=0
needed_tier3=0
needed_tier2=0
needed_tier1=0
needed_tier0=0
chosenRecipeId=0
while True:
    action_count = int(input())  # the number of spells and recipes in play
    recipeList=[]
    spellList=[]
    learnableList=[]
    neededSpellList=[]
    recipeNr=0
    turn+=1
    print("==========TURN: ",turn, file=sys.stderr, flush=True)
    print("==========MyPotNr: ",myPotNr, file=sys.stderr, flush=True)
    for i in range(action_count):
        # action_id: the unique ID of this spell or recipe
        # action_type: in the first league: BREW; later: CAST, OPPONENT_CAST, LEARN, BREW
        # delta_0: tier-0 ingredient change
        # delta_1: tier-1 ingredient change
        # delta_2: tier-2 ingredient change
        # delta_3: tier-3 ingredient change
        # price: the price in rupees if this is a potion
        # tome_index: in the first two leagues: always 0; later: the index in the tome if this is a tome spell, equal to the read-ahead tax
        # tax_count: in the first two leagues: always 0; later: the amount of taxed tier-0 ingredients you gain from learning this spell
        # castable: in the first league: always 0; later: 1 if this is a castable player spell
        # repeatable: for the first two leagues: always 0; later: 1 if this is a repeatable player spell
        action_id, action_type, delta_0, delta_1, delta_2, delta_3, price, tome_index, tax_count, castable, repeatable = input().split()
        action_id = int(action_id)
        delta_0 = int(delta_0)
        delta_1 = int(delta_1)
        delta_2 = int(delta_2)
        delta_3 = int(delta_3)
        price = int(price)
        tome_index = int(tome_index)
        tax_count = int(tax_count)
        castable = castable != "0"
        repeatable = repeatable != "0"
        if action_type=="LEARN":
            #if not (delta_0>1 and delta_1==0 and delta_2==0 and delta_3==0): #spell with lot of blue only
                learnableList.append((action_id,delta_0,delta_1,delta_2,delta_3,castable))
        elif action_type=="CAST":
            spellList.append((action_id,delta_0,delta_1,delta_2,delta_3,castable,repeatable,delta_0+delta_1+delta_2+delta_3))
        elif action_type=="BREW":
            recipeList.append([action_id,delta_0,delta_1,delta_2,delta_3,price])
            recipeNr+=1

    invList=[]
    for i in range(2):
        # inv_0: tier-0 ingredients in inventory
        # score: amount of rupees
        inv_0, inv_1, inv_2, inv_3, score = [int(j) for j in input().split()]
        if i==0: #me
            invList=[inv_0,inv_1,inv_2,inv_3]
    #check special spells
    #action_id,delta_0,delta_1,delta_2,delta_3,castable,repeatable,delta_0+delta_1+delta_2+delta_3
    yellowValue=4
    orangeValue=3
    greenValue=2
    blueValue=1
    for spell in spellList:
        if spell[4]>=1 and spell[3]>=0 and spell[2]>=0 and spell[1]>=0 and spell[5]==True: # yellow creator spell
            #print("YELLOWSPELL",file=sys.stderr, flush=True)
            if 1/spell[4]<yellowValue:
                yellowValue=1/spell[4]
                print("yellowY: ",yellowValue,file=sys.stderr, flush=True)

        if spell[4]>=0 and spell[3]>=1 and spell[2]>=0 and spell[1]>=0 and spell[5]==True: # orange creator spell
            #print("ORANGESPELL",file=sys.stderr, flush=True)
            if 1/spell[3]<orangeValue:
                orangeValue=1/spell[3]
                print("orangeO: ",orangeValue,file=sys.stderr, flush=True)
            if yellowValue>=1:
                yellowValue=orangeValue+1
                print("yellowO: ",yellowValue,file=sys.stderr, flush=True)

        if spell[4]>=0 and spell[3]>=0 and spell[2]>=1 and spell[1]>=0 and spell[5]==True: # green creator spell
            #print("GREENSPELL",file=sys.stderr, flush=True)
            if 1/spell[2]<greenValue:
                greenValue=1/spell[2]
                print("greenG: ",greenValue,file=sys.stderr, flush=True)
            if orangeValue==3:
                orangeValue=greenValue+1
                print("orangeG: ",orangeValue,file=sys.stderr, flush=True)
            if yellowValue==4:
                yellowValue=greenValue+2
                print("yellowG: ",yellowValue,file=sys.stderr, flush=True)

        if spell[4]>=0 and spell[3]>=0 and spell[2]>=0 and spell[1]>=2 and spell[5]==True: # blue creator spell
            #print("BLUESPELL",file=sys.stderr, flush=True)
            if 1/spell[1]<blueValue:
                blueValue=1/spell[1]

    print("=====ColorValues: ",file=sys.stderr, flush=True)
    print("yellow: ",yellowValue,file=sys.stderr, flush=True)
    print("orange: ",orangeValue,file=sys.stderr, flush=True)
    print("green: ",greenValue,file=sys.stderr, flush=True)
    print("blue: ",blueValue,file=sys.stderr, flush=True)
    #count steps for recipes
    for recipe in recipeList:
        yellowStep=(abs(recipe[4])-invList[3])*yellowValue
        if yellowStep<0:
            yellowStep=0
    
        orangeStep=(abs(recipe[3])-invList[2])*orangeValue
        if orangeStep<0:
            orangeStep=0
    
        greenStep=(abs(recipe[2])-invList[1])*greenValue
        if greenStep<0:
            greenStep=0  

        blueStep=(abs(recipe[1])-invList[0])*blueValue
        if blueStep<0:
            blueStep=0        
      
        print("=====Recipe: ",recipe[0],file=sys.stderr, flush=True)
        print("Recipe, step, yellow: ",yellowStep,file=sys.stderr, flush=True)
        print("Recipe, step, orange: ",orangeStep,file=sys.stderr, flush=True)
        print("Recipe, step, green: ",greenStep,file=sys.stderr, flush=True)
        print("Recipe, step, blue: ",blueStep,file=sys.stderr, flush=True)
        step=yellowStep+orangeStep+greenStep+blueStep #how many steps needed to brew something
        if step==0:
            step=0.01
        recipe.append(step)
        print("Recipe, step: ",step,file=sys.stderr, flush=True)

    #recipes sorted from big score/step to low 
    recipeList=sorted(recipeList, key=lambda recipe: recipe[5]*(1/recipe[6]), reverse=True)
    chosenRecipeId=recipeList[0][0]
    needed_tier3=abs(recipeList[0][4])
    needed_tier2=abs(recipeList[0][3])
    needed_tier1=abs(recipeList[0][2])
    needed_tier0=abs(recipeList[0][1])

    print("REC order:", file=sys.stderr, flush=True)
    for recipe in recipeList:
        print("ID, price, step, value",recipe[0],recipe[5],recipe[6],recipe[5]*(1/recipe[6]), file=sys.stderr, flush=True)
    
    id=-1
    actionType=""

    #if there is a worthy learnable spell
    if len(spellList):
        blue=-1
        for spell in learnableList:
            blue+=1
            if spell[1]>=0 and spell[2]>=0 and spell[3]>=0 and spell[4]>=0: #only positive casting spells
                neededSpellList.append((spell[0],blue))
            #elif spell[1]==-2 and spell[2]==0 and spell[3]==1 and spell[4]==0: # -2 blue +1 orange
            #    neededSpellList.append((spell[0],blue))
            #elif spell[1]<0 and spell[2]>1 and spell[3]==0 and spell[4]==0: #from blue to green
            #    neededSpellList.append((spell[0],blue))
            #elif spell[1]<0 and spell[2]==0 and spell[3]>=1 and spell[4]==0: #from blue to orange
            #    neededSpellList.append((spell[0],blue))
            #elif spell[1]<0 and spell[2]==0 and spell[3]==0 and spell[4]>=1: #from blue to yellow
            #    neededSpellList.append((spell[0],blue))
    else:
        #we have enough spell
        neededSpellList.clear()

    collectingBlue=False

    restNeeded4Blue=True
    for spell in spellList:
        if spell[1]==4 and spell[5]==True: #4blue
            restNeeded4Blue=False

    restNeeded3Blue=True
    for spell in spellList:
        if spell[1]==3 and spell[5]==True: #3blue
            restNeeded2Blue=False

    restNeeded2Blue=True
    if spellList[0][5]==True: #2blue
        restNeeded2Blue=False


    if len(neededSpellList)>0:
        if invList[0]>=neededSpellList[0][1]:
            #print("HEUREKA: inv, nr: ",invList[0], neededSpellList[0][1], file=sys.stderr, flush=True)
            id=neededSpellList[0][0]
            actionType="LEARN"
        elif restNeeded4Blue and restNeeded3Blue and restNeeded2Blue:
            #blue collection need to rest
            actionType="REST"
            id=""
        else:
            collectingBlue=True 

    #chose the best available recipe
    print("*************CB***********",collectingBlue ,file=sys.stderr, flush=True)
    print("*************AT***********",actionType ,file=sys.stderr, flush=True)
    if collectingBlue==False and actionType!="LEARN":
        if invList[0]>=needed_tier0 and invList[1]>=needed_tier1 and invList[2]>=needed_tier2 and invList[3]>=needed_tier3:
            print("*************Lets brew***********", file=sys.stderr, flush=True)
            id=chosenRecipeId  
            actionType="BREW"

    #chosen recipe
    print("Id: ",id, file=sys.stderr, flush=True)
    print("Chosen recipe: ",recipeList[0][0], file=sys.stderr, flush=True)
    print("Needed tier0: ",needed_tier0, file=sys.stderr, flush=True)
    print("Needed tier1: ",needed_tier1, file=sys.stderr, flush=True)
    print("Needed tier2: ",needed_tier2, file=sys.stderr, flush=True)
    print("Needed tier3: ",needed_tier3, file=sys.stderr, flush=True)

    #invertory
    print("====", file=sys.stderr, flush=True)
    print("Invertory: ", file=sys.stderr, flush=True)
    print("tier0: ",invList[0], file=sys.stderr, flush=True)
    print("tier1: ",invList[1], file=sys.stderr, flush=True)
    print("tier2: ",invList[2], file=sys.stderr, flush=True)
    print("tier3: ",invList[3], file=sys.stderr, flush=True)

    print("Spells: ", file=sys.stderr, flush=True)
    for i in range(len(spellList)):
        print(spellList[i], file=sys.stderr, flush=True)

    print("******INV: ",sum(invList), file=sys.stderr, flush=True) 
    if actionType=="LEARN":
        print("We are learning: ",id, file=sys.stderr, flush=True) 
    elif actionType=="REST":
        id=""
    elif collectingBlue==True: #collectingBlue
        print("CB:", file=sys.stderr, flush=True)
        actionType="CAST"
        id=-1
        for spell in spellList:
            if spell[1]==4 and spell[5]==True and sum(invList)+4<=10: #4blue
                id=spell[0]

        if id==-1: #3blue
            for spell in spellList:
                if spell[1]==3 and spell[5]==True and sum(invList)+3<=10:
                    id=spell[0]
        if id==-1 and sum(invList)+2<=10: #default blue creator
            id=spellList[0][0]
        
        if id==-1:
            actionType="REST"
            id=""
    elif actionType=="BREW":
        print("BR", file=sys.stderr, flush=True)
        needed_tier3=0
        needed_tier2=0
        needed_tier1=0
        needed_tier0=0
        myPotNr+=1
    #no brew id, then we have to spell
    elif id==-1:
        print("CASTOOO", file=sys.stderr, flush=True)
        actionType="CAST"
        i=0
        while id==-1 and i<len(spellList): #lets try tier3, with learned spell
            #calculating impact, not to overload the invertory
            blueImpact=invList[0]+spellList[i][1]
            if blueImpact<0:
                blueImpact=0

            greenImpact=invList[1]+spellList[i][2]
            if greenImpact<0:
                greenImpact=0

            orangeImpact=invList[2]+spellList[i][3]
            if orangeImpact<0:
                orangeImpact=0


            yellowImpact=invList[3]+spellList[i][4]
            if yellowImpact<0:
                yellowImpact=0

            if blueImpact+greenImpact+orangeImpact+yellowImpact<=10:
                notOverload=True
            else:
                notOverload=False

            if needed_tier3>invList[3] and spellList[i][4]>=1 and spellList[i][3]>=0 and spellList[i][2]>=0 and spellList[i][1]>=0 and spellList[i][5]==True and notOverload: #cast tier3 if needed and possible
                id=spellList[i][0]
                print("TIER3L", file=sys.stderr, flush=True)
            else:
                i+=1

        if id==-1: #lets try tier3, with default spell
            i=0
            while id==-1 and i<len(spellList): 
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False

                if needed_tier3>invList[3] and spellList[i][4]==1 and spellList[i][3]==-1 and spellList[i][2]==0 and spellList[i][1]==0 and invList[2]>0 and spellList[i][5]==True and notOverload: #cast tier3 if needed and possible
                    id=spellList[i][0]
                    print("TIER3D", file=sys.stderr, flush=True)
                else:
                    i+=1

        if id==-1: #no tier3 spell possible, lets try tier2, with learned spell
            i=0
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False
                
                if needed_tier2>invList[2] and spellList[i][4]>=0 and spellList[i][3]>=1 and spellList[i][2]>=0 and spellList[i][1]>=0 and spellList[i][5]==True and notOverload: #cast tier2 if needed and possible
                    id=spellList[i][0]
                    print("TIER2L", file=sys.stderr, flush=True)
                else:
                    i+=1  

        if id==-1: #no tier3 spell possible, lets try tier2, with default spell
            i=0
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False
                if (needed_tier2>invList[2] or needed_tier3>invList[3]) and spellList[i][3]==1 and spellList[i][1]==0 and spellList[i][2]==-1 and spellList[i][4]==0 and invList[1]>0 and spellList[i][5]==True and notOverload: #cast tier2 if needed and possible
                    id=spellList[i][0]
                    print("TIER2D", file=sys.stderr, flush=True)
                else:
                    i+=1          

        if id==-1: #no tier2 spell possible, lets try tier1, with learned spell
            i=0
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False

                if needed_tier1>invList[1] and spellList[i][4]>=0 and spellList[i][3]>=0 and spellList[i][2]>=1 and spellList[i][1]>=0 and spellList[i][5]==True and notOverload: #cast tier1 if needed and possible
                    id=spellList[i][0]
                    print("TIER1L", file=sys.stderr, flush=True)
                else:
                    i+=1


        if id==-1: #no tier2 spell possible, lets try tier1, with default spell
            i=0 
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False
               
                if (needed_tier1>invList[1] or needed_tier3>invList[3] or needed_tier2>invList[2]) and spellList[i][2]==1 and spellList[i][3]==0 and spellList[i][4]==0 and spellList[i][1]==-1 and invList[0]>0 and spellList[i][5]==True and notOverload: #cast tier1 if needed and possible
                    id=spellList[i][0]
                    print("TIER1D", file=sys.stderr, flush=True)
                else:
                    i+=1  

        if id==-1: #no tier1 spell possible, lets try tier0, with learned spell 4blue
            i=0
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False
               
                if (needed_tier0>invList[0] or invList[0]==0) and spellList[i][4]>=0 and spellList[i][3]>=0 and spellList[i][2]>=0 and spellList[i][1]==4 and spellList[i][5]==True and notOverload: #cast tier0 if needed and possible
                    id=spellList[i][0]   
                    print("TIER0L4", file=sys.stderr, flush=True)            
                else:
                    i+=1   

        if id==-1: #no tier1 spell possible, lets try tier0, with learned spell 3blue
            i=0
            while id==-1 and i<len(spellList):
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False
                
                if (needed_tier0>invList[0] or invList[0]==0) and spellList[i][4]>=0 and spellList[i][3]>=0 and spellList[i][2]>=0 and spellList[i][1]==3 and spellList[i][5]==True and notOverload: #cast tier0 if needed and possible
                    id=spellList[i][0]   
                    print("TIER0L3", file=sys.stderr, flush=True)            
                else:
                    i+=1   

        if id==-1: #no tier1 spell possible, lets try tier0, with default spell
            i=0
            while id==-1 and i<len(spellList):  
                #calculating impact, not to overload the invertory
                blueImpact = invList[0]+spellList[i][1]
                if blueImpact < 0:
                    blueImpact = 0

                greenImpact = invList[1]+spellList[i][2]
                if greenImpact < 0:
                    greenImpact = 0

                orangeImpact = invList[2]+spellList[i][3]
                if orangeImpact < 0:
                    orangeImpact = 0

                yellowImpact = invList[3]+spellList[i][4]
                if yellowImpact < 0:
                    yellowImpact = 0

                if blueImpact+greenImpact+orangeImpact+yellowImpact <= 10:
                    notOverload = True
                else:
                    notOverload = False           
                
                if (needed_tier0>invList[0] or invList[0]==0) and spellList[i][1]==2 and spellList[i][5]==True and notOverload: #cast tier0 if needed and possible
                    id=spellList[i][0]
                    print("TIER0D", file=sys.stderr, flush=True)
                else:
                    i+=1   

        if id==-1: #no cast spells, maybe its exhausted
            actionType="REST"
            id=""



    #print(actionType,id, file=sys.stderr, flush=True)
    # in the first league: BREW <id> | WAIT; later: BREW <id> | CAST <id> [<times>] | LEARN <id> | REST | WAIT
    if id==0: #just to be sure
        id=""
    print(actionType,id)
