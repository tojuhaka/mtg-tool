#!/usr/bin/env python
import optparse


def _enum(**enums):
    # Used to make life easier with indexes
    return type('Enum', (), enums)

CARDINFO = _enum(NAME=0, COLOR=1, VALUE=2, COUNT=3, EXTRA=4)

# u = blue, b = black, r = red, g = green, w = white
# m = multicolor, a = artifact, c = colorless
cards = {}

color_graph = {'u': 'Blue', 'b': 'Black', 'g': 'Green', 'w': 'White',
               'm': 'Multicolor', 'a': 'Artifact', 'c': 'Colorless'}


def add_card(card_tuple):
    name, color, value, count, extra = card_tuple
    #sort by color
    if color in cards:
        if not card_tuple in cards[color]:
            cards[color].append(card_tuple)
        else:
            print "duplicate card: %s" % name
    else:
        cards[color] = [card_tuple]


def render(output_file):
    f = open(output_file, 'w')
    for color in cards:
        f.write(color_graph[color] + '\n')
        cards[color] = sorted(
            cards[color], key=lambda card: card[CARDINFO.VALUE], reverse=True)
        for card in cards[color]:
            f.write("%sx [card]%s[/card] (%s)\n"
                    % (card[CARDINFO.COUNT],
                       card[CARDINFO.NAME],
                       card[CARDINFO.EXTRA]))
        f.write('\n')


def load(filename):
    # Load the file containing cards and store them inside dict
    f = open(filename, 'r')
    card_list = f.readlines()
    for card in card_list:
        # convert line to tuple and get the values
        # remove the last two characters: \n
        card = card.lower()[:-1]
        card_tuple = tuple(card.lower().split('|'))
        try:
            add_card(card_tuple)
        except ValueError, e:
            print "Error in " + cards
            print e


def main():
    p = optparse.OptionParser()
    p.add_option('--input', '-i', default="input.txt")
    p.add_option('--output', '-o', default="output.txt")
    options, arguments = p.parse_args()

    # load cards from file
    load(options.input)
    render(options.output)

if __name__ == '__main__':
    main()
