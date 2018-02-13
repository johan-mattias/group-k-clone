class ServerGame():
    def __init__(self):
        self.players = list()

    def remove_player(self, player_to):
        self.players.remove(self.players[player_to.player_id])

    def add_player(self, user_id, name):
        new_id = len(self.players)
        new_player = Player(new_id, user_id, name, 0, 0)
        self.players.append(new_player)
        return new_id

class Player():
    def __init__(self, player_id, user_id, name, x, y):
        self.player_id = player_id
        self.user_id = user_id
        self.name = name
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return "player_id: " + str(self.player_id) + " user_id: " + str(self.user_id) + " name: " + str(self.name) +  " x: " + str(self.x) + " y: " + str(self.y)
