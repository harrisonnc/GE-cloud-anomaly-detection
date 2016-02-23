#!/usr/env
from data_logs import data_logs
class log_analysis(data_logs):

    def top_logins(self,rows=10):
        return self.formatted_log.groupby('username').size().sort_values(ascending=False).head(rows).to_frame()

    def failed_login_anomaly(self,locked_account=3,interval_sec=300):

        self.failed_account_anomalies=['none']
        account_indexed_log=self.formatted_log.set_index(self.column_headings['login_account'])
        failure_values=['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed']
        for key in self.formatted_log.groupby(self.column_headings['login_account']).groups.keys():
            failed_count=0
            current_account=account_indexed_log.loc[[key]][['eventName','startTime']].sort_values('startTime')
            #print(current_account)
            if current_account.isin(failure_values)['eventName'].any():
                failure_count=current_account.isin(failure_values).groupby('eventName').size()[1]
            else:
                failure_count=0
            if failure_count >= locked_account:
                for failed in current_account['eventName'].isin(failure_values):
                    #print(failed)
                    if failed:
                        failed_count += 1
                    else:
                        failed_count = 0
                    if failed_count >= locked_account:
                        self.failed_account_anomalies.append(key)
                        break
        #return self.failed_account_anomalies
    def location_login_anomaly(self,interval_sec=900):
        pass

def main():

    logFile=log_analysis()
    topLogins=logFile.top_logins()
    #loginAnomaly=logFile.failed_login_anomaly()
    #print(loginAnomaly)
    logFile.failed_login_anomaly()
#    print(master_log.head())
    print(logFile.failed_account_anomalies)
#    print(logFile.formatted_log[logFile.formatted_log.username == 'user-5941']['eventName'])
if __name__ == "__main__":
    main()




#anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]
#anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]['eventName'].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed'])
#failure_count=anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed']).groupby('eventName').size()[1]