import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    #key pressed
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    #key released
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
#watch for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button (ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)           
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)


def check_play_button (ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    #start new game when player clicks play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        #hide the mouse cursor
        pygame.mouse.set_visible(False)

        #reset stats
        stats.reset_stats()
        stats.game_active = True

        #reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #empty aliens and bullets
        aliens.empty()
        bullets.empty()

        #create new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    #update images on the screen and flip to new screen
    #fill bg color
    screen.fill(ai_settings.bg_color)

    #redraw all bullet behind ship and aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #draw the play game buttom if the game is inactive
    if stats.game_active != True:
        play_button.draw_button()

    #make the most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    #get rid of disappeared bullets
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
    

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #check for any bullets that have hit aliens and get rid of the alien and bullet
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens)==0:
        #if entire fleet is destroyed, increase level
        #get rid of bullets
        bullets.empty()
        #speed up game and create new fleet
        ai_settings.increase_speed()

        #increase level
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    #create a new bullet and add it to bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(ai_settings, screen, ship, aliens):
    #create an alien and find number of aliens in a row
    #spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    for row_number in range(number_rows):
        create_alien(ai_settings, screen, aliens, number_aliens_x, row_number)


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - (2*alien_width)
    number_aliens_x = int(available_space_x/(2*alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number_x, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    for alien_number in range(alien_number_x):
        alien = Alien(ai_settings,screen)
        alien.x = alien_width + (2 * alien_width* alien_number)
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    #drop the entire fleet and change the fleet's direction
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #check if the fleet is at an edge and then update positions of all aliens
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit (ai_settings, screen, stats, sb, ship, aliens, bullets)

    #look for aliens hitting bottom of screen
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)


def ship_hit (ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        #decrement ships left and display ships left
        stats.ships_left -= 1
        sb.prep_ships()

        #empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        #create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #check aliens that have reached the bottom
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    #check if there is a new high score
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()