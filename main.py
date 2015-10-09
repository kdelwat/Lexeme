import cmd
from Interface import *


class Lexeme(cmd.Cmd):
    intro = "Welcome to Lexeme. Input ? for help and commands"
    prompt = "(lexeme) "

    def do_list(self, arg):
        'List word database.'
        listwords()

    def do_quit(self, arg):
        quit()

    def do_add(self, arg):
        add()

    def do_decline(self, arg):
        decline()

    def do_statistics(self, arg):
        statistics()

    def do_search(self, arg):
        search()

    def do_generate():
        generate()

    def do_export():
        export()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", help="set database file")
    parser.add_argument("--config", help="set configuration file")
    args = parser.parse_args()

    if args.database is not None:
        Library.loadDatabase(args.database)

    else:
        Library.loadDatabase()

    if args.config is not None:
        loadData(args.config)
    else:
        loadData()

    Lexeme().cmdloop()
