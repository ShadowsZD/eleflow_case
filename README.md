# Data engineering capstone
## BigData Airlines

Para executar, apenas rodar o script main.py, garantindo que existam duas pastas, AIR_CIA e VRA, com os respectivos dados fornecidos

#### Extras:
  - Descrever qual estratégia você usaria para ingerir estes dados de forma incremental caso precise capturar esses dados a cada mes?\
  Alterações no script para update das companhias áereas e integração com uma ferramenta de orquestração (Airflow) para execução periódica.

  - Justifique em cada etapa sobre a escalabilidade da tecnologia utilizada.\
  Podemos escalar o processamento dos json e csvs utilizando uma tecnologia como spark para tratamento e posterior escrita em parquet.
  Na parte do SQL, pode ser adicionado mais máquinas para a replicaçao do dado para leitura. Além disso pode ser aumentado o poder de processamento do servidor
  para suportar mais dados.
  
  - Justifique as camadas utilizadas durante o processo de ingestão até a disponibilização dos dados.\
  Mês a mês pode ser utilizado uma máquina EC2 com airflow para a orquestração, ou até mesmo o crontab da máquina para executar o script mensal.
  Para a escrita dos dados, o script seria incrementado com o boto3 para escrita do dado final no banco, ou até mesmo no s3, usando o como data lake.
