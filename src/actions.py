class Actions:
    """
    This class defines the actions a player can take during their turn in the game,
    such as paying rent, buying properties, and passing GO.
    """
    def rent(self, player, landed_property, board):
        """
        Handles the rent payment when a player lands on a property that is owned by another player.
        
        Args:
            player (Player): The player who landed on the property and must pay rent.
            landed_property (Property): The property the player landed on.
            board (Board): The game board, used to retrieve property sets and verify ownership.

        Returns:
            str: A message detailing the rent transaction, or an empty string if no rent is due.
        
        Notes:
            If the player lands on a property that is owned by another player, they must pay rent.
            If the owner has a complete set of properties (all properties of the same color), the rent is doubled.
        """
        if landed_property.is_owned():  #check if the property is owned
            rent = landed_property.get_rent()   # Get the standard rent for the property
            owner = landed_property.get_owner() # Get the owner of the property
            property_set = board.get_property_set(landed_property.get_colour()) # Get all properties of the same color
            # Double the rent if the owner has all properties of the same color
            if all(p.get_owner() == owner for p in property_set):
                rent *= 2
             # Perform the transaction
            owner.receive(rent)
            player.pay(rent)
            # Return a message detailing the transaction
            return f"{player.name} pays ${rent} rent to {owner.name}."
        return ""
    def buy_property(self, player, landed_property):
        """
        Handles the purchase of a property by a player if the property is not owned.
        
        Args:
            player (Player): The player who wants to buy the property.
            landed_property (Property): The property the player wants to purchase.
        
        Returns:
            str: A message detailing the property purchase, or an empty string if the property is already owned.
        
        Notes:
            If the property is not owned by anyone, the player can buy it. After buying, the property’s ownership
            is transferred to the player.
        """
        if not landed_property.is_owned():  # Check if the property is not owned
            player.buy_property(landed_property)     # Player buys the property
            landed_property.set_owner(player)   # Set the player's ownership of the property
             # Return a message detailing the purchase
            return f"{player.name} buys {landed_property.name} for ${landed_property.get_price()}."
        return ""
    def pass_go(self, player, steps, board_length):
        """
        Handles the event when a player passes the 'GO' space on the board.
        
        Args:
            player (Player): The player who may pass the 'GO' space.
            steps (int): The number of steps the player has moved (based on dice roll).
            board_length (int): The total number of spaces on the board.
        
        Returns:
            str: A message detailing the action of passing GO and earning $1, or an empty string if the player did not pass GO.
        
        Notes:
            If the player moves beyond the 'GO' space, they earn $1.
        """
        if player.check_pass_go(steps, board_length):   # Check if the player has passed GO
            player.receive(1)   # Player earns $1 for passing GO
            return f"{player.name} passes GO and earns $1!"
        return ""