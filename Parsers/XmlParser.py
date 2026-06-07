import json
import xmltodict
from Parsers.JsonParser import CreatureJsonParser
from Database.models import Creature


class CreatureXmlParser:
    def __init__(self, xml_input, options):
        self.creature = None
        self.input_xml = xml_input.replace("–", "-").replace("×", "x").replace("°", " degrees")
        self.options = options

    def run(self):
        # 2. Parse XML string to a Python dictionary
        data_dict = xmltodict.parse(self.input_xml)

        # 3. Convert the dictionary into a JSON string/object
        json_data = json.dumps(data_dict, indent=4)

        parser = CreatureJsonParser(json_data, self.options)
        parser.run()
        self.creature = parser.creature
