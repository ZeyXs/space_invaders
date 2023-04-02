all_enemy = self.enemies.sprites()
        for enemy in all_enemy:
            # Enemies movement
            if enemy.rect.right >= WIDTH:
                self.enemy_direction = -1
            elif enemy.rect.left < 2:
                self.enemy_direction = 1