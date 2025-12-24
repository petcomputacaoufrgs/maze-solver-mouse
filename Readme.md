# Mico-Leão - Maze Solver Mouse

O Mico-leão é um projeto do PET Computação UFRGS voltado para o estudo de robótica e IA. Esse repositório tem como objetivo desenvolver um robô autônomo solucionador de labirintos usando o algoritmo Flood Fill. O projeto inclui uma simulação gráfica completa para testes e validação antes da implementação no hardware físico.

## Sobre o Robô

O robô que navega autonomamente por labirintos desconhecidos, mapeando o ambiente em tempo real e encontrando o caminho mais eficiente até o objetivo. O algoritmo utilizado (Flood Fill) calcula continuamente as distâncias até o destino, permitindo que o robô tome decisões inteligentes mesmo em ambientes parcialmente conhecidos.

### Funcionalidades Atuais

- **Simulação visual interativa** com Pygame
- **Geração procedural de labirintos** com seeds customizáveis
- **Algoritmo Flood Fill** para navegação inteligente
- **Mapeamento progressivo** do ambiente
- **Visualização em tempo real** com heatmap de distâncias
- **Controles de simulação** (play/pause, reset, velocidade)
- **Métricas de performance** (passos tomados vs. ideal)

### Em Desenvolvimento

- Integração com hardware físico (sensores e motores)
- Otimização de trajetória

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositório>
cd maze-solver-mouse
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a simulação**
```bash
python main.py
```

## Como Usar

### Controles da Interface

- **▶️ Play/Pause** - Inicia ou pausa a simulação
- **🔄 Reset** - Reseta o robô para a posição inicial mantendo o mapa conhecido
- **🔃 Restart** - Reinicia completamente (novo mapa vazio)
- **Gerar** - Cria um novo labirinto com as dimensões especificadas
- **🎲 Randomizar Seed** - Gera uma seed aleatória
- **Slider de Intervalo** - Controla a velocidade da simulação (10-1000ms)

### Campos de Entrada

- **L (Largura)** - Define largura do labirinto (valores ímpares)
- **A (Altura)** - Define altura do labirinto (valores ímpares)
- **Seed** - Número para gerar labirintos reproduzíveis

### Visualização

- **Células vermelhas → amarelas → brancas → azuis** - Heatmap de distância até o objetivo
- **Números nas células** - Distância mínima conhecida até o objetivo
- **Bordas cinzas** - Paredes ainda não descobertas pelo robô
- **Células pretas** - Paredes conhecidas
- **Célula cinza claro** - Entrada
- **Célula verde** - Objetivo

## Estrutura do Projeto

```
maze-solver-mouse/
├── assets/                          # Recursos visuais
│   ├── logo_pet.png                # Logo do PET
│   ├── mouse.png                   # Sprite do robô
│   └── [ícones dos botões]
│
├── simulation/                      # Módulo de simulação
│   ├── __init__.py
│   ├── simulation.py               # Loop principal e lógica de simulação
│   ├── ui/                         # Interface do usuário
│   │   ├── __init__.py
│   │   ├── interface.py            # Gerenciador principal da interface
│   │   ├── ui_elements.py          # Botões, sliders, inputs
│   │   ├── ui_layout.py            # Constantes de layout
│   │   └── theme.py                # Cores e estilos
│   └── renderers/                  # Renderizadores especializados
│       ├── __init__.py
│       ├── maze_renderer.py        # Renderiza labirinto e heatmap
│       ├── ui_renderer.py          # Renderiza títulos e legendas
│       └── mouse_renderer.py       # Renderiza e rotaciona o robô
│
├── maze_generator.py               # Geração procedural de labirintos
├── maze_solver.py                  # Algoritmo Flood Fill
├── main.py                         # Entry point da aplicação
├── requirements.txt                # Dependências do projeto
└── README.md
```

## Detalhes de Implementação

### Algoritmo de Navegação

O robô utiliza uma abordagem baseada em **Flood Fill** com as seguintes características:

1. **Mapeamento Progressivo**
   - Visão limitada (3 direções: frente, esquerda, direita)
   - Alcance de visão: `min(BOT_VISION_BY_SQUARES, distância até parede)`
   - Atualiza mapa conhecido a cada movimento

2. **Tomada de Decisão**
   - Recalcula distâncias com Flood Fill quando há escolhas
   - Prioriza células com menor distância até o objetivo
   - Em empates: mantém direção atual > movimento ortogonal > volta

### Inicialização do Sistema

#### Definição do Labirinto (Simulação)
- Layout: matriz onde `0` = caminho livre, `1` = parede
- Define entrada e saída aleatórias
- Garante que dimensões sejam ímpares (requisito do algoritmo)

#### Labirinto Conhecido pelo Robô
- Inicializa apenas com entrada e saída (*nota 1)
- Expande progressivamente conforme exploração
- Paredes desconhecidas representadas como "caminho potencial"

### Loop Principal

```
1. Atualiza Visão
   ↓
2. Aplica Flood Fill (se necessário)
   ↓
3. Seleciona Melhor Direção
   ↓
4. Move Robô
   ↓
5. Verifica Chegada ao Objetivo
   ↓
   [Repete ou Finaliza]
```

## Arquitetura de Renderização

O projeto utiliza uma arquitetura modular de renderização:

- **MazeRenderer** - Responsável pelo labirinto e heatmap de distâncias
- **UIRenderer** - Gerencia títulos, legendas e labels
- **MouseRenderer** - Renderiza e rotaciona o robô
- **UILayout** - Centraliza todas as constantes de posicionamento

Esta separação facilita manutenção, testes e futuras expansões.

## Labirintos de Teste

Labirintos interessantes para teste (difíceis ou com performance pior):

| Seed   | Dimensões (L x A) |
|--------|-------------------|
| 346967 | 71 x 55           |
| 77492  | 63 x 63           |
| 175156 | 29 x 29           |

## Observações Técnicas

- **Nota 1**: Inicialização do mapa conhecido depende das informações fornecidas ao robô:
  - Apenas saída: inicia com pontas na entrada/saída
  - Entrada + saída: pode inicializar área retangular entre ambos
  
- **Valores ímpares**: Dimensões do labirinto devem ser ímpares para garantir funcionamento correto do algoritmo de geração

- **Performance**: Para labirintos > 30x30, números nas células são ocultados para melhor performance

## Equipe

Desenvolvido por estudantes do Programa de Educação Tutorial (PET) Computação UFRGS para fins educacionais.
Integrantes do Projeto: Eduardo Altmann, Eduardo Fonseca, Guilherme d'Ávila, Leonardo Leal, Luiza Helwig