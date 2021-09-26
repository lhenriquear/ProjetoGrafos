import csv

class Grafo:
    def __init__(self):
        # Iniciamos a nossa matriz de adjacencia, que nem vimos la em cima
        self.adjacencia = {}

    def adiciona(self, vertice):
        # Para adicionar um vertice, simplesmente criamos a chave dele dentro nosso dicionario de adjacencia
        self.adjacencia[vertice] = {}

    def cria_vertice(self):
        with open('usuarios.csv', newline='') as csvfile:
            f = csv.reader(csvfile, delimiter=',')
            for row in f:
                self.adiciona(row[1])
                # print(row)

    def conecta(self, origem, destino, peso=1):
        # Acessamos nosso vertice e criamos uma chave para a conexao dele,...
        # ...atribuindo o valor como sendo o peso
        self.adjacencia[origem][destino] = peso
        # self.adjacencia[destino][origem] = peso

    def cria_aresta(self):
        with open('conexoes.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.conecta(row[0], row[1], row[2])
                # print(row)

    def busca_profundidade(self, origem, visitados=None):
        # Criando lista de visitados vazia na primeira iteracao
        if visitados is None:
            visitados = []
        # Pegando os nós adjacentes, que são as chaves do meu dicionario interno
        visitados.append(origem)
        for adjacente in self.adjacencia[origem].keys():
            if adjacente not in visitados:
                self.busca_profundidade(adjacente, visitados)
        return visitados

    def quantos_me_seguem(self, destino):
        seguidores = 0
        for seguidor in self.adjacencia.values():
            if destino in seguidor:
                seguidores += 1
        # print(f" o usuário {destino} tem {seguidores} seguidores")
        return seguidores

    def quantos_sigo(self, origem):
        follows = len(self.adjacencia[origem])
        print(f"O usuário {origem} segue {follows} pessoas")

    def top_influencers(self, k):
        top_influencer = {}

        for origem in self.adjacencia.keys():
            top = self.quantos_me_seguem(origem)
            top_influencer[origem] = top

        lista_auxiliar = []
        for i in sorted(top_influencer, key=top_influencer.get, reverse=True):
            lista_auxiliar.append(i)

        print(lista_auxiliar[0:k])

    def listaStories(self, usuarioInteressado):
        listaMelhoresAmigos = []
        listaAmigosComuns = []
        for conexao, peso in self.adjacencia[usuarioInteressado].items():
            if peso == "2":
                listaMelhoresAmigos.append(conexao)
            else:
                listaAmigosComuns.append(conexao)
        listaMelhoresAmigos = sorted(listaMelhoresAmigos)
        listaAmigosComuns = sorted(listaAmigosComuns)
        print("Stories (Melhores Amigos) de " + usuarioInteressado, *listaMelhoresAmigos, sep=" | ")
        print("Stories (Amigos Comuns) de " + usuarioInteressado, *listaAmigosComuns, sep=" | ")


g = Grafo()
g.cria_vertice()
g.cria_aresta()
# g.quantos_sigo("helena42")
# g.quantos_me_seguem("helena42")
g.top_influencers()
