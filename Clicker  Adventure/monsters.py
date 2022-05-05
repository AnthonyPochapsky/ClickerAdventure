#Import essential module and initialize the pygame module to be imported into the main program.
import pygame
pygame.init()

#Classify the Monster Class.
class Monster(pygame.sprite.Sprite):
    #Initialize the attributes that will be included in all of the regular monster objects.
    def __init__(self,monster_HP,player_damage,monster_EXP,neutral_state):
        self.monster_HP=monster_HP
        self.player_damage=player_damage
        self.monster_EXP=monster_EXP
        self.neutral_state=neutral_state
    #Call this method in the main program to increase the health of the monster after the previous monster's defeat.
    #Accomplished through reassigning the total HP of the defeated monster and including a percent health boost.
    def HP_buff(self,percent_increase,monster_previous_hp):
        self.monster_HP=round(monster_previous_hp*percent_increase)
    #Call this method in the main program to retrieve the full HP value of the current monster before any damage is dealt.
    def full_HP(self):
        return self.monster_HP
    #Call this method in the main program to add onto the players base damage by additively increasing the player's damage by 1 each call.
    def damage_up(self,damage_increase):
        self.player_damage +=damage_increase
    #Call this method in the main program to reduce the current monster's HP by the player's damage until the monster is finished.
    def damage_taken(self):
        self.monster_HP=self.monster_HP-self.player_damage
        return self.monster_HP
    #Call this method in the main program to increase the amoount of EXP that the next monster will give by a certain precent.
    def add_EXP(self,EXP_added_percent):
        self.monster_EXP *=round(EXP_added_percent)
    #Call this method in the main program to gain the EXP value that the current monster's defeat will lend the player.
    def EXP_gained(self):
        return self.monster_EXP
    #Call this method in the main program to return a resized image of the currently slelected monster.
    def image(self):
        monster=pygame.image.load(self.neutral_state)
        monster=pygame.transform.smoothscale(monster,(175,175))
        return monster
    
#Classify the Boss_Monster Class
class Boss_Monster(pygame.sprite.Sprite):
    #Initialize the attributes that will be included in all of the boss monster objects.
    def __init__(self,boss_HP,player_damage,name,boss_neutral_state):
        self.name=name
        self.boss_HP=boss_HP
        self.player_damage=player_damage
        self.boss_neutral_state=boss_neutral_state
    #Call this method in the main program to retrieve the fu;; HP of the selected boss monster before any damage is dealt.
    def full_HP(self):
        return self.boss_HP
    #Call this method in the main program to apply the player's damage to all boss monster types.
    def damage_up(self,damage_increase):
        self.player_damage +=damage_increase
    #Call this method in the main program when the selected boss monster takes damage.
    def damage_taken(self):
        self.boss_HP=self.boss_HP-self.player_damage
        return self.boss_HP
    #Call this method in the main program to retrieve and resize the image of the selected boss monster.
    def image(self):
        boss_monster=pygame.image.load(self.boss_neutral_state)
        boss_monster=pygame.transform.smoothscale(boss_monster,(300,300))
        return boss_monster
    #Call this method in the main program to retrieve the name of the selected boss monster
    def boss_name(self):
        return self.name
