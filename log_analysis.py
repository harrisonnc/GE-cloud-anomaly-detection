#!/usr/env
from data_logs import data_logs
import re

class log_analysis(data_logs):

    def __init__(self):
        super(log_analysis, self).__init__()
        #self.conf_file=data_logs.retrieve_conf_file(self)
        self.white_listed=[]
        self.black_listed=[]
        self.failed_account_anomalies=[]
        log_analysis.retrieve_location_anomaly_settings(self)


    def retrieve_location_anomaly_settings(self,white_list_rfc1911='True'):
        white_list_tag='white_list[001-999]'
        black_list_tag='black_list[001-999]'
        white_listed={}
        black_listed={}

        for line in self.conf_file:
            if re.match('white_list_rfc1911', line):
                white_list_rfc1911=line.split('\'', 1)[1].split('\'',1)[0]
                #print(white_list_rfc1911) #for testing purposes only
        self.conf_file.seek(0,0)
        #print(white_list_rfc1911) #for testing purposes only
        if white_list_rfc1911=='True':
            print(white_list_rfc1911)
            white_listed['10.0.0.0']=8
            white_listed['192.168.0.0']=16
            white_listed['172.16.0.0']=12

        data_logs.set_configuration_values(self=self,tag_value=white_list_tag,conf_value=white_listed,fb_del='\'',
                                           fe_del='/',sb_del='/',se_del='\'')
        data_logs.set_configuration_values(self=self,tag_value=black_list_tag,conf_value=black_listed,fb_del='\'',
                                           fe_del='/',sb_del='/',se_del='\'')
        log_analysis.set_location_lists_regex(self,white_listed,'white')
        log_analysis.set_location_lists_regex(self,black_listed,'black')

    def set_location_lists_regex(self,lists,w_b):
        for key in lists.keys():
            new_key=str()
            for x in range(0,4,1):
                if int(lists[key]) < (8*x):
                    octet_range=pow(2,8)
                else:
                    octet_range=pow(2,((8*(x+1))-int(lists[key])))
                if int(lists[key]) < (8+(8*x)):
                    octet='['+key.split('.',4)[x]+'-'+str(int(key.split('.',4)[x])+octet_range)+')'
                else:
                    octet=key.split('.',4)[x]
                if x < 3:
                    new_key+=octet+'\.'
                else:
                    new_key+=octet
            if w_b == 'white':
                self.white_listed.append(new_key)
            elif w_b == 'black':
                self.black_listed.append(new_key)
            else:
                print('No list to append.')
            print(new_key)

    def location_anomalies(self):
        pass

    def top_logins(self,rows=10):
        return self.formatted_log.groupby('username').size().sort_values(ascending=False).head(rows).to_frame()

    def failed_login_anomaly(self,locked_account=3,interval_sec=300):


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
    print(logFile.white_listed)
    print(len(logFile.white_listed))
    print(logFile.white_listed[0])
    print(logFile.black_listed)
    print(len(logFile.black_listed))
    print(logFile.black_listed[0])
    logFile.failed_login_anomaly()
#    print(master_log.head())
    print(logFile.failed_account_anomalies)
#    print(logFile.formatted_log[logFile.formatted_log.username == 'user-5941']['eventName'])
if __name__ == "__main__":
    main()




#anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]
#anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]['eventName'].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed'])
#failure_count=anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed']).groupby('eventName').size()[1]