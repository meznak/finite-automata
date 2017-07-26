import itertools
import xml.etree.ElementTree as ET

from automata import automata


def read_file(filename: str):
    try:
        fa = automata.PDA()
        if filename[-3:] == 'csv':
            with open(filename) as f:
                fa_type = f.readline().strip()
                sigma = f.readline().strip().split(',')
                if fa_type.upper() == "PDA":
                    gamma = f.readline().strip().split(',')
                else:
                    gamma = None
                states = f.readline().strip().split(',')
                start = f.readline().strip().split(',')
                final = f.readline().strip().split(',')
                delta = f.readlines()
                delta = [(s,d,a) for [s,d,a] in [trans.strip().split(',') for trans in delta]]
        elif filename[-3:] == 'jff' or filename[:-3] == 'xml':
            tree = ET.parse(filename)
            automaton = tree.find('automaton')

            fa.fa_type = tree.find('type').text
            if fa.fa_type.upper() == 'PDA':
                for s in automaton.findall('state'):
                    state = fa.add_state(int(s.attrib['id']), s.attrib['name'])
                    if s.find('initial') is not None:
                        fa.start = state
                    if s.find('final') is not None:
                        fa.final.append(state)

                for t in automaton.findall('transition'):
                    src = fa.get_state(id=int(t.find('from').text))
                    dest = fa.get_state(id=int(t.find('to').text))
                    read = t.find('read').text or u'ε'
                    pop = t.find('pop').text or u'ε'
                    push = t.find('push').text or u'ε'

                    fa.add_transition(src, dest, read, pop, push)

#        fa.verify()
        return fa
    except FileNotFoundError:
        print("Could not open file: " + filename)
        exit(2)

# TODO: add save function
#def save_file(fa, filename)
