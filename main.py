#!/usr/bin/env python3
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveTank
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.display import Display
from time import sleep

# Motores e display
motor_esquerdo = LargeMotor(OUTPUT_A)
motor_direito = LargeMotor(OUTPUT_B)
robot = MoveTank(OUTPUT_A, OUTPUT_B)
display = Display()

# Sensores
sensor_cor = ColorSensor(INPUT_4)
sensor_infravermelho = InfraredSensor(INPUT_1)

# Parâmetros (0–100)
WHITE_THRESHOLD = 50   # Ajuste conforme a iluminação do dojo
ATTACK_SPEED = 80      # Velocidade de ataque (%)
SEARCH_SPEED = 40      # Velocidade de busca (%)
RETREAT_SPEED = -60    # Velocidade de recuo (%)

def detectar_borda():
    """
    Retorna True se a cor refletida for maior que o limite (borda branca).
    """
    return sensor_cor.reflected_light_intensity > WHITE_THRESHOLD

def detectar_oponente():
    """
    Detecta se o oponente está próximo com o sensor infravermelho.
    .proximity retorna de 0 (muito perto) a 100 (longe).
    """
    return sensor_infravermelho.proximity < 30

def recuar_e_girar_aleatorio():
    """
    Recuar quando detectar a borda.
    """
    display.text_pixels("Borda detectada! Recuando...", x=10, y=60, clear_screen=True)
    display.update()
    
    # Recuar por 0.4s
    robot.on_for_seconds(RETREAT_SPEED, RETREAT_SPEED, 0.4)
    sleep(0.1)

def atacar():
    """
    Avançar em alta velocidade para empurrar o oponente.
    """
    display.text_pixels("Oponente detectado! Atacando...", x=10, y=60, clear_screen=True)
    display.update()
    robot.on(ATTACK_SPEED, ATTACK_SPEED)

def procurar_oponente():
    """
    Movimento de busca: gira levemente para cobrir área.
    """
    display.text_pixels("Procurando...", x=10, y=60, clear_screen=True)
    display.update()
    robot.on(SEARCH_SPEED, int(SEARCH_SPEED/2))

# Loop principal
while True:
    if detectar_borda():
        recuar_e_girar_aleatorio()
    elif detectar_oponente():
        atacar()
    else:
        procurar_oponente()
