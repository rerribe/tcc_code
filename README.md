# tcc_code

Ok,
Essa é a implementação do meu trabalho de conclusão de curso, que consiste em um simplificador lógico de 
máquinas de estados finitos, que por meio do algoritmo de resfriamento simulado(Simulated Annealing), chega à
atribuição de estados que representa o circuito de menor área para uma determinada MSF.

O código começa convertendo o arquivo de benchmark no formato .kiss2 para .PLA. Para assim ser alimentado ao 
simplificador lógico ESPRESSO, que é um dos mais usados pela comunidade pois oferece um resultado satisfatório 
e mais rápido que outros métodos, como quine-mccluskey.

Como o ESPRESSO é um script em C, foi necessário fazer a utulização de subprocessos para simplificar os arquivos convertidos 
de .kiss2 para .PLA, onde a criação de novas MSF's geram arquivos que são simplificados e atualizados pelo simplficador lógico e 
posteriormente, utilizadas para o cálculo de custo de solução.

O espaço de busca do algoritmo é gerado de forma aleatória, futuramente, pretendo implementar algum modo de manupular 
a criação do estado de busca para que acompanhe a escala de resfriamento.

