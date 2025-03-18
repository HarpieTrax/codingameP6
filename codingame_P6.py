import sys
import math

#===================================================
#FONCTIONS UTILISES PENDANT LE JEU
#===================================================

# Fct utilent par la suite pour code plus optimale
def Abilities_detection(x):      #fct qui permet de savoir si y a des cartes des abilities d'un jeu de crate passé en paramètre et les renvoi pour les ciblers (sauf charge qui sert plus à rien)
    tab=[]
    for elt in x :
        print(f"### OUI ### {dico[elt]['abilitie']}", file=sys.stderr, flush=True) 
        if "G" in dico[elt]["abilitie"]:      #détection en priorité de Guard 
            tab.append(elt)
    for elt2 in x :  
        if "B" in dico[elt2]["abilitie"]:     #détection ensuite de Breakthrough
            tab.append(elt2) 
    #print(f"### TESTTTTTTT ### {tab}", file=sys.stderr, flush=True)
    return tab

#===================================================
#VARIALBES À DÉCLARER EN DEHORS DU WHILE
#===================================================

Tour = 0
tab_types=[0,0,0,0]
pourcentage=0


# Game loop
while True:
    player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    ennemy_health, ennemy_mana, ennemy_deck, ennemy_rune, ennemy_draw = [int(j) for j in input().split()]

    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    
    for i in range(opponent_actions):
        input()  # On consomme bien toutes les lignes d'action de l'adversaire
    
    card_count = int(input())

    # Listes des coûts, attaques et défenses des monstres à sélectionner
    costs = [] #coûts en mana des monstres
    attacks = [] #attaques des monstres
    defenses = [] #PV / def des monstres
    locations = [] #Monstres en main ou sur le board (allié ou adverse)
    abilities=[] #capacités des monstres / objets
    tab_my_health_change=[] #modifications de nos PVs
    tab_opponent_health_change=[] #modifications des PVs de l'adversaire
    tab_card_draw=[] #nombre de cartes tirés
    cards_type = [] #type de la carte 0 : créature | 1 obj vert | 2 obj rouge | 3 obj bleu 

    dico = {}

    # Mon jeu  (ma main)
    MyHand = []

    # Mes cartes sur le Board
    MyGame = []

    # Liste des cartes que l'adversaire a en jeu
    OpponentGame = []

    # Enlever les cartes jouées de ma main
    MyHand = [elt for elt in MyHand if elt not in MyGame]

    # Récupérer les infos des cartes
    #TOUTE LA BOUCLE FOR PEUT ÊTRE MISE DANS UNE FONCTION
    for i in range(card_count): 
        inputs = input().split() 
        card_number = int(inputs[0]) #identifiant unique
        instance_id = int(inputs[1]) #identifiant d'instance
        location = int(inputs[2]) #localisation : 0 = main, 1 = board allié, -1 = board ennemi
        card_type = int(inputs[3]) #type de carte, bleu, vert, rouge, neutre
        cost = int(inputs[4]) #coût en mana de la carte
        attack = int(inputs[5]) #attaque de la carte
        defense = int(inputs[6]) #défense de la carte
        abilitie = inputs[7] #capacité de la carte
        my_health_change = int(inputs[8]) #modification nos pvs par la carte
        opponent_health_change = int(inputs[9]) #modif pv adverse par la carte
        card_draw = int(inputs[10]) #modif tirage carte par la carte
        
        #des tab pour recup les infos des 3 cartes et faire le meilleur choix pour draft
        locations.append(location)
        costs.append(cost)
        attacks.append(attack)
        defenses.append(defense)
        abilities.append(abilitie)
        tab_my_health_change.append(my_health_change)
        tab_opponent_health_change.append(opponent_health_change)
        tab_card_draw.append(card_draw)
        cards_type.append(card_type)

        #recup les info sous forme de dico pour phase de combat 
        if Tour >= 30:
            dico[instance_id] = {
                "card_number": card_number,
                "location": location,
                "card_type": card_type,
                "cost": cost,
                "attack": attack,
                "defense": defense,
                "abilitie": abilitie,
                "my_health_change": my_health_change,
                "opponent_health_change": opponent_health_change,
                "card_draw": card_draw
            }
            #print("### nb" + str(instance_id) + " ; " + str(dico[instance_id]['defense']), file=sys.stderr, flush=True)
            #Création des listes des cartes de ma main et du Board
            if location == 0 and instance_id not in MyHand:
                MyHand.append(instance_id)
            elif location == 1 and instance_id not in MyGame:
                MyGame.append(instance_id)
            elif location == -1 and instance_id not in OpponentGame:
                OpponentGame.append(instance_id)
    
    print(f"dico : {dico}", file = sys.stderr, flush = True)


#===================================================
#AFFICHAGE INFO DE BASE
#===================================================

    Tour += 1 #CHANGER LA PLACE DU TOUR+=1 (CALCUL SUR LES TOURS AVANT ET APRÈS PAS LOGIQUE)
    print(f"#### Tour n°{Tour} ####", file=sys.stderr, flush=True)
    print(f"Ma mana : {player_mana} | Ma vie : {player_health}\n", file=sys.stderr, flush=True)
    print(f"My Hand : {MyHand}", file=sys.stderr, flush=True)
    print(f"My Game : {MyGame}", file=sys.stderr, flush=True)
    print(f"Opponent Game : {OpponentGame}\n", file=sys.stderr, flush=True)


#===================================================
#DRAFT PHASE
#===================================================

    if Tour < 31:
        print(f"Prix Mana : {costs}", file=sys.stderr, flush=True)
        print(f"val_attaques : {attacks}", file=sys.stderr, flush=True)
        print(f"Les abilitie : {abilities}", file=sys.stderr, flush=True)
        #print(f"Les dégats en plus affligé à l'adversaire : {tab_opponent_health_change}", file=sys.stderr, flush=True)

        # choisir 80% créature et 30% objet (à opti pour trouver un bonne équilibre)
        # ce choix par rapport au pourcentage vient après avoir regarder si pas des cartes broken 

        # Variables utiles 
        best_index = None  # Stocke l'index de la meilleure carte choisie

        # REGARDE SI Y A DES CARTES TRES FORTES
        criteres = [
            # Priorité haute
            # 1. Privilégie G + my_health_change
            lambda i: "G" in abilities[i] and tab_my_health_change[i] > 0,

            # 2. Privilégie G + opponent_health_change
            lambda i: "G" in abilities[i] and tab_opponent_health_change[i] < 0,

            # 7. My_health_change >= 4
            lambda i: tab_my_health_change[i] >= 4,

            # 8. Opponent_health_change <= -2
            lambda i: tab_opponent_health_change[i] <= -2,

            # 9. My_health_change >= 2 and opponent_health_change <= -1
            lambda i: tab_my_health_change[i] >= 2 and tab_opponent_health_change[i] <= -1,

            # 10. Privilégie B + my_health_change
            lambda i: "B" in abilities[i] and tab_my_health_change[i] > 0,

            # 11. Privilégie B + opponent_health_change
            lambda i: "B" in abilities[i] and tab_opponent_health_change[i] < 0,

            lambda i: "B" in abilities[i] and tab_opponent_health_change[i] < 0,

            
            # type 1 (obj verte) avec attaque et defense >= +2 
            #lambda i:  1 in cards_type[i] and attacks[i] >= 2 and defenses[i] >= 2,

            # type 2 (obj rouge) avec attaque et defense <= +2

            # type 3 (obj verte) avec attaque et defense >= +2 

            #lambda i:  1 in cards_type[i] and attacks[i] >= 2 and defenses[i] >= 2,


            # Autres critères si pas au dessus de 80%
            # 3. Privilégie G + card_draw
            lambda i: "G" in abilities[i] and tab_card_draw[i] > 0,

            # 4. Privilégie G + B
            lambda i: "G" in abilities[i] and "B" in abilities[i],

            # 5. Privilégie G + C
            lambda i: "G" in abilities[i] and "C" in abilities[i],

            # 6. Privilégie G seul
            lambda i: "G" in abilities[i],

            # 12. Privilégie B + card_draw
            lambda i: "B" in abilities[i] and tab_card_draw[i] > 0,

            # 13. Privilégie B + C
            lambda i: "B" in abilities[i] and "C" in abilities[i],

            # 14. Privilégie B seul
            lambda i: "B" in abilities[i],

            # 15. My_health_change >= 2
            lambda i: tab_my_health_change[i] >= 2,

            # 16. My_health_change >= 1 and opponent_health_change <= -1
            lambda i: tab_my_health_change[i] >= 1 and tab_opponent_health_change[i] <= -1,

            # 17. Privilégie C + my_health_change
            lambda i: "C" in abilities[i] and tab_my_health_change[i] > 0,

            # 18. Privilégie C + opponent_health_change
            lambda i: "C" in abilities[i] and tab_opponent_health_change[i] < 0,

            # 19. Privilégie C + card_draw
            lambda i: "C" in abilities[i] and tab_card_draw[i] > 0,

            # 20. Privilégie C seul
            lambda i: "C" in abilities[i],

            # 21. Privilégie l'attaque la plus élevée
            lambda i: attacks[i] == max(attacks),
        ]

        # Parcours les critères et sélectionne le premier qui correspond
        for critere in criteres:
            for i in range(3):
                if critere(i):
                    best_index = i
                    break
            if best_index is not None:
                break

        #mise à jour pourcentage des types de cartes
        if best_index is not None:
            for i in range(4):
                if cards_type[best_index] == i:
                    tab_types[i] += 1
            print(f"Après mise à jour: {tab_types}", file=sys.stderr, flush=True)
            pourcentage = tab_types[0] / sum(tab_types)  # Éviter la division par zéro
        else:
            pourcentage = tab_types[0] / sum(tab_types) if sum(tab_types) > 0 else 0 

        print(f"### TESTTTTTTT pourcentage : ### {pourcentage}", file=sys.stderr, flush=True)

        # Affichage et choix de la carte
        print(f"Carte choisie : {best_index}", file=sys.stderr, flush=True)
        print(f"PICK {best_index}")

    


#===================================================
#BATTLE PHASE
#===================================================

    else:
        #ensemble des variables utiles 
        actions = []
        possibilities=[]
        ind=0
        count_action=0
        tab_Abilities_detection=Abilities_detection(OpponentGame)  # recup les id des cartes opponent avec des abilities
        break_all = False  # Flag pour arrêter après un SUMMON
        break_all_attack = False  # Flag pour arrêter après une attaque réussie
        charge_attack_done = False  # Flag pour savoir si l'attaque a été effectuée pour la dernière carte ioché a l'instant



        ### LE CHOIX DE LA CARTE A ENVOYER (SUMMON) ###

        if len(MyGame)<6:   #vérifie qu'on a pas déjà 6 cartes sur le plateau pour pas envoyer d'autres cartes car impossible

            for elt in MyHand:
                if player_mana >= dico[elt]["cost"] and not dico[elt]["card_type"]>0:  # Sélectionne seulement les cartes jouables
                    possibilities.append(elt)
        
        # Sélectionne les cartes jouables en fonction du mana
            for i in range(len(MyHand)):
                break_all = False


                #A OPTI
                # 1. Privilégie Guard + my_health_change >= 4
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 4:  # Guard + soin >= 4
                        MyGame.append(elt)
                        possibilities.remove(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        player_mana -= dico[elt]["cost"]
                        break

                # 2.  privilégie Guard + opponent_health_change <= -2
                if not break_all:
                    for elt in possibilities:
                        if "G" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Guard + dégâts adversaire >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 3.  privilégie Guard + card_draw >= 2
                if not break_all:
                    for elt in possibilities:
                        if "G" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 2:  # Guard + pioche >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 4.  privilégie Guard + Breakthrough
                if not break_all:
                    for elt in possibilities:
                        if "G" in dico[elt]["abilitie"] and "B" in dico[elt]["abilitie"]:  # Guard + Breakthrough
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 5.  privilégie Guard + Charge
                if not break_all:
                    for elt in possibilities:
                        if "G" in dico[elt]["abilitie"] and "-C-" in dico[elt]["abilitie"]:  # Guard + Charge
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 6.  privilégie Guard
                if not break_all:
                    for elt in possibilities:
                        if "G" in dico[elt]["abilitie"]:  # Guard seul
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 7.  privilégie my_health_change >= 4
                if not break_all:
                    for elt in possibilities:
                        if dico[elt]["my_health_change"] >= 4:  # Soin >= 4
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 8.  privilégie opponent_health_change <= -2
                if not break_all:
                    for elt in possibilities:
                        if dico[elt]["opponent_health_change"] <= -2:  # Dégâts adversaire >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 9.  privilégie my_health_change >= 2 et opponent_health_change <= -1
                if not break_all:
                    for elt in possibilities:
                        if dico[elt]["my_health_change"] >= 2 and dico[elt]["opponent_health_change"] <= -1:  # Soin >= 2 et dégâts adversaire >= 1
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 10.  privilégie Breakthrough + my_health_change >= 2
                if not break_all:
                    for elt in possibilities:
                        if "B" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 2:  # Breakthrough + soin >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 11.  privilégie Breakthrough + opponent_health_change <= -2
                if not break_all:
                    for elt in possibilities:
                        if "B" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Breakthrough + dégâts adversaire >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 12.  privilégie Breakthrough + card_draw >= 1
                if not break_all:
                    for elt in possibilities:
                        if "B" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 1:  # Breakthrough + pioche >= 1
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 13.  privilégie Breakthrough + Charge
                if not break_all:
                    for elt in possibilities:
                        if "B" in dico[elt]["abilitie"] and "-C-" in dico[elt]["abilitie"]:  # Breakthrough + Charge
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 14.  privilégie Breakthrough seul
                if not break_all:
                    for elt in possibilities:
                        if "B" in dico[elt]["abilitie"]:  # Breakthrough seul
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 15.  privilégie Charge + my_health_change >= 2
                if not break_all:
                    for elt in possibilities:
                        if "-C-" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 2:  # Charge + soin >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 16.  privilégie Charge + opponent_health_change <= -2
                if not break_all:
                    for elt in possibilities:
                        if "-C-" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Charge + dégâts adversaire >= 2
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 17.  privilégie my_health_change >= 1 et opponent_health_change <= -1
                if not break_all:
                    for elt in possibilities:
                        if dico[elt]["my_health_change"] >= 1 and dico[elt]["opponent_health_change"] <= -1:  # Soin >= 2 et dégâts adversaire >= 1
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 18.  privilégie Charge + card_draw >= 1
                if not break_all:
                    for elt in possibilities:
                        if "-C-" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 1:  # Charge + pioche >= 1
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 19.  privilégie Charge seul
                if not break_all:
                    for elt in possibilities:
                        if "-C-" in dico[elt]["abilitie"]:  # Charge seul
                            MyGame.append(elt)
                            possibilities.remove(elt)
                            actions.append(f"SUMMON {elt}")
                            break_all = True
                            player_mana -= dico[elt]["cost"]
                            break

                # 20.  privilégie la carte avec la plus grosse attaque
                if not break_all and possibilities:
                    ind = max(range(len(possibilities)), key=lambda i: dico[possibilities[i]]["attack"])
                    MyGame.append(possibilities[ind])
                    actions.append(f"SUMMON {possibilities[ind]}")
                    player_mana -= dico[possibilities[ind]]["cost"]
                    possibilities.remove(possibilities[ind])




        ### LES ATTACKS ###

        # Initialisation de break_all_attack à False avant de commencer les attaques
        for elt in MyGame[:-1]:  # Le :-1 car la dernière carte est appelée par SUMMON et ne peut pas attaquer sauf si capa G
            if dico[elt]["attack"] == 0:  # Ne fais pas attaquer la carte si son attack vaut 0 car elle ne peut que perdre de la vie
                continue  # Passe à la carte suivante, pas d'attaque possible

            break_all_attack = False  # Réinitialise break_all_attack pour chaque carte

            if not break_all_attack:
                # Si la carte possède une capacité spéciale dans tab_Abilities_detection
                if tab_Abilities_detection:
                    for elt2 in tab_Abilities_detection:
                        if dico[elt2]["defense"] > 0:  # Si l'adversaire a de la défense
                            actions.append(f"ATTACK {elt} {elt2}")  # Attaque la carte avec défense
                            dico[elt2]["defense"] -= dico[elt]["attack"]  # Réduit la défense de la carte attaquée
                            break_all_attack = True  # Une attaque a été effectuée
                            if dico[elt2]["defense"] <= 0:
                                tab_Abilities_detection.remove(elt2)  # Si la défense tombe à 0, retirer la carte de tab_Abilities_detection
                            break  # Passe à la carte suivante

            if not break_all_attack:
                # Si aucune attaque n'a été effectuée, chercher une cible dans OpponentGame
                for elt3 in OpponentGame:
                    if dico[elt3]["defense"] > 0:  # Si l'adversaire a de la défense
                        actions.append(f"ATTACK {elt} {elt3}")  # Attaque l'adversaire
                        dico[elt3]["defense"] -= dico[elt]["attack"]  # Réduit la défense de l'adversaire
                        break_all_attack = True  # Une attaque a été effectuée
                        break  # Passe à la carte suivante

            if not break_all_attack:
                # Si aucune attaque n'a eu lieu, attaque le héros adverse directement
                actions.append(f"ATTACK {elt} -1")  # Attaque le héros adverse directement



        if MyGame:  # Vérifie si MyGame n'est pas vide pour eviter les problèmes d'index
            if dico[MyGame[-1]]["abilitie"] == "-C----":  # Permet à la carte qui vient d'être piochée d'attaquer si elle a la capacité Charge
                if tab_Abilities_detection:
                    for elt2 in tab_Abilities_detection:
                        if dico[elt2]["defense"] > 0:
                            actions.append(f"ATTACK {MyGame[-1]} {elt2}")
                            dico[elt2]["defense"] -= dico[MyGame[-1]]["attack"]
                            charge_attack_done = True  # L'attaque a été réalisée
                            if dico[elt2]["defense"] <= 0:
                                tab_Abilities_detection.remove(elt2)
                            break

                if not charge_attack_done:
                    for elt3 in OpponentGame:
                        if dico[elt3]["defense"] > 0:
                            actions.append(f"ATTACK {MyGame[-1]} {elt3}")
                            dico[elt3]["defense"] -= dico[MyGame[-1]]["attack"]
                            charge_attack_done = True
                            break

                if not charge_attack_done:
                    actions.append(f"ATTACK {MyGame[-1]} -1")  # Attaque directe le héros adverse



        if actions:                                        # envoie de l'ensemble des actions réalisé !
            print(f";".join(actions), file=sys.stderr, flush=True)
            print(";".join(actions))
        else:
            print("PASS")