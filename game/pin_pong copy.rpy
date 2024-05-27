init:

    image bg pong field = "images/pin_pong/pong_field.png"

    python:

        class PongDisplayable(renpy.Displayable):

            def __init__(self):

                renpy.Displayable.__init__(self)

                # Некоторые таблицы отображения, которые мы используем.
                self.paddle = Image("images/pin_pong/pong.png")
                self.ball = Image("images/pin_pong/pong_ball.png")
                self.player = Text(_("Эвелина"), size=48)
                self.eileen = Text(_("Бот"), size=48)
                self.ctb = Text(_("FIGHT"), size=48, color="000000")

                # Размеры некоторых изображений
                self.PADDLE_WIDTH = 16
                self.PADDLE_HEIGHT = 180
                self.BALL_WIDTH = 30
                self.BALL_HEIGHT = 30
                self.COURT_TOP = 200
                self.COURT_BOTTOM = 950

                # Если мяч застрял в весло.
                self.stuck = True

                # Позиции двух затворов.
                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                # Скорость компьютера.
                self.computerspeed = 700.0

# Положение, дентал-положение и скорость# мяч.
                self.bx = 88
                self.by = self.playery
                self.bdx = .5
                self.bdy = .5
                self.bspeed = 800.0

                # Время прошлого рендера кадра.
                self.oldst = None

                #победитель.
                self.winner = None

            def visit(self):
                return [ self.paddle, self.ball, self.player, self.eileen, self.ctb ]

# Пересчитывает положение мяча, ручками отбивается, и
# рисует на экране.
            def render(self, width, height, st, at):

                # Объект отображения, мы будем рисовать в.
                r = renpy.Render(width, height)

                # Выяснить время, прошедшее с предыдущего кадра.
                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                #Выяснить, где мы хотим, чтобы переместить мяч.
                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                # Переместить весло компьютера. Он хочет пойти в self.by но
                # может быть ограничена ограничить его скорость.
                cspeed = self.computerspeed * dtime
                if abs(self.by - self.computery) <= cspeed:
                    self.computery = self.by
                else:
                    self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

                # Отскакивают от верхней.
                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy

                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy

                # Это берет весло, и проверяет отскакивает.
                def paddle(px, py, hotside):

                    pi = renpy.render(self.paddle, 1920, 1080, st, at)

                    r.blit(pi, (int(px), int(py - self.PADDLE_HEIGHT / 2)))

                    if py - self.PADDLE_HEIGHT / 2 <= self.by <= py + self.PADDLE_HEIGHT / 2:

                        hit = False

                        if oldbx >= hotside >= self.bx:
                            self.bx = hotside + (hotside - self.bx)
                            self.bdx = -self.bdx
                            hit = True

                        elif oldbx <= hotside <= self.bx:
                            self.bx = hotside - (self.bx - hotside)
                            self.bdx = -self.bdx
                            hit = True

                        if hit:
                            self.bspeed *= 1.10

                # Нарисуйте два весла.
                paddle(286, self.playery, 286 + self.PADDLE_WIDTH)
                paddle(1600, self.computery, 1600)

            # Розыгрыш мяча.
                ball = renpy.render(self.ball, 1920, 1080, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                            int(self.by - self.BALL_HEIGHT / 2)))

                # Показать имена игроков.
                player = renpy.render(self.player, 1920, 1080, st, at)
                r.blit(player, (230, 65))

                # Имя Айлин.
                eileen = renpy.render(self.eileen, 1920, 1080, st, at)
                ew, eh = eileen.get_size()
                r.blit(eileen, (1610 - ew, 65))

                # Показать "Нажмите, чтобы начать" метки.
                if self.stuck:
                    ctb = renpy.render(self.ctb, 1920, 1080, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, (960 - cw / 2, 54))



                if self.bx < -200:
                    self.winner = "Бот"


                    renpy.timeout(0)

                elif self.bx > 2000:
                    self.winner = "Эвелина"
                    renpy.timeout(0)


                renpy.redraw(self, 0)

                # Return the Render object.
                return r

            # Обрабатывает события.
            def event(self, ev, x, y, st):

                import pygame

                # # Выбирете вниз == начать игру, установив застрял
# ложные.
                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                # Установить положение ракетки игрока
                y = max(y, self.COURT_TOP, 300)
                y = min(y, self.COURT_BOTTOM, 870)
                self.playery = y


                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()


label pong:

    window hide None

    # Put up the pong background, in the usual fashion.
    scene bg pong field

    # Run the pong minigame, and determine the winner.
    python:
        ui.add(PongDisplayable())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)

    scene black

    window show None


    if winner == "Бот":
        scene castle_top with fade
        show eve happy sprite full with dissolve
        e "Я выиграла! АХАХАХХАХАХАХАХ"
        e "Теперь ты не сможешь от сюда сбежать"
        pass
    else:
        jump pong_p2


