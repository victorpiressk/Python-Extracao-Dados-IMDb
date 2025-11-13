# Extração de Dados do IMDb

## [0.0.2] - 2025-11-13

### Changed

#### Arquivo `multithreading_test.py`:
- Atualização das funções de extração de dados do IMDb

## [0.0.1] - 2025-11-10

### Added 

#### Arquivo `single_thread.py`:
- realiza a extração de dados do IMDb de forma sequencial (um filme por vez)
- gera um arquivo `.csv` com os resultados.
#### Arquivo `multithreading_test.py`:
- utilizado para testar funções e otimizações do processo de extração antes da implementação final.
#### Arquivo `multithreading.py`:
- realiza a extração de dados do IMDb de forma paralela utilizando *multithreading*
- gera um arquivo `.csv` de maneira mais eficiente.