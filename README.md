# simulador-mips
Repositório para a atividade da disciplina Arquiteturas de Computadores

# O Projeto
O projeto é um trabalho para a disciplina de Arquitetura de Computadores. Foi feito um simulador de pipeline, que receberá um arquivo .asm e irá simular o processo da instruções do MIPS em 5 etapas do pipeline.

# Versão do Python
Utilizamos novas features que o [Python 3.10](https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tar.xz) adicionou. Os desenvolvedores [Maximilian Harrisson](https://github.com/Pruzny) e [Isadora Pacheco](https://github.com/Asunnya) usaram, respectivamente, as versões 3.10.1 e 3.10.5 para o desenvolvimento do trabalho.

# Modo de Execução

```
git clone https://github.com/Pruzny/simulador-mips
cd simulador-mips
python main.py
```

# Utilizando o simulador

1. Utilize um arquivo que contenha um código em asm, sendo o utilizado o ISA do mips. Por favor, lembre-se que não aceitamos pseudo-instruções talvez suportadas pelo MARS, apenas o pseudo-código "move" foi mapeado. 
2. Nossa memória de dados tem limite de 1000 bytes (250 endereços). Lembre-se dessa limitação para quando for utilizar alguma instrução que faça acesso a memória de dados, como "lw",  "sw". 
3. Nosso simulador já está tratando os hazards possíveis nativamente, sem possibilidade de ativação ou desativação.
4. Nossa previsão de desvio nas instruções de branch, são estáticas, prevendo sempre o falso, em nossa arquitetura a etapa ID irá calcular o verdadeiro valor do branch. Caso nossa previsão esteja incorreta, terá um stall de 1 ciclo e irá para o label correspondente da instrução de branch.
5. Por favor, utilize instruções junto ao label. A maneira de funcionamento depende disso. Exemplo abaixo:
```
EXIT: add, $s0, $s1, $s2
```
Correto e aceitável.
```
EXIT:
add, $s0, $s1, $s2
```
Correto, porém não aceitável para o simulador.

6. As instruções aceitas estará na imagem abaixo. Pela falta do syscall para rodarmos função, a instrução "jr" não teve mapeamento. 
![Screenshot_20220717_135718](https://user-images.githubusercontent.com/56206429/179416755-e52c5a1f-9f50-4f2a-b459-fe463b72c2f8.png)
