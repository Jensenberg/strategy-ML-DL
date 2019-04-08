# style-rotation
利用机器学习算法预测沪深300与中证500的强弱

## **hs_zz.ipynb**

1. **策略思想**

   首先对中证800的成分股，按照因子值进行**降序**排序，对排名为前50名的成分股的日收益率取平均作为“**因子收益率**”，对m个因子采用上述操作，得到输入$${\bf {X= (x_1, x_2, ..., x_n), x_t }} =(x^{(1)}_t, x^{(2)}_t , ..., x^{(m)}_t)^T​$$ 

   用沪深300的日收益率减去同一天中证500的日收益率，得到两者的收益率之差，大于等于0标记为1，小于0标记为-1，得到输出

   $$\bf Y=(y_1, y_2, ... , y_n)​$$

   运用${\bf {x_t}}$预测$y_{t+1}$:

   $$f({\bf {x_t}}) \rightarrow y_{t+1}​$$

2. **涉及的因子**

   （1）**方向明确**的因子，如**因子值越大越好**的因子：

   - **roe_ttm**：最近12个月净资产收益率

   * **roe_growth**：净资产收益率增长率

   * **ebit2ev**：企业价值乘数

   * **ep_ttm**：最近12个月市盈率倒数ep_ttm

   * **bp_lr**：最近报告期市净率

   （2）**方向不明确**的因子：

   * **weekly_return**：周收益率
   * **momentum_1m**：一个月动量
   * **momentum_12m**：12个月动量
   * **volatility**：波动率
   * **amplitude**：振幅
   * **ln_market_cap**：对数市值
   * **volume**：成交量

   对于方向不明确的因子，可以考虑取因子值排名**后50名**的成分股的日收益率作为“因子收益率”，相当于刻画**反转效应**

3. **算法**

   Logistic回归，训练集大小1000-1500，测试集150-250，k折交叉验证优化参数

4. **数据处理**

   对特征进行标准化，**并删除训练集中日收益率过小的样本**

## **style_svc.ipynb** 

1. **策略思想与数据**

   将特征数据换成了Barra的十个风格因子，在构建因子的时候考虑了因子的指数平滑，引入了半衰期，以及对于同一概念的多种刻画指标的综合平均：

   * **Beta**

   * **Size**

   * **Momentum**

   * **Growth**

   * **Book-to-Price**

   * **None-linear Size**: 

     $Cube\ of\ Size​$

   * **Residual Volatility**:

     $0.74 \times Daily\ Standard\ Deviation + 0.16 \times Cumulative\ Range + 0.10 * History\ Sigma$

   * **Liquidity**:

     $0.35\times Share\ Turnover(One\ Month) + 0.35 \times Average\ Share\ Turnover\ (Trailing\ 3\ Months)$ 

      $+\ 0.3 \times Average\ Share\ Turnover\ (Trailing\ 12\ Months) $

   * **Earning Yield**:

     $0.68 \times Predicted \ Earnings \ to \ Price + 0.21 \times Cash \ Earnings \ to \ Price + 0.11 \times Trailing \ Earing \ to \ Price$

   * **Leverage**

     $0.38 \times Market \ Leverage + 0.35 \times Debt \ to \ Asset + 0.27 \times \ Book \ Leverage$

2. **算法**

   SVC，网格搜索

## **策略的评价指标** 

最长回撤期，最大回撤，年化收益率，Calmar比率，夏普比率，胜率











