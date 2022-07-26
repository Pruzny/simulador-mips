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
1. Executando as instruções: Selecione a caixa que contém as etapas do pipeline e aperte espaço. 
2. Visualizando os registradores e a memória de dados: Selecione a caixa que deseja e mova com o botão 3 do mouse (scroll).
3. Utilize um arquivo que contenha um código em asm, sendo o utilizado o ISA do mips. Por favor, lembre-se que não aceitamos pseudo-instruções talvez suportadas pelo MARS, apenas o pseudo-código "move" foi mapeado. 
4. Nossa memória de dados tem limite de 1000 bytes (250 endereços). Lembre-se dessa limitação para quando for utilizar alguma instrução que faça acesso a memória de dados, como "lw",  "sw". 
5. A memória de dados e os registradores colocará os valores em **hexadecimal**. 
6. Nosso simulador já está tratando os hazards possíveis nativamente, sem possibilidade de ativação ou desativação.
7. Nossa previsão de desvio nas instruções de branch, são estáticas, prevendo sempre o falso, em nossa arquitetura a etapa ID irá calcular o verdadeiro valor do branch. Caso nossa previsão esteja incorreta, terá um stall de 1 ciclo e irá para o label correspondente da instrução de branch.
8. Ainda sobre o branch, caso você faça uma dependência do branch que não será executada a tempo do branch ser finalizado no ID, por favor, insira uma instrução **sll $zero, $zero, 0** antes da instrução de branch. O Forwarding nesse caso, não funcionará porque a instrução ainda não foi executada.
9. Ao utilizar a instrução "jr", o programador deve ficar atento a adicionar corretamente o valor no registrador. Caso a instrução desejada para seguir no jr, esteja na posição 4 contando a partir do 1, adicione 3 no registrador referente. Para mais informações, utilize o exemplo_funcao.asm em base/exemplos_testados
10. Por favor, utilize instruções junto ao label. A maneira de funcionamento depende disso. Exemplo abaixo:
```
EXIT: add, $s0, $s1, $s2
```
Correto e aceitável.
```
EXIT:
add, $s0, $s1, $s2
```
Correto, porém não aceitável para o simulador.

6. As instruções aceitas estará na imagem abaixo. Junto com a maneira de calculo que ocorrerá na etapa EX. Salvo instruções de branch que serão executadas na etapa ID.
![Screenshot_20220717_135718](https://user-images.githubusercontent.com/56206429/179416755-e52c5a1f-9f50-4f2a-b459-fe463b72c2f8.png)
