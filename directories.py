"""
directories.py

This file implements the following classes:

- NaryTree: A class that implements a n-ary tree
- DirectoryNameValidatorMixin: A mixin class that validates the directory name
- Directory: A class that represents a directory in the tree.
  It inherits from NaryTree and DirectoryNameValidatorMixin
- DirectoryCommandHandler: A class that handles the commands

"""

COMMANDS = ["CREATE", "MOVE", "DELETE", "LIST"]

ROOT_NAME = "/"

PROMPT = "> "


class NaryTree:
    """NaryTree class implements a n-ary tree"""

    def __init__(self, name):
        """constructor"""
        self.name = name
        self.children: dict[str, "NaryTree"] = dict()
        self.parent: "NaryTree" | None = None

    def _create_instance(self, name: str) -> None:
        """Initialize the class"""
        return NaryTree(name)

    def _validate_name(self, name: str) -> None:
        """Validate"""
        pass

    def _create_child(self, name: str) -> None:
        """Create a child node to the current node"""
        self._validate_name(name)
        if name not in self.children:
            child = self._create_instance(name)
            self.children[name] = child
            child.parent = self

    def _add_child(self, node: "NaryTree") -> None:
        """Add a subtree to the current node"""
        if node.name in self.children:
            raise Exception(f"{node.name} already exists in {self.name}")
        self.children[node.name] = node
        node.parent = self

    def _remove_child(self, name: str) -> None:
        """Remove a child from the current node"""
        if name not in self.children:
            raise Exception(f"{name} does not exist")
        child = self.children[name]
        del self.children[name]
        child.parent = None


class DirectoryNameValidatorMixin:
    """Directory name validator mixin"""

    @staticmethod
    def _validate_name(name: str) -> None:
        """Validate the child directory name before adding it"""
        if name == "/" or name.strip() == "":
            raise Exception("Invalid directory name")


class Directory(DirectoryNameValidatorMixin, NaryTree):
    """Directory class to represent a directory in the tree"""

    def __init__(self, name: str = ROOT_NAME):
        """Constructor"""
        super().__init__(name)

    def _create_instance(self, name: str) -> None:
        """Initializes the class"""
        return Directory(name)

    def create(self, path: str):
        """Creates a directory"""
        parts = path.split("/")
        current_dir = self
        for i, part in enumerate(parts, 1):
            if part not in current_dir.children:
                current_dir._create_child(part)
            elif i == len(parts):
                raise Exception(f"{part} already exists")
            current_dir = current_dir.children[part]

    def delete(self, path: str):
        """Deletes a directory"""
        parts = path.split("/")
        current_dir = self
        for part in parts:
            if part not in current_dir.children:
                raise Exception(f"{part} does not exist")
            current_dir = current_dir.children[part]
        current_dir.parent._remove_child(current_dir.name)

    def move(self, source_path: str, destination_path: str):
        """Moves a directory"""
        if source_path == destination_path:
            return
        # Find the source directory to move
        parts = source_path.split("/")
        current_dir = self
        for part in parts:
            if part not in current_dir.children:
                raise Exception(f"{part} does not exist")
            current_dir = current_dir.children[part]
        destination_parts = destination_path.split("/")
        destination = self
        # Find the destination directory
        for part in destination_parts:
            if part not in destination.children:
                raise Exception(f"{part} does not exist")
            destination = destination.children[part]
        # Delete the directory from the current parent and add it to the new destination
        current_dir.parent._remove_child(current_dir.name)
        destination._add_child(current_dir)
        current_dir.parent = destination

    def _list_dir(self) -> str:
        """Lists the directories"""
        output = []
        # Do the dfs to print the current directory
        stack = []
        stack.append((self, -1))
        while stack:
            directory, level = stack.pop()
            if level >= 0:
                output.append("  " * level + directory.name)
            for child in directory.children:
                stack.append((directory.children[child], level + 1))
        return "\n".join(output)

    def list_dir(self) -> None:
        """Lists the directories"""
        print(self._list_dir())

    def __repr__(self):
        return self.name


class DirectoryCommandHandler:
    """Directory command handler handles the commands"""

    def __init__(self):
        """Constructor"""
        self.root = Directory(name=ROOT_NAME)

    def handle_command(self, command: str):
        """handle the command"""
        command = command.strip()
        parts = command.split(" ")
        command = parts[0].upper()  # supports both upper and lower case commands
        params = parts[1:]
        if command not in COMMANDS:
            raise Exception("Invalid command")
        if command == "CREATE":
            assert len(parts) == 2, "Invalid parameters"
            self.root.create(parts[1])
        elif command == "DELETE":
            assert len(parts) == 2, "Invalid parameters"
            self.root.delete(parts[1])
        elif command == "MOVE":
            assert len(parts) == 3, "{parts} Invalid parameters"
            self.root.move(parts[1], parts[2])
        elif command == "LIST":
            self.root.list_dir()


def main():
    handler = DirectoryCommandHandler()
    while True:
        command = input(f"\n{PROMPT}")
        if command == "exit":
            break
        try:
            handler.handle_command(command)
        except Exception as e:
            print(f"Cannot execute '{command}' - {e}")


if __name__ == "__main__":
    main()
