"""Este módulo é responsável por carregar e criar as visualizaçẽos dos dados."""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging
import sys

# Logger
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler() # Log que será mostrado na tela
f_handler = logging.FileHandler('/tmp/recsys') # Log no arquivo, contendo os erros
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

class Visualizer():
    """Classe que irá lidar com as diferentes visualizações como histogram, distribuição, gráfico de barras e etc"""
    def __init__(self,train_path_file=None, metadata_path_file=None, train=None, metadata=None):
        self.__train_path_file = train_path_file
        self.__metadata_path_file = metadata_path_file

        if(train_path_file is not None and metadata_path_file is not None):
            logger.info("Arquivo que será carregado: %s",train_path_file)
            logger.info("Arquivo que será carregado: %s",metadata_path_file)
            self.__load_train_data() # Função para carregar os dados de treino
            self.__load_metadata() # Função para carregar os metadados
            logger.info("Arquivos carregados!")
        elif(train is not None and metadata is not None):
            self.__train = train
            self.__metadata = metadata
        else:
            logger.error("O path dos arquivos e nem o objeto de dados foi passado como argumentos. Programa\
                        irá finalizar")
            sys.exit(1)


    def __load_train_data(self):
        self.__train = pd.read_csv(self.__train_path_file,sep=",")

    def __load_metadata(self):
        self.__metadata = pd.read_csv(self.__metadata_path_file,sep=",")

    def get_train_data(self):
        return self.__train

    def get_metadata(self):
        return self.__metadata

    # Verificando a distribuição de uma certa coluna
    def column_distribution(self, column, log=True):
        logger.info("Criando visualizações da distribuição da coluna: %s",column)
        sns.distplot(self.__train[column],hist_kws={'log':log}) # Colocando em escala logratímica
        fig_name = "visualization/dist_" + column + ".png"
        plt.savefig(fig_name)

    # Contando os números diferentes de sampls em uma coluna
    def count_column(self, column):
        print(self.__train[column].value_counts())
