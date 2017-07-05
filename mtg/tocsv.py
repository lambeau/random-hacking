import sys
import textwrap
import json

wrapper = textwrap.TextWrapper()
wrapper.width = 40
wrapper.initial_indent = '    '
wrapper.subsequent_indent = '      '

def main():
    f_name = sys.argv[1]
    with open(f_name) as f:
        cards = json.loads(f.read())
    #print(json.dumps(cards, indent=2))
    #print('\t'.join(['number', 'name', 'cost', 'type', 'text']))
    for number, card in [(number, card) for number, card in cards.items() if card['name'] not in ('Plains', 'Forest', 'Mountain', 'Swamp', 'Island')]:
        lines = []
        lines.append(''.join([number.ljust(4), card['name']]))
        if card['cost']:
            lines.append(wrapper.fill(card['cost']))
        lines.append(wrapper.fill(card['type']))
        if card['text']:
            lines.append('\n'.join(wrapper.fill(text_line) for text_line in card['text']))
        print('\n'.join(lines))
        print()
    #    print('\t'.join([number, card['name'], card['cost'], card['type'], ' | '.join(card['text'])]))


if __name__ == '__main__':
    main()
