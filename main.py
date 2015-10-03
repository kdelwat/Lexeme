import Library

def quit():
    sys.exit(0)

def main():
        commands = {"add": Library.add,
                    "list": Library.list,
                    "decline": Library.decline,
                    "query": Library.query,
                    "search": Library.search,
                    "generate": Library.generate,
                    "quit": quit}
        commandList = ""

        for key, value in commands.items():
                commandList = commandList + value.__name__ + ", "

        commandList = commandList[:-2] + "."
        print("Available commands: " + commandList)

        Library.loadData()

        command = input("Please enter a command: ")
        while command != "quit":
                commands[command]()
                command = input("Please enter a command: ")

if __name__ == '__main__':
        main()
