import json
import xmltodict


class CreatureXmlParser:
    def __init__(self, xml_input, options):
        self.creature = Creature()
        self.creature.formal_name = ''
        self.creature.space = '5 ft.'
        self.creature.reach = '5 ft.'
        self.gear_item = None
        self.special_ability = None
        self.input_xml = xml_input.replace("–", "-").replace("×", "x").replace("°", " degrees")
        self.options = options

    def run(self):

        print(self.creature)