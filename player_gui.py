import pygame
from hand import Hand
from card import Card
from my_client import Client
import gui_helper
from gui_helper import WIDTH, HEIGHT, FPS, CARD_SIZE, TITLE


def draw_hand(hand):
    cards_location = gui_helper.hand_to_cards_location(hand, cards_images)
    for card_image, location in cards_location.values():
        WIN.blit(card_image, location)


def draw_enemy_cards(num_of_cards):
    enemy_image, enemy_location = gui_helper.enemy_cards_location(num_of_cards)
    for loc in enemy_location:
        WIN.blit(enemy_image, loc)


def draw_garbage(card):
    card_image = cards_images[str(card)]
    WIN.blit(card_image, gui_helper.GARBAGE_LOCATION)


def draw_deck(card):
    if card:
        card_image = cards_images[str(card)]
    else:
        card_image = gui_helper.BACK_CARD_IMAGE
    WIN.blit(card_image, gui_helper.DECK_LOCATION)


def what_was_clicked(mouse_pos):
    pass


def main():
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        client.send("Get")

        game_status = client.receive_data()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If exit window was clicked
                return
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

        # Drawing
        if game_status != "Game did not start yet":
            draw_hand(game_status.hand)
            draw_enemy_cards(game_status.enemy_num_cards)
            draw_deck(game_status.deck_card)
            draw_garbage(game_status.garbage_card)
        else:
            WIN.blit(background_image, (0, 0))

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    # Setup window
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # Setup background
    background_image = gui_helper.background_image
    WIN.blit(background_image, (0, 0))
    pygame.display.update()

    # Dict with cards images
    cards_images = gui_helper.create_cards_image_dict()

    # Client stuff
    Client
    client = Client()
    client.connect()

    main()
    client.close()
