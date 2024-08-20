import unittest
from directories import DirectoryCommandHandler, Directory


class TestDirectoryCommandHandler(unittest.TestCase):

    def setUp(self):
        """Set up the test directory structure"""
        self.handler = DirectoryCommandHandler()
        # setup  commands
        for entry in [
            "fruits",
            "vegetables",
            "grains",
            "fruits/apples",
            "fruits/apples/fuji",
            "grains/squash",
            "foods",
        ]:
            self.handler.handle_command(f"CREATE {entry}")

        # Manually create the expected directory structure
        root = Directory("root")
        fruits = Directory("fruits")
        fruits.parent = root
        vegetables = Directory("vegetables")
        vegetables.parent = root
        grains = Directory("grains")
        grains.parent = root
        apples = Directory("apples")
        apples.parent = fruits
        fuji = Directory("fuji")
        fuji.parent = apples
        squash = Directory("squash")
        squash.parent = grains
        foods = Directory("foods")
        root.children = {
            "fruits": fruits,
            "vegetables": vegetables,
            "grains": grains,
            "foods": foods,
        }
        fruits.children = {
            "apples": apples,
        }
        apples.children = {
            "fuji": fuji,
        }
        grains.children = {
            "squash": squash,
        }
        self.expected = root

    def tearDown(self):
        # Clean up any resources or state here
        self.handler = None
        self.expected = None

    def test_handle_command_create(self):
        """Test the CREATE command"""
        self.assertEqual(self.handler.root._list_dir(), self.expected._list_dir())

    def test_handle_command_move(self):
        """Test the MOVE command"""
        self.handler.handle_command("MOVE fruits foods")
        fruits = self.expected.children["fruits"]
        del self.expected.children["fruits"]
        foods = self.expected.children["foods"]
        foods.children["fruits"] = fruits
        fruits.parent = foods

        self.assertEqual(self.handler.root._list_dir(), self.expected._list_dir())

    def test_handle_command_delete(self):
        self.handler.handle_command("DELETE fruits/apples")
        fruits = self.expected.children["fruits"]
        del fruits.children["apples"]

        self.assertEqual(self.handler.root._list_dir(), self.expected._list_dir())

    def test_handle_command_list(self):
        self.assertEqual(self.handler.root._list_dir(), self.expected._list_dir())

    def test_handle_command_invalid(self):
        with self.assertRaises(Exception):
            self.handler.handle_command("Invalid command")

    def test_handle_command_create_existing(self):
        with self.assertRaises(Exception):
            self.handler.handle_command("CREATE fruits")

    def test_handle_command_move_nonexistent(self):
        with self.assertRaises(Exception):
            self.handler.handle_command("MOVE lentils vegetables")
        with self.assertRaises(Exception):
            self.handler.handle_command("MOVE vegetables lentils")

    def test_handle_command_delete_nonexistent(self):
        with self.assertRaises(Exception):
            self.handler.handle_command("DELETE fruits/oranges")


if __name__ == "__main__":
    unittest.main()
