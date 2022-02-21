from game_stuff.deck import Deck
from game_stuff.hand import Hand
import pygame
from typing import Dict, List, Tuple

TITLE = "Balouka Card game"
WIDTH, HEIGHT = 1088, 612
FPS = 60

CARD_SIZE = (100, 140)
CARDS_PADDING = 30
PLAYER_CARDS_Y = HEIGHT - CARD_SIZE[1] - 30
ENEMY_CARDS_Y = 30
BUTTON_SIZE = (150, 66)
BUTTON_LOCATION = 30, HEIGHT - BUTTON_SIZE[1] - 30

FONT_SIZE = 45

GARBAGE_LOCATION = WIDTH // 2 - CARD_SIZE[0] // 2, HEIGHT // 2 - CARD_SIZE[
    1] // 2
DECK_LOCATION = WIDTH - CARDS_PADDING - CARD_SIZE[0], GARBAGE_LOCATION[1]

background_image = pygame.image.load('assets/small_background3.jpg')

BACK_CARD_IMAGE = pygame.image.load(r'assets/red_back3.png')
BACK_CARD_IMAGE = pygame.transform.scale(BACK_CARD_IMAGE, CARD_SIZE)

BUTTON_IMAGE = pygame.image.load(r'assets/button.png')
BUTTON_IMAGE = pygame.transform.scale(BUTTON_IMAGE, BUTTON_SIZE)

BUTTON_CLICKED_IMAGE = pygame.image.load(r'assets/buttonclicked.png')
BUTTON_CLICKED_IMAGE = pygame.transform.scale(BUTTON_CLICKED_IMAGE,
                                              BUTTON_SIZE)
image_type = type(pygame.image)


def create_cards_image_dict() -> Dict[str, image_type]:
    """
    :return: Dictionary with all the cards in the deck as keys (str(card)) and
    the matching imageType as value
    """
    card_images = {}
    deck = Deck()
    deck.initialize()
    for card in deck:
        _value, _type = card.value, card.type[0]
        path = "assets\\" + _value + _type + ".png"
        card_images[str(card)] = pygame.image.load(path)
        card_images[str(card)] = pygame.transform.scale(card_images[str(card)],
                                                        CARD_SIZE)
    return card_images


def hand_to_cards_location(hand: Hand, cards_images: Dict[str, image_type]) \
        -> Dict[str, Tuple[image_type, Tuple[int, int]]]:
    """
    Receive a hand and return a dictionary -
    key = str(card): value = tup(card_image, (x_loc, y_loc))
    """
    cards_locations = {}
    total_width = len(hand) * (CARD_SIZE[0] + CARDS_PADDING - 1)
    start_loc = (WIDTH - total_width) // 2
    for card in hand:
        cards_locations[str(card)] = cards_images[str(card)], (
            start_loc, PLAYER_CARDS_Y)
        start_loc += CARDS_PADDING + CARD_SIZE[0]
    return cards_locations


def enemy_cards_location(num_cards: int) -> \
        Tuple[image_type, List[Tuple[int, int]]]:
    """
    param num_cards: Num of enemy's cards
    :return: list of all the cards location
    """
    cards_locations = []
    total_width = num_cards * (CARD_SIZE[0] + CARDS_PADDING - 1)
    start_loc = (WIDTH - total_width) // 2
    for i in range(num_cards):
        location = start_loc, ENEMY_CARDS_Y
        cards_locations.append(location)
        start_loc += CARDS_PADDING + CARD_SIZE[0]
    return BACK_CARD_IMAGE, cards_locations


if __name__ == '__main__':
    print(pygame.font.get_fonts())
