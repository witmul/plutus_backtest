import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta



class backtest:
    def __init__(self, comp, b_day, s_day, weights_factor= None , take_profit=None, stop_loss=None):
        self.comp = comp
        self.b_day = b_day
        self.s_day = s_day
        self.w_factor = weights_factor if weights_factor is not None else np.ones(len(comp))
        self.tp = take_profit if take_profit is not None else 100 * np.ones(len(comp))
        self.sl = stop_loss if stop_loss is not None else np.zeros(len(comp))

    def company_list(self):
        df = pd.DataFrame({"company": self.comp,"start day": self.b_day,"end day": self.s_day,"weights factor": self.w_factor,
                           "take profit": self.tp,"stop loss": self.sl})
        df = df.set_index(df['company'])
        for x in df.index:
            if df.loc[x, "weights factor"] < 0:
                a = df.loc[x, "stop loss"]
                b = df.loc[x, "take profit"]
                df.loc[x,"take profit"] = (1-a) + 1
                df.loc[x,"stop loss"] = 1 - (b-1)
        self.company_list = df

# FOR DETAILED VIEW Adding one day to first buy and last sell dates
    def date_plus_one (self, d):
        str_date = d
        date = datetime.strptime(str_date, "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        back_to_str = datetime.strftime(modified_date, "%Y-%m-%d")
        return back_to_str

    def consolidated_table_detailed(self):
        backtest.company_list(self)
        df_1 = self.company_list
        initial_df = pd.DataFrame()

        for com, b_d, s_d in zip(df_1["company"], df_1["start day"], df_1["end day"]):
            data = yf.download(com, start=backtest.date_plus_one(self, b_d), end=backtest.date_plus_one(self, s_d))
            data["Ticker"] = com
            initial_df = pd.concat([initial_df, data])
        df_close = initial_df[["Ticker", "Adj Close"]]
        df_close.columns = ['ticker', 'close_price']
        df_open = initial_df[["Ticker", "Open"]]
        df_open.columns = ['ticker', 'open']
        open_price = df_open.groupby('ticker').first()
        em1 = pd.DataFrame()
        em2 =pd.DataFrame()
        for x in open_price.index:
            get_open = open_price.loc[x]
            get_end = df_close[df_close['ticker']==x]
            fake_df = pd.DataFrame(index=get_end.index, columns=['ticker', 'close_price'])
            fake_df = pd.DataFrame(fake_df.iloc[0]).T
            fake_df.iloc[0, 0] = x
            fake_df.iloc[0, 1] = get_open.values[0]
            merged_df = fake_df.append(get_end)
            merged_df['daily_change']=merged_df['close_price'].pct_change()
            merged_df = merged_df.iloc[1:]
            aux_df = merged_df[['ticker', 'close_price']]
            work_df = merged_df[['ticker', 'daily_change']]
            em1 = em1.append(aux_df)
            em2 = em2.append(work_df)
        dc = em2.pivot_table(index=em2.index, columns='ticker', values='daily_change')
        dc = dc[self.comp]
        dc = dc.replace([np.inf, -np.inf], np.nan)
        dc = dc.fillna(0)
        dc = dc.apply(pd.to_numeric)
        aux = em1.pivot_table(index=em2.index, columns='ticker', values='close_price')
        aux = aux[self.comp]
        aux = aux.replace([np.inf, -np.inf], np.nan)
        aux = aux.fillna(0)
        aux = aux.apply(pd.to_numeric)
        self.auxiliar_df = aux
        self.detailed_return = dc

        return self.detailed_return


    def portfolio_construction(self):
        binary_weights = self.auxiliar_df / self.auxiliar_df
        binary_weights.fillna(value=0, inplace=True)
        fac_summing = np.sum(abs(np.array(self.w_factor)))
        dist = np.array(self.w_factor) / fac_summing
        dist_df = pd.DataFrame(index= self.comp, data = self.w_factor).T
        weights_df = binary_weights * dist
        for z in weights_df.index:
            if abs(weights_df.loc[z]).sum()!=1:
                act = weights_df.loc[z][weights_df.loc[z]!=0]
                act_df = dist_df[act.index]
                new_dist =np.array(act_df)/np.sum(abs(np.array(act_df)))
                new_dist_frame = pd.DataFrame(columns = act.index, data = new_dist).T
                for i in new_dist_frame.index:
                    weights_df.loc[z,i] =float(new_dist_frame.loc[i].values)


        accu = (self.detailed_return + 1).cumprod()
        for x in accu.columns:
            q1 = accu[x]
            for y in q1:
                if y> self.company_list.loc[x, 'take profit']:
                    q1.iloc[q1.values.tolist().index(y)+1:] =0
                if y< self.company_list.loc[x, 'stop loss']:
                    q1.iloc[q1.values.tolist().index(y) + 1:] = 0
        aux_table_2 = accu* binary_weights
        new_binary_weights = aux_table_2/aux_table_2
        new_binary_weights.fillna(value=0, inplace=True)
        weights_df = new_binary_weights * dist
        for z in weights_df.index:
            if abs(weights_df.loc[z]).sum() != 1:
                act = weights_df.loc[z][weights_df.loc[z] != 0]
                act_df = dist_df[act.index]
                new_dist = np.array(act_df) / np.sum(abs(np.array(act_df)))
                new_dist_frame = pd.DataFrame(columns=act.index, data=new_dist).T
                for i in new_dist_frame.index:
                    weights_df.loc[z, i] = float(new_dist_frame.loc[i].values)

        port_performance = weights_df * self.detailed_return
        port_performance['Sum'] = port_performance.sum(axis=1)
        port_performance['Sum'] = port_performance['Sum'] + 1
        port_performance['Accumulation'] = port_performance['Sum'].cumprod()

        self.final_portfolio = port_performance
        return self.final_portfolio

    def ploting (self):
        backtest.consolidated_table_detailed(self)

        fig2 = plt.figure(figsize=(15, 7))
        ax2 = fig2.add_subplot(1, 1, 1)
        self.detailed_return["Cumulative return"].plot(ax=ax2)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Cumulative return')
        ax2.set_title('Portfolio Cumulative Returns')
        plt.show()

    def general_statistic(self):
        obj = self.final_portfolio
        pdr = obj['Sum'] -1
        self.port_mean = pdr.mean()
        self.port_mean_pct = self.port_mean * 100
        self.port_std = pdr.std()
        self.LPM_0 = len(pdr[pdr<0])/len(pdr)
        self.LPM_1 = pdr.clip(upper=0).mean()
        self.LPM_2 = pdr.clip(upper=0).std()
        topless_pdr = pdr[pdr<self.port_std]
        botless_prd = topless_pdr[topless_pdr>-self.port_std]
        self.inner_mean = botless_prd.mean()
        obj_only_stocks =obj.drop(columns=['Sum', 'Accumulation'])
        self.stocks_mean = obj_only_stocks.mean()
        self.top_per = self.stocks_mean.nlargest(1)
        self.worst_per = self.stocks_mean.nsmallest(1)
        self.trade_length = len(pdr)

    def Var_and_CVaR(self):
        VaR_95 = -1.65 * self.port_std * np.sqrt(self.trade_length)
        VaR_99 = -2.33 * self.port_std * np.sqrt(self.trade_length)
        CVaR = self.LPM_1/self.LPM_0
        print(f'There is 95% confidence that we will not lose more than {round(100*VaR_95,2)} % of your portfolio in a given {self.trade_length} period.')
        print(f'There is 99% confidence that we will not lose more than {round(100*VaR_99,2)} % of your portfolio in a given {self.trade_length} period.')
        print(f'Expected loss that occur beyond the shortfall is {round(CVaR,4)}.')
    def puzzle_assembly(self, dic):
        return

