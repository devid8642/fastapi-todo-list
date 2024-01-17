# Todoist

## Setup Backend
O backed é desenvolvido usando python 3.11+. Recomenda-se o uso da ferramenta poetry para fazer o gerenciamento das depedências do projeto. Instalando as dependências:

### Com o Poetry
```
poetry install --no-root
```

### Com o PIP
```
pip install -r requirements.txt
pip install -r requirements_dev.txt
```

### Rodando o backend
```
task run
```

### Rodando os testes do backend
```
task test
```

### Verificando a cobertura de código dos testes
```
task post_test
```
Após isso acessar via navegador o arquivo htmlcov/index.html para verificar a cobertura dos testes por arquivo.



## Setup Frontend