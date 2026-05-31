APPLICATION_VERSION = '1.2.0'


class SystemOptions:
    def __init__(self, input_format='R20', output_format='R20V2', file_type='NPC', batch=False, action='None', path='', file=''):
        self.input_format = input_format
        self.output_format = output_format
        self.file_type = file_type
        self.batch = batch
        self.action = action
        self.path = path
        self.file = file

    def load_from_args(self, args):
        self.set_input_format(args.input)
        self.set_output_format(args.output)
        self.set_type(args.type)
        self.set_batch(args.batch)
        self.set_action(args.action)
        self.set_path(args.path)
        self.set_file(args.file)


    def set_input_format(self, input_format):
        self.input_format = input_format

    def get_input_format(self):
        return self.input_format

    def is_hero(self):
        return self.input_format =='Hero'

    def is_xml(self):
        return self.input_format == 'XML'

    def is_R20(self):
        return self.input_format == 'R20'

    def is_JSON(self):
        return self.input_format == 'JSON'

    def set_output_format(self, output_format):
        self.output_format = output_format

    def get_output_format(self):
        return self.output_format

    def do_r20_v1(self):
        return self.output_format == 'V1'

    def do_r20_v2(self):
        return self.output_format == 'V2'

    def set_type(self, file_type):
        self.file_type = file_type

    def get_type(self):
        return self.file_type

    def set_path(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def set_batch(self, batch):
        self.batch = batch

    def is_batch(self):
        return self.batch

    def set_action(self, action):
        self.action = action

    def get_action(self):
        return self.action

    def do_export(self):
        return self.action == 'export' or self.action == 'both'

    def do_save(self):
        return self.action == 'save' or self.action == 'both'

    def set_file(self, file):
        self.file = file

    def get_file(self):
        return self.file

    def has_file(self):
        return len(self.file) > 0 if self.file else False