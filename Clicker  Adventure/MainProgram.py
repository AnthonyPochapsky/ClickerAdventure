#Clicker Heroes Adventure

#Import essential modules. 
import monsters
import utility
import pygame
import sys
import random

#Initial Values to be used later on.
full_health=0
monster_HP=1
base_player_damage=1
damage_increase_int=0
player_damage_buff=1
EXP_needed=5
EXP_gained_from_monster=0
EXP_earned=0
player_level=1
monster_EXP=2
monsters_defeated=0
total_monsters_defeated=0
monsters_needed=10
monster_damage_taken=0
monster_HP_buff_amount=1.5
boss_time=False
boss_allowed=False
boss_kills=0

#Instructions.
print("\nHow To Play:\n")
print("- Click on the monster at the centre of the screen to deplete their health.\n")
print("- Slaying a monster rewards you with EXP allowing you to level up and gain more damage.\n")
print("- Each time you slay a monster the following monster strengthen but so does their EXP reward.\n")
print("- You need to defeat the minimum number of monsters listed on the screen to challenge each of the four bosses.\n")
print("- Defeating a boss reduces the amount of monsters that need to be defeated, you gain more damage per level, and the HP boosts of the following monsters scale down.\n")
print("- Defeat all 4 bosses and beat the game.\n")
print("Good Luck!")

#Experimental Mode
experimenting=True
while experimenting:
    choice=input("\nType 'yes' if you want to enter experimental mode in which you can establish starting stats however you see fit or type 'no':")
    if choice.lower()=="yes": #Check if the player wants to initiate this mode.
        while True:
            #Allow the player to change the following variables.
            #If the player doesn't input in a number or that number is not between 1 and 50 run through a function in which the player can correct their mistake.
            try:
                monster_HP=int(input("Enter the value for the HP you want the first monster to begin with:"))
            except ValueError:
                print("Please only include numbers")
                monster_HP=utility.input_loop("Enter the value for the HP you want the first monster to begin with:")
            if monster_HP<1 or monster_HP>50:
                print("Only values between 1 and 50 allowed")
                monster_HP=utility.input_loop("Enter the value for the HP you want the first monster to begin with:")
            
            try:
                base_player_damage=int(input("Enter the initial value for your starting damage:"))
            except ValueError:
                print("Please only include numbers")
                base_player_damage=utility.input_loop("Enter the initial value for your starting damage:")
            if base_player_damage<1 or base_player_damage>50:
                print("Only values between 1 and 50 allowed")
                base_player_damage=utility.input_loop("Enter the initial value for your starting damage:")
        
            try:
                player_damage_buff=int(input("Enter the initial value of the amount of damage you want to gain per level:"))
            except ValueError:
                print("Please only include numbers")
                player_damage_buff=utility.input_loop("Enter the initial value of the amount of damage you want to gain per level:")
            if player_damage_buff<1 or player_damage_buff>50:
                print("Only values between 1 and 50 allowed")
                player_damage_buff=utility.input_loop("Enter the initial value of the amount of damage you want to gain per level:")
                
            try:
                EXP_needed=int(input("Enter the initial amount of EXP you need to level up:"))
            except ValueError:
                print("Please only include numbers")
                EXP_needed=utility.input_loop("Enter the initial amount of EXP you need to level up:")
            if EXP_needed<1 or EXP_needed>50:
                print("Only values between 1 and 50 allowed")
                EXP_needed=utility.input_loop("Enter the initial amount of EXP you need to level up:")
    
            try:
                monster_EXP=int(input("Enter the initial amount of EXP you want the first monster to give you:"))
            except ValueError:
                print("Please only include numbers")
                monster_EXP=utility.input_loop("Enter the initial amount of EXP you want the first monster to give you:")
            if monster_EXP<1 or monster_EXP>50:
                print("Only values between 1 and 50 allowed")
                monster_EXP=utility.input_loop("Enter the initial amount of EXP you want the first monster to give you:")
            
            experimenting=False
            break       
    elif choice.lower()=="no": #Check if the player doesn't want to initiate this mode.
        break
    
#Fonts + Boss Button.
HP_lost_font_type=pygame.font.SysFont("comicsans",75)
monsters_defeated_font_type=pygame.font.SysFont("comicsans",100)
level_and_EXP_font_type=pygame.font.SysFont("comicsans",50)
damage_bonus_font_type=pygame.font.SysFont("comicsans",50)
boss_name_font_type=pygame.font.SysFont("comicsans",125)
boss_button=pygame.image.load("boss_button.PNG")

#Post victory fonts and logo.
victory_header_font_type=pygame.font.SysFont("comicsans",125)
final_stats_font_types=pygame.font.SysFont("comicsans",75)
game_title_image=pygame.image.load("clicker_hero_title.png")

#Types of regular monsters with assigned attributes that are all shared except for the image.
big_feets=monsters.Monster(monster_HP,base_player_damage,monster_EXP,"big_feets.png")
mouse=monsters.Monster(monster_HP,base_player_damage,monster_EXP,"mouse.png")
orc=monsters.Monster(monster_HP,base_player_damage,monster_EXP,"orc.png")
sage_shroom=monsters.Monster(monster_HP,base_player_damage,monster_EXP,"sage_shroom.png")
#Place all the different regular monster types into a tuple to be randomly selected later on.
monster_types=(big_feets,mouse,orc,sage_shroom)

#Types of boss monsters with shared player damage and different HP pools and images.
dark_wizard=monsters.Boss_Monster(4000,base_player_damage,"Dark Wizard","dark_wizard.png")
dread_eye=monsters.Boss_Monster(10000,base_player_damage,"Dread Eye","dread_eye.png")
ultra_bloop=monsters.Boss_Monster(20000,base_player_damage,"Ultra Bloop","ultra_bloop.png")
orc_lord=monsters.Boss_Monster(1000,base_player_damage,"Orc Lord","orc_lord.png")
#Place all the different boss monster types into a tuple to so that player_damage is distributed across them all.
boss_types=(dark_wizard,orc_lord,dread_eye,ultra_bloop)

#Screen Characteristics and backgrounds.
screen_width=750
screen_height=750
screen_colour=(255,255,255)
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Clicker Heroes Adventure")
main_background=pygame.image.load("main_background.jpg")
main_background=pygame.transform.smoothscale(main_background,(750,750))
boss_background=pygame.image.load("boss_background.PNG")
boss_background=pygame.transform.smoothscale(boss_background,(750,750))

#Allow the game to run continuously until the player wins.
running=True
while running:
    #If the player has just started the game or just defeated a boss play the main theme on repeat. 
    if monsters_defeated==0:
        theme=pygame.mixer.music.load("main_theme.ogg")
        theme=pygame.mixer.music.play(-1)
    #If the boss has been activated play the boss theme on repeat.
    elif boss_time==True:
        theme=pygame.mixer.music.stop()
        theme=pygame.mixer.music.load("boss_theme.ogg")
        theme=pygame.mixer.music.play(-1)
    #If the boss has not been activated choose a random regular monster from a different tuple.
    if boss_time==False:
        monster_pick=random.choice(monster_types)
    #If the boss has been activated choose the correct boss in order of weakest to strongest based on boss kills.
    else:
        if boss_kills==0:
            monster_pick=orc_lord
        elif boss_kills==1:
            monster_pick=dark_wizard
        elif boss_kills==2:
            monster_pick=dread_eye
        elif boss_kills==3:
            monster_pick=ultra_bloop
        boss=monster_pick.boss_name()
    #Check if the boss fight has been activated and if so render the name of the chosen boss as a font to later take the place of the otherwise "monsters defeated font".
    if boss_time==True:
        boss_name_font=boss_name_font_type.render(str(boss),True,(0,0,0))
    else:
        monsters_defeated_font=monsters_defeated_font_type.render("Slain:"+str(monsters_defeated)+"/"+str(monsters_needed),True,(0,0,0))
    #Render the rest of the fonts with specified variables that may only update after monsters are consecutively defeated.
    level_font=level_and_EXP_font_type.render("Level:"+str(player_level),True,(0,0,255))
    EXP_font=level_and_EXP_font_type.render("EXP:"+str(EXP_earned)+"/"+str(EXP_needed),True,(0,0,255))
    #If the player is only level 1 and hence hasn't gained any damage bonus from levelling up, only render their base damage.
    if player_level==1:
        damage_bonus_font=damage_bonus_font_type.render("Click Damage:"+str(base_player_damage),True,(0,0,255))
    else:
        damage_bonus_font=damage_bonus_font_type.render("Click Damage:"+str(damage_increase_int+base_player_damage),True,(0,0,255))
    #Before the monster is blitted to the screen indicate that they are alive and have full hp.
    alive=True 
    full_hp_tracker=True
    full_health=monster_pick.full_HP() #Call the full_HP() method to gain the monsters full HP prior to them taking any damage.
    while alive:
        #If the monster hasn't taken any damage yet, display their remaining health as that of their full health.
        if full_hp_tracker==True:
            health_remaining=full_health
            HP_lost_font=HP_lost_font_type.render(("HP:"+str(health_remaining)+"/"+str(full_health)),True,(255,0,0))
        else:
            HP_lost_font=HP_lost_font_type.render(("HP:"+str(health_remaining)+"/"+str(full_health)),True,(255,0,0))
        if boss_time==False:
            screen.blit(main_background,(0,0)) #Blit the main background if the boss is not being fought.
        else:
            screen.blit(boss_background,(0,0)) #Otherwise blit the boss background
        #If boss is not activated, blit the randomly chosen regular monster and fonts that are unique to regular monsters alongside fonts that are shared with boss monsters.
        if boss_time==False:
            screen.blit(HP_lost_font,(225,150))
            screen.blit(monster_pick.image(),(300,325))
            screen.blit(monsters_defeated_font,(225,40))
            screen.blit(level_font,(75,600))
            screen.blit(EXP_font,(75,675))
            screen.blit(damage_bonus_font,(400,600))
        #If boss is activated, blit the boss monster and fonts that are unique to boss monsters alongside fonts that are shared with regular monsters.
        else:
            screen.blit(HP_lost_font,(225,150))
            screen.blit(monster_pick.image(),(215,250))
            screen.blit(boss_name_font,(225,40))
            screen.blit(level_font,(75,600))
            screen.blit(EXP_font,(75,675))
            screen.blit(damage_bonus_font,(400,600))
        if monsters_defeated>=monsters_needed:
            screen.blit(boss_button,(400,675)) #Blit a boss button to the screen if the player has defeated the minimum number of monsters required to fight the boss.
            boss_allowed=True  #Indicate that the boss is allowed to be fought so that the player won't be able to just click on that area of the screen and fight the boss whether or not the button is blitted.
        pygame.display.update() #Update the screen's colour and all of the various different things that were blitted prior to now.
        #Give the player the option to quit prior to winning.
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            #Allow the player to interact with the screen by clicking the left mouse button and getting the position of that click.
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    posx,posy=pygame.mouse.get_pos()
                    if boss_time==False: #Check that the boss had not been activated.
                        #After the player has damaged the regular monster by clicking on them...
                        if 300<=posx<=470 and 320<=posy<=500: #check to see if the player has indeed clicked within the parameters of where on the screen the regular monster has been blitted to.
                            full_hp_tracker=False #Let it be known that the monster no longer has full HP.
                            hit=pygame.mixer.Sound("hit.ogg") 
                            hit.play() #Play a sound effect that indicates the monster being hit.
                            health_remaining=monster_pick.damage_taken() #Call the method that reduces the monster's HP based on the player's total damage.
                            #After the player has done enough or more than enough damage to defeat the monster...
                            if health_remaining<=0:
                                death=pygame.mixer.Sound("death_effect.ogg")
                                death.play() #Play a death sound effect.
                                alive=False #Indicate that the monster is no longer alive so a new one can be chosen.
                                monsters_defeated +=1 #Indicate that the player has defeated one extra monster.
                                #Loop through each and every monster type including the one that was just fought and defeated to...
                                for monster in monster_types:
                                    monster.HP_buff(monster_HP_buff_amount,full_health) #When a monster is defeated return their original total and buff it by the current increase.
                                    EXP_gained_from_monster=monster.EXP_gained() #Assign the player the value of EXP gained by the monster they just defeated.
                                    monster.add_EXP(1.5) #As a monster is defeated, buff the amount of EXP that all future monsters give by a rounded value of 50%.
                                EXP_earned +=EXP_gained_from_monster #Fill up the player's EXP an additonal amount with the amount that they earned from defeating the current monster.
                                #After the player has gained enough EXP to level up...
                                if EXP_earned>=EXP_needed:
                                    player_level +=1 #Increase the player's level by 1.
                                    damage_increase_int +=player_damage_buff #Increase the player's damage bonus variable by the current increase so it could be added to the player's base damage when rendering the damage font.
                                    #Loop through each and every monster type after the player levels to...
                                    for monster in monster_types:
                                        damage_increase_call=monster.damage_up(player_damage_buff) #Increase the amount of damage that can be dealt to all future monsters by the current increase.
                                    #Damage dealt being the only property that carries over to the boss fight means that it has to be updated to each and every boss monster type as the player levels up.
                                    for boss in boss_types:
                                        damage_increase_call=boss.damage_up(player_damage_buff)
                                    EXP_needed *=round(3) #The EXP that the player requires per level up is increased by 3 times each level.
                                    EXP_earned=0  #The EXP the player has gained to previously level up is reverted back to 0.
                        elif 400<=posx<=612 and 675<=posy<=711 and boss_allowed==True: #Once the boss button appears give the player the option to activate the boss fight by clicking the screen area that it occupies.
                            boss_time=True
                            alive=False #Doing so will cancel any fight that the player is initiated in.
                    elif boss_time==True: #Check if the boss has been activated
                        if 215<=posx<=519 and 245<=posy<=550: #Check to see if the player has indeed clicked within the parameters of where on the screen the boss monster has been blitted to.
                            full_hp_tracker=False  #Let it be known that the boss no longer has full HP.
                            hit=pygame.mixer.Sound("hit.ogg")
                            hit.play()  #Play a sound effect that indicates the boss being hit.
                            health_remaining=monster_pick.damage_taken() #Call the method that reduces the boss's HP based on the player's total damage.
                            #Indicate that player has dealt enough damage to defeat the boss
                            if health_remaining<=0:
                                death=pygame.mixer.Sound("boss_death_effect.ogg")
                                death.play() #Play a more drawn out death sound effect.
                                player_damage_buff *=4 #For all future levels the player gains quadruple the damage bonus from leveling after defeating a boss.
                                alive=False #Indicate that the boss is indeed dead and no longer needs to be attacked.
                                total_monsters_defeated +=monsters_defeated #Add the number of monsters defeated between the last and current boss to the total. 
                                monsters_defeated=0 #Reset the value of monsters that need to be defeated for the next boss.
                                monsters_needed -=2 #Reduce the amount of monsters that need to be defeated by 2 each time a boss is slain.
                                monster_HP_buff_amount -=0.1 #Reduce the amount of extra health the monsters gain by 10%
                                boss_time=False #indicate that the next boss isn't activated.
                                boss_allowed=False #Prevent the next boss from being allowed to be fought after this one was just defeated.
                                boss_kills +=1 #Add a boss kill to the tracker
                                #Remove the player from the main game loop once they defeat all 4 bosses.
                                if boss_kills==4:
                                    running=False
#Calculate a score based on the player's level and the amount of monster's they chose to slay prior to the boss fight                                
score=(player_level*200)+(total_monsters_defeated*100)
#Render all the various victory messages that are meant to display final statistics.
victory_header_font=victory_header_font_type.render("Congratulations!",True,(0,0,255))
final_monsters_defeated_font=final_stats_font_types.render("Total Monsters Defeated:"+str(total_monsters_defeated),True,(0,0,255))
final_level_font=final_stats_font_types.render("Level Achieved:"+str(player_level),True,(0,0,255))
final_damage_font=final_stats_font_types.render("Click Damage Achieved:"+str(base_player_damage+damage_increase_int),True,(0,0,255))
final_score_font=final_stats_font_types.render("Overall Score:"+str(score),True,(0,0,255))
#Stop the boss music from playing to instead produce a victory sound effect.
pygame.mixer.music.stop()
victory_sound=pygame.mixer.Sound("victory.ogg")
victory_sound.play()
#Display the screen colour, logo, and blit all of the victory messages along with the option for the player to quit the game after winning.
while True:
    screen.fill(screen_colour)
    screen.blit(victory_header_font,(0,0))
    screen.blit(final_monsters_defeated_font,(0,120))
    screen.blit(final_level_font,(0,200))
    screen.blit(final_damage_font,(0,280))
    screen.blit(final_score_font,(0,360))
    screen.blit(game_title_image,(50,480))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
