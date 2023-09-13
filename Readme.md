**Webscraping utilizando Pandas e Selenium com Chrome Webdriver**

Esse pequeno repositório realiza uma busca em: https://cad-app-estruturaje.tse.jus.br/estruturaje-servico-ws/paginas/zonaEleitoral/consultar.faces;

**O que ele faz?**

1. Ele baixa todos os arquivos referentes a cada estado da federação e a zona internacional;
2. Concatena todos os arquivos baixados em um único arquivo e então deleta os desnecessários;
3. Cria um dataframe e adiciona duas novas colunas ao mesmo: Latitude e Longitude;
4. Para cada linha, através da API da nomatim: https://nominatim.openstreetmap.org, realiza três verificações para encontrar as coordenadas;
5. Cria um csv com todas as informações processadas.


**TO-DO**
1. Melhorar o tempo de todo o processamento;
2. Trabalhar no controle de erros;

