import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


Tour = 0

#mon jeu 
MyHand=[]

#mes cartes joué
MyGame = []

#liste des cartes qu'à l'adversaire en jeu
OpponentGame = []

# game loop
while True:

    player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    ennemy_health, ennemy_mana, ennemy_deck, ennemy_rune, ennemy_draw = [int(j) for j in input().split()]

    opponent_hand, opponent_actions = [int(i) for i in input().split()]

    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())

    #listes des coûts, attack et défense des monstres à sélectionner
    costs = []
    attacks = []
    defenses = []

    #locations
    locations = []

    # Dictionnaire pour centraliser les infos (à partir du Tour 30)
    dico = {}


    #enlever les cartes que j'ai joué de ma main
    for elt in MyGame :
        if elt in MyHand : 
            MyHand.remove(elt)


# récupérer les infos
    for i in range(card_count):
        inputs = input().split()
        #print("INFO " + str(inputs), file=sys.stderr, flush=True)
        
        if Tour < 30:
            card_number = int(inputs[0]) # Identifiant unique de la carte
            instance_id = int(inputs[1]) # ID unique pour cette instance de carte
            location = int(inputs[2]) # 0 = Draft, 1 = Ma main, -1 = Cartes de l’adversaire <== pas sur des infos
            locations.append(location)
            card_type = int(inputs[3]) # 0 = Créature, 1 = Vert, 2 = Rouge, 3 = Bleu
            cost = int(inputs[4]) # Coût en mana
            costs.append(cost)
            attack = int(inputs[5]) # Valeur d'attaque
            attacks.append(attack)
            defense = int(inputs[6]) # Valeur de défense
            defenses.append(defense)
            abilities = inputs[7] # Chaîne contenant les capacités (ex: "B" pour Breakthrough, "G" pour Guard, Charge)
            my_health_change = int(inputs[8]) # Modification de mes PV en jouant cette carte
            opponent_health_change = int(inputs[9]) # Modification des PV de l’adversaire
            card_draw = int(inputs[10]) # Nombre de cartes supplémentaires piochées


        if Tour >= 30:
            card_number = int(inputs[0]) # Identifiant unique de la carte
            instance_id = int(inputs[1]) # ID unique pour cette instance de carte
            location = int(inputs[2]) # 0 = Draft, 1 = Ma main, -1 = Cartes de l’adversaire <== pas sur des infos
            locations.append(location)
            card_type = int(inputs[3]) # 0 = Créature, 1 = Vert, 2 = Rouge, 3 = Bleu
            cost = int(inputs[4]) # Coût en mana
            costs.append(cost)
            attack = int(inputs[5]) # Valeur d'attaque
            attacks.append(attack)
            defense = int(inputs[6]) # Valeur de défense
            defenses.append(defense)
            abilities = inputs[7] # Chaîne contenant les capacités (ex: "B" pour Breakthrough, "G" pour Guard, Charge)
            my_health_change = int(inputs[8]) # Modification de mes PV en jouant cette carte
            opponent_health_change = int(inputs[9]) # Modification des PV de l’adversaire
            card_draw = int(inputs[10]) # Nombre de cartes supplémentaires piochées
            
            # Stocker toutes les infos dans un dictionnaire
            dico[instance_id] = {
                "card_number": int(inputs[0]),
                "location": location,
                "card_type": int(inputs[3]),
                "cost": int(inputs[4]),
                "attack": int(inputs[5]),
                "defense": int(inputs[6]),
                "abilities": inputs[7],
                "my_health_change": int(inputs[8]),
                "opponent_health_change": int(inputs[9]),
                "card_draw": int(inputs[10])
            }

            # Gérer les cartes en main et en jeu
            
            if location == 0:  # Ma main
                if instance_id not in MyHand:
                    MyHand.append(instance_id)

            elif location == 1:  # Mon jeu
                if instance_id not in MyGame:
                    MyGame.append(instance_id)

            elif location == -1:  # Jeu de l'adversaire
                if instance_id not in OpponentGame:
                    OpponentGame.append(instance_id)






    Tour +=1
    print("    #### Tour n°" + str(Tour) + " ####", file=sys.stderr, flush=True)
    print(f"Ma mana : {player_mana} | Ma vie : {player_health} \n", file=sys.stderr, flush=True)

    print("My hand : " + str(MyHand) , file=sys.stderr, flush=True)
    print("My Game : " + str(MyGame) , file=sys.stderr, flush=True)
    print("Opponent Game : " + str(OpponentGame) + "\n", file=sys.stderr, flush=True)



### DRAFT PHASE ###

    if Tour < 31:
        print("Prix Mana : " + str(costs), file=sys.stderr, flush=True)
        print("val_attaques :" + str(attacks), file=sys.stderr, flush=True)
        print("Carte choisi : " + str(costs.index(min(costs))), file=sys.stderr, flush=True)

        print(f"PICK {costs.index(min(costs))}")

### BATTLE PHASE ###

    if Tour >= 31:
        Action = "PASS"
        #choix des actions

         
        for elt in MyHand :
            if player_mana >= dico[elt]["cost"] :
                print("###### test" + str(dico[elt]["cost"]), file=sys.stderr, flush=True)
                MyGame.append(elt)
                Action = "SUMMON " + str(elt) + ";"
                print(Action)    

            else :
                print(Action)


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)


    
    