import minimax
import gamestate
import time

import config as cfg

from client import ClientSocket
from argparse import ArgumentParser
            
def play_game(strategy, args):
    client_socket = ClientSocket(args.ip, args.port)
    client_socket.send_nme(args.name)

    # getting map limits
    [y_limit, x_limit] = client_socket.get_message()[1]

    # hum message : coordonnées des maisons (humains) - useless
    _ = client_socket.get_message()
    # hme message
    hme_info = client_socket.get_message()
    # map message
    map_info = client_socket.get_message()

    # updating the state with initial information
    state = gamestate.GAME_STATE(x_limit, y_limit)
    state.map_treatment(hme_info, map_info)

    # SETUP DES VAR GLOBALES
    cfg.X_LIM, cfg.Y_LIM = state.getLimits()
    cfg.IDX_US, cfg.IDX_EN = state.getIdx()


    # start of the game
    while True:
        message = client_socket.get_message()

        if message[0] == "upd":
            state.update_treatment(message)

            if len(state.us) == 1:
                cfg.N_GROUPS = 1

            best, moves = minimax.run_minimax(state)

            if len(moves) == 5:
                client_socket.send_mov(1, [moves])

            else:
                client_socket.send_mov(len(moves), moves)

            minimax.DEBUG = False

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument(dest='name', default='name', type=str, help='name of your AI')
    parser.add_argument(dest='ip', default='localhost', type=str, help='IP adress the connection should be made to.')
    parser.add_argument(dest='port', default='5555', type=int, help='Chosen port for the connection.')

    args = parser.parse_args()
    
    play_game(None, args)

    