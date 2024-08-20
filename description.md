# Directory tree problem

A common method of organizing files on a computer is to store them in hierarchical directories. For instance:

```

photos/

  birthdays/

    joe/

    mary/

  vacations/

  weddings/

```

In this challenge, you will implement commands that allow a user to create, move and delete directories.

A successful solution will take the following input:

```

CREATE fruits

CREATE vegetables

CREATE grains

CREATE fruits/apples

CREATE fruits/apples/fuji

LIST

CREATE grains/squash

MOVE grains/squash vegetables

CREATE foods

MOVE grains foods

MOVE fruits foods

MOVE vegetables foods

LIST

DELETE fruits/apples

DELETE foods/fruits/apples

LIST

```


and produce the following output


```

CREATE fruits

CREATE vegetables

CREATE grains

CREATE fruits/apples

CREATE fruits/apples/fuji

LIST

fruits

  apples

    fuji

grains

vegetables

CREATE grains/squash

MOVE grains/squash vegetables

CREATE foods

MOVE grains foods

MOVE fruits foods

MOVE vegetables foods

LIST

foods

  fruits

    apples

      fuji

  grains

  vegetables

    squash

DELETE fruits/apples

Cannot delete fruits/apples - fruits does not exist

DELETE foods/fruits/apples

LIST

foods

  fruits

  grains

  vegetables

    squash

```

## Helpful hints

Please solve the challenge on your own and without using any helper libraries as this would not show us the skillset we are interested in.
Your solution should not actually create folders on the host machine.
Your solution should take the above input and produce exactly the output shown above.