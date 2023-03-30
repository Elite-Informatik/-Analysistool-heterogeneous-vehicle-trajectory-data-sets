# Analysistool-heterogeneous-vehicle-trajectory-data-sets

This is an analysis tool for heterogenous vehicle trajectory data sets.
To execute the application, follow these steps:
1. Set up your own PostgreSQL Database.
2. The application uses the database via an user called "max". The password of max has to be set to "1234". The name of the database should be "example".
3. It is important to also use PosGis since it is used for various filtering methods.
4. There are several json files that are necessary to use the application
5. These json files are located in the src.dictionary path. 
6. They can be created initially with build file in the src folder.
7. To start the application, the main method in the application class has to be executed. 
8. Currently, there is always one dataset in the json file. This dataset does not exist in the database and should not be imported. 
9. Datasets have to be imported first and can be opened afterwards. When using HighD Data, three datasets have to be selected. The order of the datasets does not matter.
