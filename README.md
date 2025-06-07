# 🐍 Snake Game com Ranking (Pygame + SQLite)

Este projeto implementa o clássico **Snake Game** utilizando a biblioteca **Pygame**, com um sistema de **ranking persistente** baseado em **SQLite**.

## 🎮 Funcionalidades

- Tela inicial com entrada do nome do jogador.
- Ciclo completo de jogo com reinício automático após "Game Over".
- Placar persistente dos **10 melhores jogadores**, exibido em tela.
- Interface gráfica com pontuação em tempo real.

## 🧰 Tecnologias utilizadas

- Python 3
- [Pygame](https://www.pygame.org/news)
- SQLite (`sqlite3`, embutido no Python)
- Random (`random`, embutido no Python)

## 🖥️ Pré-requisitos

- Python 3.8 ou superior
- Pygame

Instale o Pygame com:

```bash
pip install pygame
```

## ▶️ Como executar

Clone o repositório e execute o script principal:

```bash
git clone https://github.com/Eng-Soft-Claudio/SnakeGame.git
cd SnakeGame
python main.py
```

> Certifique-se de estar com o terminal na mesma pasta do arquivo `.py`.

## 🗃️ Banco de dados

O jogo cria automaticamente um arquivo SQLite chamado `placar.db` com a tabela `placares`, que armazena nome e pontuação dos jogadores. Apenas os 10 melhores resultados são exibidos.

## 📁 Estrutura do projeto

```
SnakeGame/
├── main.py         # Código principal do jogo
├── placar.db       # Banco de dados SQLite (gerado em tempo de execução)
├── README.md       # Documentação do projeto
```

## 📷 Capturas de tela

> (Você pode adicionar imagens em uma pasta `docs/` e referenciá-las aqui)

## 📜 Licença

Este projeto está licenciado sob os termos da **Licença MIT**, conforme descrito a seguir.

---

## Licença MIT (Licença de Software de Código Aberto)

Copyright (c) [2025] Eng-Soft-Claudio

É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software e dos arquivos de documentação associados (o "Software"), para lidar com o Software sem restrição, incluindo, sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software, e permitir que pessoas a quem o Software é fornecido o façam, sujeitas às seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas as cópias ou partes substanciais do Software.

O SOFTWARE É FORNECIDO "NO ESTADO EM QUE SE ENCONTRA", SEM GARANTIA DE QUALQUER TIPO, EXPRESSA OU IMPLÍCITA, INCLUINDO MAS NÃO SE LIMITANDO ÀS GARANTIAS DE COMERCIALIZAÇÃO, ADEQUAÇÃO A UM DETERMINADO FIM E NÃO VIOLAÇÃO. EM NENHUMA HIPÓTESE OS AUTORES OU DETENTORES DOS DIREITOS AUTORAIS SERÃO RESPONSÁVEIS POR QUALQUER REIVINDICAÇÃO, DANO OU OUTRA RESPONSABILIDADE, SEJA EM UMA AÇÃO DE CONTRATO, ATO ILÍCITO OU DE OUTRA FORMA, DECORRENTE DE, FORA DE OU EM CONEXÃO COM O SOFTWARE OU O USO OU OUTRAS NEGOCIAÇÕES NO SOFTWARE.

---

Feito com 🐍 e ☕ por [Eng-Soft-Claudio](https://github.com/Eng-Soft-Claudio)