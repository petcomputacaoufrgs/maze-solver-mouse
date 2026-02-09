import RPi.GPIO as GPIO
import time

class SonarSystem:
    def __init__(self):
        # Configuração do modo GPIO em BCM - quer dizer, não usa os números físicos dos pinos, mas sim os números de GPIO
        GPIO.setmode(GPIO.BCM)
        
        # Mapa de Pinos
        # Estrutura: 'nome_sensor': {'trig': pino_t, 'echo': pino_e}
        self.sensors = {
            'frente':   {'trig': 23, 'echo': 24},
            'esquerda': {'trig': 17, 'echo': 27},
            'direita':  {'trig': 5,  'echo': 6}
        }
        
        # Configura entrada e saída para todos os sensores
        for name, pins in self.sensors.items():
            GPIO.setup(pins['trig'], GPIO.OUT)
            GPIO.setup(pins['echo'], GPIO.IN)
            
            # Inicializa o trigger em LOW
            GPIO.output(pins['trig'], False)

        print("Sensores Inicializados. Aguardando estabilização...")
        time.sleep(2)

    def get_distance(self, sensor_name):
        """
        Lê a distância de um sensor específico.
        Retorna a distância em cm ou -1 se houver erro/timeout.
        """
        if sensor_name not in self.sensors:
            print(f"Erro: Sensor '{sensor_name}' não existe.")
            return -1

        pins = self.sensors[sensor_name]
        trig = pins['trig']
        echo = pins['echo']

        # Envia pulso de 10us para o trigger
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        # Monitora o pulso de retorno (Echo)
        # Vai ficar esperando o echo ir para HIGH, e depois para LOW, medindo o tempo entre esses eventos
        # Fica esperando por resposta por no máximo 40ms (timeout) para evitar ficar preso em um loop infinito caso o sensor não responda
        timeout = time.time() + 0.04
        
        pulse_start = time.time()
        while GPIO.input(echo) == 0:
            pulse_start = time.time()
            if pulse_start > timeout:
                return -1 # Retorna erro se o sensor não responder

        pulse_end = time.time()
        while GPIO.input(echo) == 1:
            pulse_end = time.time()
            if pulse_end > timeout:
                return -1 # Retorna erro se o sensor não responder

        pulse_duration = pulse_end - pulse_start
        
        # Cálculo da distância
        # Velocidade do som = 34300 cm/s
        # Distância = (Tempo * Velocidade) / 2 (ida e volta)
        distance = pulse_duration * 17150
        
        return round(distance, 2)
    


    def get_filtered_distance(self, sensor_name, samples=3):
        """
        Lê a distância do sensor `sensor_name` um número de vezes definido por `samples`.
        Retorna a mediana das leituras para reduzir o impacto de leituras ruidosas.
        """

        readings = []
        for _ in range(samples):
            readings.append(self.get_distance(sensor_name))
            time.sleep(0.005) # Pequena pausa entre leituras
        
        readings.sort()
        # Retorna o valor do meio (mediana)
        return readings[len(readings) // 2]
    


    def cleanup(self):
        """Libera os pinos GPIO ao desligar o robô"""
        GPIO.cleanup()


"""

# Exemplo:

if __name__ == "__main__":
    try:
        sonar = SonarSystem()
        while True:
            dist_f = sonar.get_distance('frente')
            dist_e = sonar.get_distance('esquerda')
            dist_d = sonar.get_distance('direita')
            
            print(f"Frente: {dist_f}cm | Esq: {dist_e}cm | Dir: {dist_d}cm")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nParando...")
        sonar.cleanup()

"""