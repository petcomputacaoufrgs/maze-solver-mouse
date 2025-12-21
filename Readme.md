# INICIALIZAÇÃO

## Definição do labirinto real (só na simulação)
    - Define layout do labirinto (matriz onde 0 é caminho livre e 1 é parede)
    - Seleciona saida e entrada

- Inicializa o labirinto conhecido pelo robô: (um labirinto com pontas na entrada e na saída e sem paredes) (***1**)


## INÍCIO DO LOOP PRINCIPAL

1. Atualiza visão do robô:
   - O robô olha para 3 direções: frente, esquerda e direita um número de quadrados igual a min(BOT_VISION_BY_SQUARES, parede mais próxima seguindo a direção)
   - Atualiza o labirinto conhecido pelo robô com a visão atual, o que pode expandir o labirinto conhecido

    - Se o robô só tem apenas uma direção possível: apenas continua.
    - Se não:
        - Aplica o algoritmo de flood fill a partir da saída para preencher o labirinto conhecido com a distância mínima até a saída de cada quadrado

        - Seleciona a direção a seguir:
            1. Pega as direções que levam aos menores valores de distância até a saída. 
            2. Em caso de empate, dá preferância para a direção para a qual o robô está virado e depois para a direção que leve a um menor esforço de movimento (ortogonais primeiro, por último oposta).
            3. Vira o robô para a direção selecionada.
   
2. Avança o robô

3. Se o robô chegou na saída termina o loop

---------------------------

# OBSERVAÇÕES

- *1: depende das informações que vamos fornecer para o robô. Se fornecermos só a saída, vai ser isso mesmo. 
- Fornecendo a entrada também, o labirinto conhecido pode inicializar da posição (0, 0) até (maxRow(entrada, saida), maxCol(entrada, saída)) 
