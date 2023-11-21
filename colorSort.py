from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

POSSIBLE_COLORS = [Color.RED, Color.GREEN, Color.BLUE, Color.YELLOW]

ev3 = EV3Brick()

belt_motor = Motor(Port.D)
feed_motor = Motor(Port.A)

touch_sensor = TouchSensor(Port.S1)

color_sensor = ColorSensor(Port.S3)


while True:
    feed_motor.run_until_stalled(120, duty_limit=50)
    feed_motor.run_angle(450, -200)

    belt_motor.run(-500)
    while not touch_sensor.pressed():
        pass
    belt_motor.stop()
    wait(1000)
    belt_motor.reset_angle(0)

    color_list = []

    while len(color_list) < 8:
        ev3.screen.load_image(ImageFile.RIGHT)

        ev3.screen.print(len(color_list))

        while True:
            pressed = Button.CENTER in ev3.buttons.pressed()
            color = color_sensor.color()
            if pressed or color in POSSIBLE_COLORS:
                break

        if pressed:
            break

        ev3.speaker.beep(1000, 100)
        color_list.append(color)

        while color_sensor.color() in POSSIBLE_COLORS:
            pass
        ev3.speaker.beep(2000, 100)

        ev3.screen.load_image(ImageFile.BACKWARD)
        wait(2000)

    ev3.speaker.play_file(SoundFile.READY)
    ev3.screen.load_image(ImageFile.EV3)

    for color in color_list:
        wait(1000)

        match color:
            case Color.BLUE:
                ev3.speaker.say('blue')
                belt_motor.run_target(500, 10)
            case Color.GREEN:
                ev3.speaker.say('green')
                belt_motor.run_target(500, 132)
            case Color.YELLOW:
                ev3.speaker.say('yellow')
                belt_motor.run_target(500, 360)
            case Color.RED:
                ev3.speaker.say('red')
                belt_motor.run_target(500, 530)

        feed_motor.run_angle(1500, 180)
        feed_motor.run_angle(1500, -180)