# Antes de mais nada, iremos importar o módulo 'csv' a fim de realizar a leitura
# dos arquivos disponibilizados pelos professores para a execução do projeto.

import csv

class RedeSocial():
    def __init__(self):
        """
        Método inicializador da Rede Social. Cria um dicionário vazio atribuído à 
        matriz de adjacência, responsável por guardar as informações referentes aos
        usuários da Rede Social.
        """
        self.matriz_adjacencia = {}    

    # O primeiro método próprio de nossa classe será responsável por adicionar os 
    # vértices (i.e., usuários) à matriz de adjacência de forma genérica, também
    # em formato de dicionário vazio, inicialmente.
    
    def adicionar_usuario(self, usuario):
        self.matriz_adjacencia[usuario] = {}
    
    # Como no caso em tela temos um banco de dados pronto com a listagem do nome
    # e username de cada um dos usuários pré-criados, o segundo método fará a 
    # adição dos vértices a partir de qualquer arquivo no formato 'csv' com o 
    # mesmo padrão de dados.
    
    def adicionar_usuario_arquivo(self, arquivo_usuarios):
        with open(arquivo_usuarios, newline = "") as csvfile:
            lista_tuplas = [tuple(linha) for linha in csv.reader(csvfile)]
            
            for (_, usuario) in lista_tuplas:
                self.matriz_adjacencia[usuario] = {}
    
    # O terceiro e quarto métodos serão responsáveis por realizar as conexões
    # entre os usuários a partir da leitura do arquivo conexoes.csv, e juntá-las
    # à matriz de adjacência.
   
    # Sabemos que se trata de um grafo ponderado, portanto não é necessário 
    # atribuir '1' ao peso "padrão".
    
    # Ademais, trata-se de um grafo direcionado, não sendo necessário realizar
    # a inclusão do caminho "destino -> origem", apenas "origem -> destino".
    
    def conectar_usuarios(self, seguidor, seguido, peso):
        self.matriz_adjacencia[seguidor][seguido] = peso
    
    def criar_lista_conexoes(self, arquivo_conexoes):
        with open (arquivo_conexoes, newline = "") as csvfile:
            lista_conexoes = csv.reader(csvfile)
            
            for linha in lista_conexoes:
                self.conectar_usuarios(linha[0], linha[1], linha[2])

    # As duas funções abaixo servem para verificar e, posteriormente, caso
    # necessário ou quisto, remover uma conexão da rede social (p.ex., se 
    # detectado que um usuário deixou de seguir outro usuário). A função não
    # consta dos requerimentos mínimos do projeto, mas acreditamos ser uma boa
    # adição.
    
    def verificar_adjacencia(self, seguidor, seguido):
        return seguido in self.matriz_adjacencia[seguidor].keys()
    
    def remover_conexao(self, seguidor, seguido):
        if self.verificar_adjacencia(seguidor, seguido):
            self.matriz_adjacencia[seguidor].pop[seguido]
            return

    # Criada a matriz de adjacência, os próximos métodos servirão para realizar
    # cada uma das funções necessárias ao funcionamento da Rede Social conforme
    # solicitado pelas instruções do Projeto.

    ## Exibir número de seguidores de um usuário:
    
    ## Método auxiliar interno:
    
    def _contar_seguidores(self, usuario_interessado):
        total_seguidores = 0
        
        for _, conexoes in self.matriz_adjacencia.items():
            if usuario_interessado in conexoes.keys():
                total_seguidores += 1
        
        return total_seguidores
    
    ## Método externo:
    
    def contar_seguidores(self, usuario_interessado):
        seguidores = self._contar_seguidores(usuario_interessado)
        return print(f"O usuario {usuario_interessado} possui {seguidores} seguidores na Rede Social.")

    ## Exibir quantidade de pessoas que um usuário segue:
    
    def contar_seguidos(self, usuario_interessado):
        total_seguidos = len(self.matriz_adjacencia[usuario_interessado])
        print(f"O usuario {usuario_interessado} segue {total_seguidos} pessoas na Rede Social.")

    ## Ordenar a lista de "stories" a partir do peso das conexões, ou seja,
    ## melhores amigos primeiro, seguidos de conexões comuns, ambos em ordem
    ## alfabética:
    
    def lista_stories(self, usuario_interessado):
        lista_melhores_amigos = []
        lista_amigos_comuns = []
        
        for conexao, peso in self.matriz_adjacencia[usuario_interessado].items():
            if peso == "2":
                lista_melhores_amigos.append(conexao)
            else:
                lista_amigos_comuns.append(conexao)
       
        lista_melhores_amigos = sorted(lista_melhores_amigos)
        lista_amigos_comuns = sorted(lista_amigos_comuns)
        
        print("Stories | Melhores Amigos de: " + usuario_interessado, *lista_melhores_amigos, sep = " | ")
        print("Stories | Amigos de: " + usuario_interessado, *lista_amigos_comuns, sep = " | ")

    ## Encontrar o Top 'k' influencers (as 'k' pessoas que têm mais seguidores
    ## na Rede):
    
    def top_influencers(self, top_k):
        top_k_influencers = {}
        
        for origem in self.matriz_adjacencia.keys():
            numero_seguidores = self._contar_seguidores(origem)
            top_k_influencers[origem] = numero_seguidores
        lista_top_k = []
        
        for influencer in sorted(top_k_influencers, key = top_k_influencers.get, reverse = True):
            lista_top_k.append(influencer)
       
        print(f"Top {top_k} influenciadores da Rede Social: ")
        print(*lista_top_k[0:top_k], sep = "\n")

 ## Encontrar o caminho entre uma pessoa e outra na rede:
    
    def distancia_conexao(self, usuario_interessado, usuario_alvo):
        fila = [usuario_interessado]
        visitados = []
        predecessor = {usuario_interessado: None}
        
        while len (fila) > 0:
            primeiro_elemento = fila[0]
            fila = fila[1:]
            visitados.append(primeiro_elemento)
            
            for adjacente in self.matriz_adjacencia[primeiro_elemento].keys():
                if adjacente == usuario_alvo:
                    pred = primeiro_elemento
                    caminho = [usuario_alvo]
                    
                    while pred is not None:
                        caminho.append(pred)
                        pred = predecessor[pred]
                    
                    caminho.reverse()
                    caminho_string = " -> ".join(caminho)
                    
                    return print(f"Distância entre {usuario_interessado} e {usuario_alvo} na Rede Social é de {(int(len(caminho)) - 2)} grau(s): \n {caminho_string}")
            
                if (adjacente not in fila) and (adjacente not in visitados):
                    predecessor[adjacente] = primeiro_elemento
                    fila.append(adjacente)
                
        return print(f"Não foi possível encontrar um caminho entre {usuario_interessado} e {usuario_alvo} na Rede Social.")

####

instaMau = RedeSocial()
instaMau.adicionar_usuario_arquivo("usuarios.csv")
instaMau.criar_lista_conexoes("conexoes.csv")
instaMau.contar_seguidores("isis3")
instaMau.contar_seguidos("isis3")
instaMau.lista_stories("isis3")
instaMau.distancia_conexao("isis3", "helena42")
instaMau.top_influencers(5)