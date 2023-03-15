rang = 0
        for y in range(40, HEIGHT-130, 15):
            for x in range(25, WIDTH-30, 15):
                if rang==0:
                    self.enemies.append(Meduse(x+1.9, y))
                elif rang<=2:
                    self.enemies.append(Crabe(x+0.5, y))
                elif rang<=4:
                    self.enemies.append(Poulpe(x, y))
            rang+=1