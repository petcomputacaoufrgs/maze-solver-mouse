import time

# Importe as funções do motor a ser usado (L298N ou L9110)
# Exemplo assumindo que estamos usando as funções do L9110
from motor.L9110 import motor_a_forward, motor_b_forward, all_stop


class RobotController:
    def __init__(self, sonar_system, pwm_a, pwm_b):
        self.sonar = sonar_system
        self.pwm_a = pwm_a
        self.pwm_b = pwm_b

        # Kp: constant proporcional, deverão ser feitos testes para descobrir o valor ideal
        # Se o robô oscilar muito, diminuir. Se demorar a corrigir, aumentar.
        self.Kp = 1.5
        self.base_speed = 60  # Velocidade base de 0 a 100

    def move_forward_with_correction(self, duration_or_condition):
        """
        Move o robô para frente corrigindo a trajetória usando os sensores laterais.
        """
        start_time = time.time()

        # Loop de controle (pode ser baseado no encoder das rodas - aqui está baseado no tempo)
        while time.time() - start_time < duration_or_condition:

            # Lê os sensores
            dist_esq = self.sonar.get_filtered_distance("esquerda")
            dist_dir = self.sonar.get_filtered_distance("direita")

            # Se der erro na leitura apenas segue reto ignorando a correção
            if dist_esq == -1 or dist_dir == -1 or dist_esq > 20 or dist_dir > 20:
                motor_a_forward(self.base_speed, self.pwm_a)
                motor_b_forward(self.base_speed, self.pwm_b)
                continue

            # Calculo do erro
            erro = dist_esq - dist_dir

            # Calculo do ajuste
            ajuste = self.Kp * erro

            # Aplica o ajuste nas velocidades (Motor A = Esquerda, Motor B = Direita - ou vice versa dependendo da montagem)
            # Valor limitado entre 0 e 100 para não estourar o limite do PWM
            speed_a = max(0, min(100, self.base_speed + ajuste))
            speed_b = max(0, min(100, self.base_speed - ajuste))

            # Manda o comando para os motores
            motor_a_forward(speed_a, self.pwm_a)
            motor_b_forward(speed_b, self.pwm_b)

            # Pausa para não sobrecarregar Raspberry Pi (comentar se não for necessário)
            time.sleep(0.05)

        # Para o robô ao terminar o movimento
        all_stop(self.pwm_a, self.pwm_b)
