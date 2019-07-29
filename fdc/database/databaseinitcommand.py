from di_container.injector import Inject, di_container

import os


class FDCInitCommand(object):

    def __init__(self):
        self._configs = Inject('app configuration')
        self._git = Inject('fdc git wrapper')
        self._logger = Inject('logger')

    def database_parser_created_handler(self, db_parser):
        db_parser.add_parser(
            "init",
            help="Inicializa a pasta do FDC e o banco de dados com uma estrutura vazia. Se houver um banco de dados já "
                 "existente o mesmo será excluído e reiniciado.").set_defaults(event='database_init_command')

    def database_init_command_handler(self, args):
        # TODO Verificar se o arquivo de banco de dados é um SQLITE válido!

        self._ensure_fdc_folder_exists()

        self._ensure_fdc_folder_is_git_repository()

        self._ensure_database_structure_with_no_data()

        return 'ok'

    def _ensure_fdc_folder_exists(self):
        if not os.path.isdir(self._configs['fdc.folder']):
            self._logger.info('Creating fdc folder at "{}"', self._configs['fdc.folder'])
            os.makedirs(self._configs['fdc.folder'], exist_ok=True)
        else:
            self._logger.info('fdc folder found at "{}"', self._configs['fdc.folder'])

    def _ensure_fdc_folder_is_git_repository(self):
        if not self._git.is_repository():
            self._logger.info('Git repository not found at fdc folder, creating it...')
            if not self._git.init():
                raise FDCInitializationException('Error initializing git repository at "{}"',
                                                 self._git.repository_folder)

    def _ensure_database_structure_with_no_data(self):
        if os.path.isfile(self._configs['fdc.db_full_path']):
            self._logger.warn('Database file "{}" found, removing it...', self._configs['fdc.db_full_path'])
            os.remove(self._configs['fdc.db_full_path'])

        connection = di_container.get_resource('database connection')

        # TODO Create these tables via controller events to centralize table handling in specialized classes

        self._logger.debug('Creating table "Conta"...')
        connection.executescript('create table Conta ('
          '  nome text not null,'
          '  descricao text,'
          '  data_aquisicao date,'
          '  propriedades text not null,'
          '  observacao text);')

        self._logger.debug('Creating table "Cotacao"...')
        connection.executescript('create table Cotacao ('
          '  data date not null,'
          '  moeda text not null,'
          '  valor money not null);')

        self._logger.debug('Creating table "Orcamento"...')
        connection.executescript('create table Orcamento ('
          '  nome text not null,'
          '  descricao text not null);')

        self._logger.debug('Creating table "OrcamentoLancamento"...')
        connection.executescript('create table OrcamentoLancamento ('
          '  orcamento not null references Orcamento,'
          '  regra_data_vencimento text not null,'
          '  origem_padrao not null references Conta,'
          '  destino_padrao not null references Conta,'
          '  valor_padrao money not null,'
          '  cotacao_moeda text,'
          '  regra_cotacao_data text,'
          '  regra_periodo_referencia text not null,'
          '  produto references Produto,'
          '  quantidade integer,'
          '  observacao text);')

        self._logger.debug('Creating table "Lancamento"...')
        connection.executescript('create table Lancamento ('
          '  data date not null,'
          '  origem references Conta,'
          '  destino references Conta,'
          '  valor money not null,'
          '  cotacao references Cotacao,'
          '  referencia_inicio text,'
          '  referencia_fim text,'
          '  realizado boolean not null default false,'
          '  produto references Produto,'
          '  quantidade integer,'
          '  observacao text);')

        self._logger.debug('Creating table "Produto"...')
        connection.executescript('create table Produto ('
          '  tipo not null references ProdutoTipo,'
          '  fornecedor not null references Fornecedor,'
          '  marca not null references Marca,'
          '  fabricante not null references Fabricante,'
          '  medida text not null,'
          '  unidade text not null);')

        self._logger.debug('Creating table "ProdutoTipo"...')
        connection.executescript('create table ProdutoTipo ('
          '  descricao text not null,'
          '  categoria not null references ProdutoCategoria);')

        self._logger.debug('Creating table "ProdutoCategoria"...')
        connection.executescript('create table ProdutoCategoria ('
          '  nome text not null);')


        self._logger.debug('Creating table "Fornecedor"...')
        connection.executescript('create table Fornecedor ('
          '  nome text not null);')


        self._logger.debug('Creating table "Marca"...')
        connection.executescript('create table Marca ('
          '  nome text not null);')


        self._logger.debug('Creating table "Fabricante"...')
        connection.executescript('create table Fabricante ('
          '  nome text not null);')


        # TODO Handle errors

    def database_init_command_ok_handler(self):
        print('Structure created successfully')


class FDCInitializationException(Exception):
    pass
