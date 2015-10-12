import cmd
import argparse
from Interface import *


class Lexeme(cmd.Cmd):
    intro = "Welcome to Lexeme! Input '?' for help and commands."
    prompt = "\nEnter command: "

    def do_list(self, arg):
        clearScreen()
        listwords()

    def do_quit(self, arg):
        quit()

    def do_add(self, arg):
        clearScreen()
        add()

    def do_decline(self, arg):
        clearScreen()
        decline()

    def do_statistics(self, arg):
        clearScreen()
        statistics()

    def do_search(self, arg):
        clearScreen()
        search()

    def do_generate(self, arg):
        clearScreen()
        generate()

    def do_export(self, arg):
        clearScreen()
        export()

    def do_batch(self, arg):
        clearScreen()
        batchgenerate()

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

    clearScreen()

    Lexeme().cmdloop()
