import sys
import math

Tour = 0


# Game loop
while True:
    player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
    ennemy_health, ennemy_mana, ennemy_deck, ennemy_rune, ennemy_draw = [int(j) for j in input().split()]

    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    
    for i in range(opponent_actions):
        input()  # On consomme bien toutes les lignes d'action de l'adversaire
    
    card_count = int(input())

    # Listes des coûts, attaques et défenses des monstres à sélectionner
    costs = []
    attacks = []
    defenses = []
    locations = []
    abilities=[]
    tab_my_health_change=[]
    tab_opponent_health_change=[]
    tab_card_draw=[]

    dico = {}

    # Mon jeu 
    MyHand = []

    # Mes cartes jouées
    MyGame = []

    # Liste des cartes que l'adversaire a en jeu
    OpponentGame = []

    # Enlever les cartes jouées de ma main
    MyHand = [elt for elt in MyHand if elt not in MyGame]

    # Récupérer les infos des cartes
    for i in range(card_count):
        inputs = input().split()
        card_number = int(inputs[0])
        instance_id = int(inputs[1])
        location = int(inputs[2])
        card_type = int(inputs[3])
        cost = int(inputs[4])
        attack = int(inputs[5])
        defense = int(inputs[6])
        abilitie = inputs[7]
        my_health_change = int(inputs[8])
        opponent_health_change = int(inputs[9])
        card_draw = int(inputs[10])
        
        #des tab pour recup les infos des 3 cartes et faire le meilleur choix
        locations.append(location)
        costs.append(cost)
        attacks.append(attack)
        defenses.append(defense)
        abilities.append(abilitie)
        tab_my_health_change.append(my_health_change)
        tab_opponent_health_change.append(opponent_health_change)
        tab_card_draw.append(card_draw)

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
            #print("### nb" + str(instance_id) + str(dico[instance_id]['defense']), file=sys.stderr, flush=True)

            if location == 0 and instance_id not in MyHand:
                MyHand.append(instance_id)
            elif location == 1 and instance_id not in MyGame:
                MyGame.append(instance_id)
            elif location == -1 and instance_id not in OpponentGame:
                OpponentGame.append(instance_id)

    # Affichage Information de base  
    Tour += 1
    print(f"#### Tour n°{Tour} ####", file=sys.stderr, flush=True)
    print(f"Ma mana : {player_mana} | Ma vie : {player_health}\n", file=sys.stderr, flush=True)
    print(f"My Hand : {MyHand}", file=sys.stderr, flush=True)
    print(f"My Game : {MyGame}", file=sys.stderr, flush=True)
    print(f"Opponent Game : {OpponentGame}\n", file=sys.stderr, flush=True)

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
        print(f"### TESTTTTTTT ### {tab}", file=sys.stderr, flush=True)
        return tab

    # Phase de draft
    if Tour < 31:
        print(f"Prix Mana : {costs}", file=sys.stderr, flush=True)
        print(f"val_attaques : {attacks}", file=sys.stderr, flush=True)
        print(f"Les abilitie : {abilities}", file=sys.stderr, flush=True)
        print(f"Les dégats en plus affligé à l'adversaire : {tab_opponent_health_change}", file=sys.stderr, flush=True)

        best_index = None  # Stocke l'index de la meilleure carte choisie

        # 1. Privilégie G + my_health_change
        for i in range(3):
            if "G" in abilities[i] and tab_my_health_change[i] > 0:
                best_index = i
                break

        # 2. Privilégie G + opponent_health_change
        if best_index is None:
            for i in range(3):
                if "G" in abilities[i] and tab_opponent_health_change[i] < 0:
                    best_index = i
                    break

        # 3. Privilégie G + card_draw
        if best_index is None:
            for i in range(3):
                if "G" in abilities[i] and tab_card_draw[i] > 0:
                    best_index = i
                    break

        # 4. Privilégie G + B
        if best_index is None:
            for i in range(3):
                if "G" in abilities[i] and "B" in abilities[i]:
                    best_index = i
                    break

        # 5. Privilégie G + C
        if best_index is None:
            for i in range(3):
                if "G" in abilities[i] and "C" in abilities[i]:
                    best_index = i
                    break

        # 6. Privilégie G seul
        if best_index is None:
            for i in range(3):
                if "G" in abilities[i]:
                    best_index = i
                    break

        # 7. My_health_change >= 4
        if best_index is None:
            for i in range(3):
                if tab_my_health_change[i] >= 4:
                    best_index = i
                    break

        # 8. Opponent_health_change <= -2
        if best_index is None:
            for i in range(3):
                if tab_opponent_health_change[i] <= -2:
                    best_index = i
                    break

        # 9. My_health_change >= 2 and opponent_health_change <= -1
        if best_index is None:
            for i in range(3):
                if tab_my_health_change[i] >= 2 and tab_opponent_health_change[i] <= -1:
                    best_index = i
                    break

        # 10. Privilégie B + my_health_change
        if best_index is None:
            for i in range(3):
                if "B" in abilities[i] and tab_my_health_change[i] > 0:
                    best_index = i
                    break

        # 11. Privilégie B + opponent_health_change
        if best_index is None:
            for i in range(3):
                if "B" in abilities[i] and tab_opponent_health_change[i] < 0:
                    best_index = i
                    break

        # 12. Privilégie B + card_draw
        if best_index is None:
            for i in range(3):
                if "B" in abilities[i] and tab_card_draw[i] > 0:
                    best_index = i
                    break

        # 13. Privilégie B + C
        if best_index is None:
            for i in range(3):
                if "B" in abilities[i] and "C" in abilities[i]:
                    best_index = i
                    break

        # 14. Privilégie B seul
        if best_index is None:
            for i in range(3):
                if "B" in abilities[i]:
                    best_index = i
                    break

        # 15. My_health_change >= 2
        if best_index is None:
            for i in range(3):
                if tab_my_health_change[i] >= 2:
                    best_index = i
                    break

        # 16. My_health_change >= 1 and opponent_health_change <= -1
        if best_index is None:
            for i in range(3):
                if tab_my_health_change[i] >= 1 and tab_opponent_health_change[i] <= -1:
                    best_index = i
                    break

        # 17. Privilégie C + my_health_change
        if best_index is None:
            for i in range(3):
                if "C" in abilities[i] and tab_my_health_change[i] > 0:
                    best_index = i
                    break

        # 18. Privilégie C + opponent_health_change
        if best_index is None:
            for i in range(3):
                if "C" in abilities[i] and tab_opponent_health_change[i] < 0:
                    best_index = i
                    break

        # 19. Privilégie C + card_draw
        if best_index is None:
            for i in range(3):
                if "C" in abilities[i] and tab_card_draw[i] > 0:
                    best_index = i
                    break

        # 20. Privilégie C seul
        if best_index is None:
            for i in range(3):
                if "C" in abilities[i]:
                    best_index = i
                    break

        # 21. Privilégie l'attaque la plus élevé
        if best_index is None:
            best_index = attacks.index(max(attacks))

        # Affichage et choix de la carte
        print(f"Carte choisie : {best_index}", file=sys.stderr, flush=True)
        print(f"PICK {best_index}")

    


    # Phase de bataille
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



        # LE CHOIX DE LA CARTE A ENVOYER (SUMMON)
        if len(MyGame)<6:   #vérifie qu'on a pas déjà 6 cartes sur le plateau pour pas envoyer d'autres cartes car impossible
        # Sélectionne les cartes jouables en fonction du mana
            for elt in MyHand:
                if player_mana >= dico[elt]["cost"]:  # Sélectionne seulement les cartes jouables
                    possibilities.append(elt)

            # 1. Privilégie Guard + my_health_change >= 4
            for elt in possibilities:
                if "G" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 4:  # Guard + soin >= 4
                    MyGame.append(elt)
                    actions.append(f"SUMMON {elt}")
                    break_all = True
                    break

            # 2.  privilégie Guard + opponent_health_change <= -2
            if not break_all:
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Guard + dégâts adversaire >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 3.  privilégie Guard + card_draw >= 2
            if not break_all:
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 2:  # Guard + pioche >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 4.  privilégie Guard + Breakthrough
            if not break_all:
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"] and "B" in dico[elt]["abilitie"]:  # Guard + Breakthrough
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 5.  privilégie Guard + Charge
            if not break_all:
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"] and "-C-" in dico[elt]["abilitie"]:  # Guard + Charge
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 6.  privilégie Guard
            if not break_all:
                for elt in possibilities:
                    if "G" in dico[elt]["abilitie"]:  # Guard seul
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 7.  privilégie my_health_change >= 4
            if not break_all:
                for elt in possibilities:
                    if dico[elt]["my_health_change"] >= 4:  # Soin >= 4
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 8.  privilégie opponent_health_change <= -2
            if not break_all:
                for elt in possibilities:
                    if dico[elt]["opponent_health_change"] <= -2:  # Dégâts adversaire >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 9.  privilégie my_health_change >= 2 et opponent_health_change <= -1
            if not break_all:
                for elt in possibilities:
                    if dico[elt]["my_health_change"] >= 2 and dico[elt]["opponent_health_change"] <= -1:  # Soin >= 2 et dégâts adversaire >= 1
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 10.  privilégie Breakthrough + my_health_change >= 2
            if not break_all:
                for elt in possibilities:
                    if "B" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 2:  # Breakthrough + soin >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 11.  privilégie Breakthrough + opponent_health_change <= -2
            if not break_all:
                for elt in possibilities:
                    if "B" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Breakthrough + dégâts adversaire >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 12.  privilégie Breakthrough + card_draw >= 1
            if not break_all:
                for elt in possibilities:
                    if "B" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 1:  # Breakthrough + pioche >= 1
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 13.  privilégie Breakthrough + Charge
            if not break_all:
                for elt in possibilities:
                    if "B" in dico[elt]["abilitie"] and "-C-" in dico[elt]["abilitie"]:  # Breakthrough + Charge
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 14.  privilégie Breakthrough seul
            if not break_all:
                for elt in possibilities:
                    if "B" in dico[elt]["abilitie"]:  # Breakthrough seul
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 15.  privilégie Charge + my_health_change >= 2
            if not break_all:
                for elt in possibilities:
                    if "-C-" in dico[elt]["abilitie"] and dico[elt]["my_health_change"] >= 2:  # Charge + soin >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 16.  privilégie Charge + opponent_health_change <= -2
            if not break_all:
                for elt in possibilities:
                    if "-C-" in dico[elt]["abilitie"] and dico[elt]["opponent_health_change"] <= -2:  # Charge + dégâts adversaire >= 2
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 17.  privilégie my_health_change >= 1 et opponent_health_change <= -1
            if not break_all:
                for elt in possibilities:
                    if dico[elt]["my_health_change"] >= 1 and dico[elt]["opponent_health_change"] <= -1:  # Soin >= 2 et dégâts adversaire >= 1
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 18.  privilégie Charge + card_draw >= 1
            if not break_all:
                for elt in possibilities:
                    if "-C-" in dico[elt]["abilitie"] and dico[elt]["card_draw"] >= 1:  # Charge + pioche >= 1
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 19.  privilégie Charge seul
            if not break_all:
                for elt in possibilities:
                    if "-C-" in dico[elt]["abilitie"]:  # Charge seul
                        MyGame.append(elt)
                        actions.append(f"SUMMON {elt}")
                        break_all = True
                        break

            # 20.  privilégie la carte avec la plus grosse attaque
            if not break_all and possibilities:
                ind = max(range(len(possibilities)), key=lambda i: dico[possibilities[i]]["attack"])
                MyGame.append(possibilities[ind])
                actions.append(f"SUMMON {possibilities[ind]}")



        #LES ATTACKS

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
