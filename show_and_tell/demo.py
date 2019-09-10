import argparse
import subprocess

import yaml

# XXX - generate markdown from demo

class Demo:
    INPUT_VALUES = {}

    def do_input(self, cmd, command_type, arg_notes, use_as_input, store_input_name):
        # XXX - add support for input values, or other conditions
        if command_type is not None and command_type.lower() == 'input':
            arg_msg = ''
            if arg_notes is not None:
                arg_msg = " {} ".format(arg_notes)
            if use_as_input is None:
                the_arg_input = input(arg_msg)
            else:
                the_arg_input = self.INPUT_VALUES.get(use_as_input)

            if use_as_input is not None and '{'+use_as_input+'}' in cmd:
                cmd = cmd.format(**{use_as_input: the_arg_input})
            else:
                cmd = "{} {}".format(cmd, the_arg_input)
            if store_input_name is not None:
                self.INPUT_VALUES[store_input_name] = the_arg_input
        return cmd

    def do_command(self, cmd, prompt=True, prompt_value="",
                   use_as_input=None, store_input_name=None,
                   command_type=None, arg_notes=None, shell=True):
        if prompt:
            the_input = input("{} \n `{}` (Execute Y/n?) ".format(prompt_value, cmd))
            cmd = self.do_input(cmd, command_type, arg_notes, use_as_input, store_input_name)
            if the_input.lower() in ['', 'y', 'yes']:
                print("Running {}".format(cmd))
                subprocess.run(cmd, shell=shell)
            else:
                print('Skipped {}\n'.format(cmd))

    def do_demo(self, demo):
        for part in demo.get('parts', []):
            print("\n {} \n".format(part['name']))
            print("\n {} \n".format(part['intro']))
            for step in part.get('steps', []):
                caption = step.get('cap', step.get('caption'))
                print(caption)
                command = step.get('com', step.get('communication'))
                command_type = step.get('type')
                # XXX - come up with a better name
                arg_notes = step.get('notes')
                if command is not None:
                    use_as_input = step.get('use')
                    store_input_name = step.get('store')
                    self.do_command(command, use_as_input=use_as_input,
                                    store_input_name=store_input_name,
                                    command_type=command_type, arg_notes=arg_notes)

    def run(self, demo_files):
        for demo_file in demo_files:
            with open(demo_file) as f:
                self.do_demo(yaml.load(f, Loader=yaml.FullLoader))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run an interactive document')
    parser.add_argument('files', type=str, nargs='+',
                        help="The yaml files containing the document steps")
    args = parser.parse_args()

    demo = Demo()
    demo.run(args.files)

