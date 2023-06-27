# remove-corrupted-files

Remover arquivos corrompidos.

## Dependências

- Python v3.11.0
- pip v23.1.2

## Como rodar?

- Instale os pacotes necessários

```sh
pip install -r requirements.txt
```

- Rodar a aplicação

```sh
python main.py
```

### Parâmetros adicionais (flags)

- `-d` ou `--dirpath` (string)

  Caminho para o diretório que você quer verificar os arquivos. Por padrão ele irá olhar os arquivos no diretório atual.

- `--removecorrupted` (boolean)

  Remover arquivos corrompidos ou vazios (em caso de planilhas) ao detectá-los ou `--no-removecorrupted` para não remover, que é o comportamento padrão.
