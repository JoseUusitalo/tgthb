from attack import attack
from buy import buy
from call import call
from drop import drop
from examine import examine
from give import give
from greet import greet
from helpcmd import helpcmd   # "help" was a reserved name.
from inventory import inventory
from load import load
from look import look
from movement import north, northeast, east, southeast, south, southwest, west, northwest, up, down, move
from quitgame import quitgame  # "quit" was a reserved name.
from rent import rent
from restart import restart
from save import save
from say import say
from shoot import shoot
from take import take
from talk import talk
from tips import tips
from travel import travel
from use import use


def test(x="No argument given."):
    print("Function: test | Argument:",x)

# This acts as central file to point to all the game commands.