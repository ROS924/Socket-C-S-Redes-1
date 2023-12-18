# Socket-C-S-Redes-1
Trabalho final da disciplina MATA59 - REDES DE COMPUTADORES 2023.2

Integrantes:
* Lucas Azevedo
* Lucas Morais
* Marcelo Moura
* Rodrigo Ornellas
* Saulo Bonfim

O trabalho teve como objetivo criar um sistema que oferecesse os seguintes features:
* Capacidade de armazenar arquivos em computadores-servidores através de um proxy
* Uma aplicação-cliente com modos de depositar e recuperar arquivos
* A aplicação deve ser implementada com um proxy mediando a comunicação
* A aplicação deve seguir o modelo cliente-servidor


Após iniciar o proxy, server e client em máquinas distintas, é possível, a partir do terminal do client, executar as seguintes funções:

* `upload [filename with extension] [number of copies]`: armazena o arquivo especificado em `n` servidores;
* `recover [filename with extension]`: recupera uma copia do arquivo armazenado em um servidor conectado;
* `connected-servers`: apresenta lista dos servidores conectados;
* `modify [filename with extension] [number of copies]`: altera o número de replicações para um certo arquivo entre os servidores conectados;
* `quit`: encerra a aplicação.


