init:

    image bg pong field = "images/pin_pong/pong_field.png"

    python:

        class PongDisplayable1(renpy.Displayable):
        #Отличие от прошлого в финале и именах, в целом тут тоже самое, по этому не дублирую комментарии где уже писал

            def __init__(self):

                renpy.Displayable.__init__(self)

                self.paddle = Image("images/pin_pong/pong.png")
                self.ball = Image("images/pin_pong/pong_ball.png")
                self.player = Text(_("Даня"), size=48)
                self.eileen = Text(_("Бот"), size=48)
                self.ctb = Text(_("FIGHT"), size=48, color="000000")

                self.PADDLE_WIDTH = 16
                self.PADDLE_HEIGHT = 180
                self.BALL_WIDTH = 30
                self.BALL_HEIGHT = 30
                self.COURT_TOP = 200
                self.COURT_BOTTOM = 950

                self.stuck = True

                self.playery = (self.COURT_BOTTOM - self.COURT_TOP) / 2
                self.computery = self.playery

                self.computerspeed = 700.0

                self.bx = 88
                self.by = self.playery
                self.bdx = .5
                self.bdy = .5
                self.bspeed = 800.0

                self.oldst = None

                self.winner = None

            def visit(self):
                return [ self.paddle, self.ball, self.player, self.eileen, self.ctb ]

            def render(self, width, height, st, at):

                r = renpy.Render(width, height)

                if self.oldst is None:
                    self.oldst = st

                dtime = st - self.oldst
                self.oldst = st

                speed = dtime * self.bspeed
                oldbx = self.bx

                if self.stuck:
                    self.by = self.playery
                else:
                    self.bx += self.bdx * speed
                    self.by += self.bdy * speed

                cspeed = self.computerspeed * dtime
                if abs(self.by - self.computery) <= cspeed:
                    self.computery = self.by
                else:
                    self.computery += cspeed * (self.by - self.computery) / abs(self.by - self.computery)

                ball_top = self.COURT_TOP + self.BALL_HEIGHT / 2
                if self.by < ball_top:
                    self.by = ball_top + (ball_top - self.by)
                    self.bdy = -self.bdy

                ball_bot = self.COURT_BOTTOM - self.BALL_HEIGHT / 2
                if self.by > ball_bot:
                    self.by = ball_bot - (self.by - ball_bot)
                    self.bdy = -self.bdy

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

                paddle(286, self.playery, 286 + self.PADDLE_WIDTH)
                paddle(1600, self.computery, 1600)

                ball = renpy.render(self.ball, 1920, 1080, st, at)
                r.blit(ball, (int(self.bx - self.BALL_WIDTH / 2),
                            int(self.by - self.BALL_HEIGHT / 2)))

                player = renpy.render(self.player, 1920, 1080, st, at)
                r.blit(player, (260, 65))

                eileen = renpy.render(self.eileen, 1920, 1080, st, at)
                ew, eh = eileen.get_size()
                r.blit(eileen, (1610 - ew, 65))

                if self.stuck:
                    ctb = renpy.render(self.ctb, 1920, 1080, st, at)
                    cw, ch = ctb.get_size()
                    r.blit(ctb, (960 - cw / 2, 54))



                if self.bx < -200:
                    self.winner = "Бот"


                    renpy.timeout(0)

                elif self.bx > 2000:
                    self.winner = "Даня"
                    renpy.timeout(0)


                renpy.redraw(self, 0)

                return r

            def event(self, ev, x, y, st):

                import pygame

                if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    self.stuck = False

                y = max(y, self.COURT_TOP, 300)
                y = min(y, self.COURT_BOTTOM, 870)
                self.playery = y


                if self.winner:
                    return self.winner
                else:
                    raise renpy.IgnoreEvent()


label pong_p2:

    window hide None

    scene bg pong field

    python:
        ui.add(PongDisplayable1())
        winner = ui.interact(suppress_overlay=True, suppress_underlay=True)

    scene black

    window show None


    if winner == "Бот":
        # Если выиграл бот то плохая концовка
        scene castle_top with fade
        show eve happy sprite full with dissolve
        e "Я выиграла! АХАХАХХАХАХАХАХ"
        e "Теперь ты не сможешь от сюда сбежать"
        pass
    else:
        # При победе первого игрока хорошая концовка
        scene white_bg
        show eve_sad_top with dissolve
        e "НЕЕЕЕЕЕЕТ"
        hide eve_sad_top
        show eve_sad with dissolve
        e "ТЫ НЕ ДОЛЖЕН БЫЛ ЭТО СДЕЛАТЬ"
        hide eve_sad with dissolve
        "Кажется тебе удалось спастись..."
        s "Стоп что"
        s "Почему тут звук будильника???"
        scene sqwore_room
        s "?????????????"
        show sqwore_angry_sprite with fade
        s "В чем дело???"
        hide sqwore_angry_sprite with fade
        "Ты оказался в своей кровати"
        show sqwore happy sprite with dissolve
        s "Так это был сон?"
        "Это был сон"
        "Эвелина была дома и спала в своей комнате"
        scene white_bg
        "Поставте оценку пж" #финал
        pass


