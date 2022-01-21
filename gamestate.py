class GAME_STATE():
    """
    The goal of this class is updating the game states
    i.e. the human, us, and enemy dictionary
    which is then used in the alpha-beta algorithm
    """

    def __init__(self, x_limit, y_limit):
        """
        :param x_limit: map limit on the x axis
        :param y_limit: map limit on the y axis
        """
        self.human = {}
        self.us = {}
        self.enemy = {}

        self.y_limit = y_limit
        self.x_limit = x_limit

    def hme_treatment(self, info):

        """
        :param info: message from the server
        :return: return initial position
        """

        init_x = info[1][0]
        init_y = info[1][1]
        return init_x, init_y

    def map_treatment(self, info_hme, info_map):

        """
        :param info_hme: message from the server regarding inital position
        :param info_map: message from the server regarding the map layout

        Setting up the index that refers to our mobs i.e. vampires are
        always the 3rd number and werewolves the 4th number in the update
        messages. This avoids if statements when checking the UPD message.
        """

        init_x = info_hme[1][0]
        init_y = info_hme[1][1]

        # setting our idx and the enemy's to instantly access the update

        for mob in info_map[1]:
            x, y, nh, nv, nw = mob

            if x == init_x and y == init_y:
                if nv != 0:
                    self.idxUs = 3
                    self.idxEn = 4

                else:
                    self.idxUs = 4
                    self.idxEn = 3

        # filling the dictionaries
        for mob in info_map[1]:

            x, y, nh, nv, nw = mob

            if nh != 0:  # humain
                self.human[(x, y)] = nh

            elif mob[self.idxUs] != 0:  # us
                self.us[(x, y)] = mob[self.idxUs]

            else:  # enemy
                self.enemy[(x, y)] = mob[self.idxEn]

    def update_treatment(self, info):

        for mob in info[1]:

            x, y, nh, nv, nw = mob

            if nh != 0:
                self.human[(x, y)] = nh

            elif mob[self.idxUs] != 0:
                self.us[(x, y)] = mob[self.idxUs]

                if (x, y) in self.human:
                    del self.human[(x, y)]

                if (x, y) in self.enemy:
                    del self.enemy[(x, y)]


            elif mob[self.idxEn] != 0:
                self.enemy[(x, y)] = mob[self.idxEn]

                if (x, y) in self.human:
                    del self.human[(x, y)]

                if (x, y) in self.us:
                    del self.us[(x, y)]

            else:

                # deleting if no one in the cell
                if (x, y) in self.human:
                    del self.human[(x, y)]

                if (x, y) in self.us:
                    del self.us[(x, y)]

                if (x, y) in self.enemy:
                    del self.enemy[(x, y)]

    def getState(self):
        return (self.us, self.enemy, self.human)

    def getIdx(self):
        return self.idxUs, self.idxEn

    def getLimits(self):
        return self.x_limit, self.y_limit