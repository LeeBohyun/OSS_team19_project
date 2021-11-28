# Stock Trading AI bot

-   Opensource Software Project
-   Team 19

![image](https://user-images.githubusercontent.com/55489991/143690155-ead4367b-614f-4ab1-8411-d18785df38f7.png)

## Background

Interest in the stock trading AI bot is increasing. Many researchers are developing innovatory Ai algorithms, but it is not easy for a normal person to understand. Using these algorithms to implement an AI bot is even harder. So many people spend their time and money learning how to implement AI bots which work as they want. So, we plan to implement a stock trading AI bot with a user-friendly web interface in which the users can customize the functions, such as alarms and prediction algorithm hyper-parameters so that they can make the AI bots work as they want.

## Prerequisites

-   In window OS, you have to install python 3.8 and pip3.
-   Install pandas_datareader, numpy, pandas, sklearn, and tqdm package.

```bash
$ pip3 install pandas_datareader
$ pip3 install numpy
$ pip3 install sklearn
$ pip3 install pandas
$ pip3 install tqdm
```

## How to run the application

1. Clone the repository to your local device.

```bash
$ git clone https://github.com/LeeBohyun/OSS_team19_project.git
```
2. Unzip the file to the directory.
```bash
$ unzip OSS_team19_project.zip
```
3. Open a powershell prompt in the directory where your source code is. Then run the python file main.py.
```bash
$ python3 main.py
```

4. Open file index.html in public directory, or just load 127.0.0.1:3000/ in your chrome. Either way, it will show you the main page of the application.

![image](https://user-images.githubusercontent.com/55489991/143690402-d60f2d5e-3f64-4136-a18a-c900c5798eec.png)

## Main Functions of Stock Trading AI bot

1. Customizing: In settings page`(main page-> menu -> settings)`, there are parameters like expected risk, investment boundaries, and whether to invest in long term or short term.
2. Cart: In settings page`(main page-> menu -> cart)`, we have a shopping cart that users can put stocks in and compare them. It sorts their rank based on the probability of success. Users can use this information to invest more effectively.
3. AI prediction & recommendation: In mypage`(main page-> menu -> mypage)`, in order to predict the expected benefit and loss, we use machine learning algorithms and display the results to the use in that page. It also displays the stocks that user purchased.

## How to extend our work

You can fork our repository and create pull request. Drafts are provided in our repository.

## License

[MIT](https://github.com/LeeBohyun/OSS_team19_project/blob/main/LICENSE)
