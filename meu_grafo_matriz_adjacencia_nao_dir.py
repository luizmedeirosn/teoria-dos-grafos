from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado
from bibgrafo.grafo_exceptions import *
from bibgrafo.aresta import Aresta
import copy

class MeuGrafo(GrafoMatrizAdjacenciaNaoDirecionado):

    def vertices_nao_adjacentes(self):
        '''
        Provê uma lista de vértices não adjacentes no grafo. A lista terá o seguinte formato: [X-Z, X-W, ...]
        Onde X, Z e W são vértices no grafo que não tem uma aresta entre eles.
        :return: Uma lista com os pares de vértices não adjacentes
        '''
        resp = list()
        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if j > i and not bool(self.M[i][j]): #caso a posição na matriz seja vazia, indica que não há adjacencia entre os vertices correspondentes
                    resp.append('%s-%s' % (self.N[i], self.N[j])) #o index dos vertices na matriz são iguais aos index desses mesmos vertices no self.N
        return resp

    def ha_laco(self):
        '''
        Verifica se existe algum laço no grafo.
        :return: Um valor booleano que indica se existe algum laço.
        '''
        for i in range(len(self.M)):
            if bool(self.M[i][i]): #caso haja algum elemento na diagonal principal, indica um laço
                return True
        return False

    def grau(self, V=''):
        '''
        Provê o grau do vértice passado como parâmetro
        :param V: O rótulo do vértice a ser analisado
        :return: Um valor inteiro que indica o grau do vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''
        if V not in self.N: #caso vertice inválido
            raise VerticeInvalidoException

        cont = 0 #grau a ser retornado
        linhaDoV = self.N.index(V) #pega a posição do V(parâmetro) na matriz
        for i in range(len(self.M)):
            for j in range(len(self.M)):
                if j >= i: #ler-se a matriz apenas na diagonal principal e à cima
                    if (i == linhaDoV or j == linhaDoV) and bool(self.M[i][j]): #é necessario ler-se apenas as posições que correspondem ao V(parâmetro) tanto no sentido de linhas como no de colunas
                        if i == j: #se for laço
                            # pegamos a quantidade de arestas na posição e incrementa-se o contador:
                            cont += (len(self.M[i][j]) * 2)
                        else:
                            cont += len(self.M[i][j])
        return cont

    def ha_paralelas(self):
        '''
        Verifica se há arestas paralelas no grafo
        :return: Um valor booleano que indica se existem arestas paralelas no grafo.
        '''
        for i in range(len(self.M)):
            for j in range(len(self.M)):
                if len(self.M[i][j]) > 1: #caso haja mais de uma aresta na posição da matriz, há paralelas
                    return True
        return False

    def arestas_sobre_vertice(self, V):
        '''
        Provê uma lista que contém os rótulos das arestas que incidem sobre o vértice passado como parâmetro
        :param V: O vértice a ser analisado
        :return: Uma lista os rótulos das arestas que incidem sobre o vértice
        :raises: VerticeInvalidoException se o vértice não existe no grafo
        '''

        '''
        O raciocínio é o mesmo que a função do grau, porém ao inves de incrementar-se um contador, adiciona-se
        cada uma das arestas que estão numa posição da matriz, dentro de uma lista.
        '''
        if V not in self.N:
            raise VerticeInvalidoException

        arestas = list()
        indexV = self.N.index(V)

        for i in range(len(self.M)):
            for j in range(len(self.M)):
                if j >= i:
                    if (i == indexV or j == indexV) and bool(self.M[i][j]):
                        for rotulo in self.M[i][j]:
                            arestas.append(rotulo)
        return arestas

    def eh_completo(self):
        '''
        Verifica se o grafo é completo.
        :return: Um valor booleano que indica se o grafo é completo
        '''

        '''
        Para um grafo ser completo, ele não pode conter laços, arestas paralelas e vertices não adjacentes.
        '''
        if self.ha_laco() or self.ha_paralelas() or bool(self.vertices_nao_adjacentes()):
            return False
        return True

    def getAresta(self, rotulo):
        '''
        :param rotulo: rótulo da aresta que deve ser retornada.
        :return: retorna a aresta correspondente ao rótulo.
        '''

        for i in range(len(self.M)):
            for j in range(len(self.M[i])):
                if j >= i and bool(self.M[i][j]):
                    for rotuloAresta in self.M[i][j]:
                        if rotulo == rotuloAresta:
                            a = Aresta(rotulo, self.N[i], self.N[j])
                            return a

    def dfs(self, V):
        dfsFinal = MeuGrafo()
        listaVazia = []
        return self.dfs_rec(V, dfsFinal, listaVazia)

    def dfs_rec(self, V, dfsFinal, vertVisitados):
        vertVisitados.append(V)

        for rotulo in self.arestas_sobre_vertice(V):
            aresta = self.getAresta(rotulo)
            if V not in dfsFinal.N:
                dfsFinal.adicionaVertice(V)

            if aresta.getV1() == V:
                if aresta.getV2() not in vertVisitados:
                    dfsFinal.adicionaVertice(aresta.getV2())
                    dfsFinal.adicionaAresta(rotulo, V, aresta.getV2())
                    self.dfs_rec(aresta.getV2(), dfsFinal, vertVisitados)
            else:
                if aresta.getV1() not in vertVisitados:
                    dfsFinal.adicionaVertice(aresta.getV1())
                    dfsFinal.adicionaAresta(rotulo, V, aresta.getV1())
                    self.dfs_rec(aresta.getV1(), dfsFinal, vertVisitados)
        return dfsFinal

    def conexo(self):
        '''
        Verifica se um grafo é conexo ou não. Para um grafo ser conexo, todos os seus vertices devem estar
        presentes em sua arvoreDfs.
        :return: um valor booleano que indica se é conexo ou não.
        '''

        dfs = self.dfs(self.N[0])
        if len(self.N) != len(dfs.N):
            return False
        return True

    def verticesImpares(self):
        '''
        Retorna os vertices ímpares de um grafo.
        :return: Uma lista com os vertices ímpares, pode ser vazia ou não.
        '''

        lista = list()
        for v in self.N:
            if self.grau(v) % 2 == 1:
                lista.append(v)
        return lista

    def haCaminhoDeEuler(self):
        '''
        Verifica se o grafo possui ou não caminho de euler.
        :return: Um valor booleano que indica se o grafo possui ou não caminho de euler
        '''
        '''
        Um gráfico contém o Caminho de Euler apenas se tiver exatamente 0 ou 2 vértices de grau ímpar.Além disso
        ele também deve ser conexo.
        '''

        if not self.conexo():
            return False

        lista = self.verticesImpares()
        if len(lista) != 0 and len(lista) != 2:
            return False
        return True

    def isPonte(self, aresta):
        '''
        Verifica se a aresta passada como parâmetro é uma ponte.
        :param aresta: um objeto aresta do grafo.
        :return: uma lista com um valor booleano que indica se a aresta é uma ponte e a posição da aresta na matriz
        '''
        grafo = copy.deepcopy(self)
        #print(grafo)

        for i in range(len(grafo.M)):
            for j in range(len(grafo.M[i])):
                if j >= i and bool(grafo.M[i][j]):
                    for rotulo in grafo.M[i][j]:
                        if rotulo == aresta.getRotulo():
                            del grafo.M[i][j][rotulo]
                            if not grafo.conexo():
                                return [True, i, j, rotulo]
                            else:
                                return [False, i, j, rotulo]

    def allIsPonte(self):
        '''
        Verifica se todas as arestas do grafo são pontes.
        :return: um valor boleano que indica se todas são pontes ou não.
        '''
        grafo = self
        # print(grafo)
        lista = list()
        cont = 0
        for i in range(len(grafo.M)):
            for j in range(len(grafo.M[i])):
                if j >= i and bool(grafo.M[i][j]):
                    for rotulo in grafo.M[i][j]:
                        if grafo.isPonte(grafo.getAresta(rotulo))[0]:
                            lista.append(rotulo)
                        cont += 1
        if cont == len(lista):
            return True
        else:
            return False

    def caminhoDeEuler(self):
        '''
        Verifica se há ou não um caminho de Euler no grafo.
        :return: um valor booleano caso não haja caminho ou uma lista que contém o caminho.
        '''
        if not self.haCaminhoDeEuler():
            return False

        caminho = list()
        grafo = copy.deepcopy(self)
        vertices = self.verticesImpares()
        V = None

        if len(vertices) == 0:
            V = self.N[0]
            return self.caminhoDeEuler_rec(V, caminho, grafo)
        else:
            V = vertices[1]
            return self.caminhoDeEuler_rec(V, caminho, grafo)

    def caminhoDeEuler_rec(self, V, caminho, grafo):
        '''

        :param V: O vertice para dar inicio a analise e elaboração do caminho.
        :param caminho: Uma lista inicialmente vazia, porém conforme o decorrer do codigo irá ser contruido um caminho
        dentro dela.
        :param grafo: uma cópia do grafo principal.
        :return: um caminho de euler.
        '''
        if grafo.grau(V) == 0:
            caminho.append(V)
            return caminho

        for rotulo in grafo.arestas_sobre_vertice(V):

            if grafo.grau(V) == 0:
                return caminho

            aresta = grafo.getAresta(rotulo)
            isPonte = grafo.isPonte(aresta)

            if not isPonte[0] or grafo.allIsPonte() or grafo.grau(V) == 1: #se a aresta visitada não é uma ponte, ou se todas as arestas presentes no grafo são pontes, ou se o grau do vertice analisado é 1.
                caminho.append(V)
                caminho.append(aresta.getRotulo())
                del grafo.M[isPonte[1]][isPonte[2]][isPonte[3]] #deleta-se a aresta analisada após os dados serem coletados, uma vez que é necessario seguir a logica do algoritmo.
                if aresta.getV1() == V:
                    grafo.caminhoDeEuler_rec(aresta.getV2(), caminho, grafo)
                else:
                    grafo.caminhoDeEuler_rec(aresta.getV1(), caminho, grafo)
        return caminho