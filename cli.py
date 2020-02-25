import yaml
import json


class Command:
    def __init__(self, command, description):
        self.command = command
        self.description = description

    def make(self, name, description, **kwargs):
        command = list()
        command.append("@bot.command")
        command.append("async def %s(ctx, *args):" % self.command)
        command.append("\tawait ctx.send(args)")
        return "\n".join(command)


class CommandBuilder:
    @staticmethod
    def yaml_to_json(file):
        return yaml.load(file)

    @staticmethod
    def retrieve_file(self):
        data = str()
        with open('commands/commands.yml') as file:
            for line in file:
                data += line
        return data

    def load_command(self):
        print()
        return Command()
