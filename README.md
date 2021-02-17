# Trading Strategy Simulation
### 📈 Comparing weekly vs monthly dollar-cost averaging trading 

This repository explores the topic of dollar-cost averaging strategy for investing,and how risk and return of assets could change as the investment interval varies.

We are typically interested in comparing weekly (5-day) vs monthly (20-day) investment frequency. The dataset is pulled via this python package [yahoofinancials](https://github.com/JECSand/yahoofinancials). We do backtesting by randomly sampling historical prices over a 5-year period since 2016 to construct portfolios, and use hypothesis testing to see if there's any significant difference between risks and returns over the study period.

You can also find a writeup of findings in this notebook on my website [here](https://www.chuxinhuang.com/).

**Getting started**

In order to run the notebook, you need to have all required packages installed, run
```
pip3 install -r requirements.txt
```
### 📬 Wanna to stay in touch 

I tweet about data, tech, china and art [@chuxin_h](https://twitter.com/chuxin_h) and stay up-to-date by subscribing to my [newsletter](https://cantabile.substack.com/).

> *Disclaimer*
>The work in this notebook is provided for informational purposes only, and should not be relied upon as legal, businesses, investment or tax advice. References to any securities or digital assets are for illustrative purposes only, and do not constitute an investment recommendation or offer to provide investment advisory services.
