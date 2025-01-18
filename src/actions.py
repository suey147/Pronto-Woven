class Actions:
    def rent(self, player, landed_property, board):
        if landed_property.is_owned():
            rent = landed_property.get_rent()
            owner = landed_property.get_owner()
            property_set = board.get_property_set(landed_property.get_colour())
            if all(p.get_owner() == owner for p in property_set):
                rent *= 2
            owner.receive(rent)
            player.pay(rent)
            return f"{player.name} pays ${rent} rent to {owner.name}."
        return ""
    def buy_property(self, player, landed_property):
        if not landed_property.is_owned():
            player.buy_property(landed_property)
            landed_property.set_owner(player)
            return f"{player.name} buys {landed_property.name} for ${landed_property.get_price()}."
        return ""
    def pass_go(self, player, steps, board_length):
        if player.check_pass_go(steps, board_length):
            player.receive(1)
            return f"{player.name} passes GO and earns $1!"
        return ""