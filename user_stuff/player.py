from typing import Tuple, Union

import gui_helper
import pygame

from game_stuff.card import Card
from game_stuff.game import Game_status_type
from gui_helper import WIDTH, HEIGHT, FPS, TITLE, FONT_SIZE
from game_stuff.hand import Hand
from client import Client

image_type = type(pygame.image)
Game_status_type = Game_status_type


def draw_hand(hand: Hand) -> None:
    """
    Draws a given hand
    """
    cards_location = gui_helper.hand_to_cards_location(hand, cards_images)
    for card_image, location in cards_location.values():
        WIN.blit(card_image, location)


def draw_enemy_cards(num_of_cards: int) -> None:
    """
    Draws The enemy's cards (the back side)
    """
    enemy_image, enemy_location = gui_helper.enemy_cards_location(num_of_cards)
    for loc in enemy_location:
        WIN.blit(enemy_image, loc)


def draw_garbage(card: Card) -> None:
    """
    Draws the top card in the garbage
    """
    card_image = cards_images[str(card)]
    WIN.blit(card_image, gui_helper.GARBAGE_LOCATION)


def draw_deck(card: Card) -> None:
    """
    Draws the top card of the deck if player's turn else, Draws the back side
    """
    if card:
        card_image = cards_images[str(card)]
    else:
        card_image = gui_helper.BACK_CARD_IMAGE
    WIN.blit(card_image, gui_helper.DECK_LOCATION)


def draw_button(game_status: Game_status_type) -> None:
    """
    Draws the 'try my luck' button
    """
    if game_status["asked_to_finish"]:
        WIN.blit(gui_helper.BUTTON_CLICKED_IMAGE, gui_helper.BUTTON_LOCATION)
    else:
        WIN.blit(gui_helper.BUTTON_IMAGE, gui_helper.BUTTON_LOCATION)


def draw_end_game(text: str) -> None:
    """
    Draws the text of the end of game - you win / you lose
    """
    text_location = (WIDTH // 2 - 100, HEIGHT // 2)
    text_color = (0, 0, 0)

    font = pygame.font.SysFont('arial', FONT_SIZE * 2)
    turn = font.render(text, True, text_color)
    WIN.blit(turn, text_location)


def draw_turn(game_status: Game_status_type) -> None:
    """
    Draws the text of whose turn is it
    """
    text_location = (30, 35)
    text_color = (0, 0, 0)

    text = "Your turn" if game_status["is_turn"] else "Enemy's turn"
    font = pygame.font.SysFont('arial', FONT_SIZE)
    turn = font.render(text, True, text_color)
    WIN.blit(turn, text_location)


def draw_all(game_status: Game_status_type) -> None:
    """
    Draws: hand, deck, garbage, enemy's cards, turn text, end game text
    """
    if game_status == "Game did not start yet":
        WIN.blit(background_image, (0, 0))  # Blank background
        pygame.display.update()
        return

    # If the game is finished
    if isinstance(game_status, str) and game_status.startswith("End of Game"):
        result = (game_status.split('|'))[1]
        WIN.blit(background_image, (0, 0))
        draw_end_game(result)
        pygame.display.update()
        return

    WIN.blit(background_image, (0, 0))
    draw_hand(game_status["hand"])
    draw_enemy_cards(game_status["enemy_num_cards"])
    draw_deck(game_status["deck_card"])
    draw_garbage(game_status["garbage_card"])
    draw_button(game_status)
    draw_turn(game_status)
    pygame.display.update()


def what_was_clicked(game_status: Game_status_type,
                     mouse_pos: Tuple[int, int]) -> Union[None, str]:
    """
    Returns a code representing the element that was clicked by the user_stuff
    """
    if game_status == "Game did not start yet":
        return None
    if isinstance(game_status, str) and game_status.startswith("End of Game"):
        return None

    # Check if clicked on one of the cards in the hand
    mouse_x, mouse_y = mouse_pos
    card_width, card_height = gui_helper.CARD_SIZE
    cards_location = gui_helper.hand_to_cards_location(game_status["hand"],
                                                       cards_images)

    for card_index, card_pos in enumerate(cards_location.values()):
        card_x, card_y = card_pos[1]
        if card_x <= mouse_x <= card_x + card_width and \
                card_y <= mouse_y <= card_y + card_height:
            return f"Hand|{card_index}"

    # Check if clicked on the deck
    deck_x, deck_y = gui_helper.DECK_LOCATION
    if deck_x <= mouse_x <= deck_x + card_width and \
            deck_y <= mouse_y <= deck_y + card_height:
        return "Deck"

    # Check if clicked on the garbage
    garbage_x, garbage_y = gui_helper.GARBAGE_LOCATION
    if garbage_x <= mouse_x <= garbage_x + card_width and \
            garbage_y <= mouse_y <= garbage_y + card_height:
        return "Garbage"

    # Check if clicked on Button
    button_x, button_y = gui_helper.BUTTON_LOCATION
    button_width, button_height = gui_helper.BUTTON_SIZE
    if button_x <= mouse_x <= button_x + button_width and \
            button_y <= mouse_y <= button_y + button_height:
        return "Button"
    return None


def main_loop() -> None:
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS)
        client.send(action[0])
        action[0] = "Get"
        game_status = client.receive_data()

        for event in pygame.event.get():  # All the events
            if event.type == pygame.QUIT:  # If exit window was clicked
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONUP:  # If mouse was clicked
                mouse_pos = pygame.mouse.get_pos()
                _clicked = what_was_clicked(game_status, mouse_pos)
                action[0] = _clicked if _clicked else "Get"

        draw_all(game_status)


if __name__ == '__main__':
    # Setup window
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.font.init()

    background_image = gui_helper.background_image
    # Dict with cards images
    cards_images = gui_helper.create_cards_image_dict()
    action = ["Get"]  # What to send the server (list for aliasing)

    # Client stuff
    client = Client()
    client.connect()

    main_loop()
    client.close()
