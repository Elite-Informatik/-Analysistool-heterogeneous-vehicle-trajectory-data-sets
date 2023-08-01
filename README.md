# Analysistool-heterogeneous-vehicle-trajectory-data-sets

This is an analysis tool for heterogenous vehicle trajectory data sets.
To execute the application, follow these steps:
1. Execute the build file in the src folder. This will create the necessary json files in the src.dictionary path.
2. Install the docker container for PostgreSQL with PostGis. The docker image is: lauraxrb/pseanalysistool
3. If you want to use the a custom database, follow these steps:
    1. The application uses the database via an user called "analysisUser". The password of analysisUser has to be set to "1234". The name of the database should be "Analysistool".
    2. These settings can be changed in the src/dictionary/sql_connection.json file.
    3. It is important to also use PosGis since it is used for various filtering methods.
4. If not done already automatically install the dependencies in the requirements.txt file.
5. To start the application, the main method in the application class has to be executed. 
6. Datasets have to be imported first and can be opened afterwards. When using HighD Data, three datasets have to be selected. 
