# Вы можете расположить сценарий своей игры в этом файле.

# Определение персонажей игры.
define s = Character('Данил', color="#00fa9a")
define e = Character('Эвелина', color="#1dacd6")

# Игра начинается здесь:
label start:

    define points = 0

    scene black_bg

    "Все изображения не имеют авторского права и сгенерированны нейросетью Playground"

    scene castle_bottom with fade
    s "БЕЖИМ"

    scene sqwore_run_monster_bg with fade
    "Это Даня"
    "Прямо сейчас он бежит спасать свою сестру от ужасных монстров"

    menu:
        "Бежать прямо":
            "Справа появился огромный камень"
            s "Фух.... чуть не врезался"
        "Попробовать бежать направо":
            s "АЙ"
            "Даня врезался об неожиданно появившийся камень"
            "(Напоминание: Попробовать - не значит сделать удачно)"
            "Кстати это плохая концовка, вы проиграли"
            return

    scene castle_bottom with fade
    "На горизонте наконец появился пункт назначения..."
    show sqwore_angry_sprite with dissolve
    s "Вот он"
    s "Наконец..."
    s "Только куда идти...."

    menu:
        "Идти прямо":
            hide sqwore_angry_sprite
            scene castle_top with fade
            show sqwore happy sprite with dissolve
            s "Видимо верно"
            "Даня наступил на что-то и опустил голову"
            s "О зажигалка. Что она тут делает?"
            s "Ладно, лишней не будет"
            "Он положил зажигалку в карман и побежал дальше"
            hide sqwore happy sprite with dissolve
            $ points += 1
        "Итди налево":
            hide sqwore_angry_sprite
            scene black_bg with fade
            "Впереди был темный проход"
            show sqwore_angry_sprite with dissolve
            s "Ничего не вижу"
            hide sqwore_angry_sprite with dissolve
            "Спустя какое-то время..."
        "Идти направо":
            scene black_bg with fade
            s "АААААААААААААААААААААААААААААААААА"
            "Упс... попробуй другой вариант"
            return

    show black_bg with fade
    "Наконец из темноты появляется она"
    show eve happy sprite full with dissolve
    e "Привет братец!!" 
    e "Я тут в целом давно, но мне не страшно"
    e "Они не злые как нам рассказывали родители"
    hide eve happy sprite full with fade
    show eve_monsters3 with dissolve
    e "Тут на самом деле очень даже не плохо!"
    show sqwore_angry_sprite with dissolve
    s "Но дома нас ждет мама"
    hide sqwore_angry_sprite with dissolve
    e "хмммм"
    show eve happy sprite full with dissolve
    e "Ладно тогда давай возвращаться домой"
    hide eve_monsters3 with fade
    hide eve happy sprite full with fade
    show black_bg with dissolve
    "Посадите за ПК второго игрока"
    "После нажмите лкм"
    show eve happy spite top with fade
    e "Как же жаль что этот бедный малый не знает что это ложь"
    e "Моя цель оставить его тут навечно"
    e "Всего пара правильно нажатых кнопок и он будет тут навечно"
    e "Ой, каких еще кнопок я же не в игре"
    e "ХИХИ"
    hide eve happy spite top with fade
    scene black
    "Мини игра пин понг"
    jump demo_minigame_pong

    return
