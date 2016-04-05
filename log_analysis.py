#!/usr/env
from data_logs import data_logs
import re
import pandas as pd


class log_analysis(data_logs):
    def __init__(self):
        super(log_analysis, self).__init__()
        # self.conf_file=data_logs.retrieve_conf_file(self)
        self.white_listed = []
        self.black_listed = []
        self.failed_account_anomalies = []
        self.event_indexed = self.formatted_log.set_index(['eventName'])
        self.failure_values = ['A Kerberos authentication ticket (TGT) was rejected', 'Web Service Login Failed']
        log_analysis.retrieve_location_anomaly_settings(self)

    def retrieve_location_anomaly_settings(self, white_list_rfc1918='True'):
        white_list_tag = 'white_list[001-999]'
        black_list_tag = 'black_list[001-999]'
        white_listed = {}
        black_listed = {}

        for line in self.conf_file:
            if re.match('white_list_rfc1918', line):
                white_list_rfc1918 = line.split('\'', 1)[1].split('\'', 1)[0]
                # print(white_list_rfc1918) #for testing purposes only
        self.conf_file.seek(0, 0)
        # print(white_list_rfc1918) #for testing purposes only
        if white_list_rfc1918 == 'True':
            # print(white_list_rfc1918)
            white_listed['10.0.0.0'] = 8
            white_listed['192.168.0.0'] = 16
            white_listed['172.16.0.0'] = 12

        data_logs.set_configuration_values(self=self, tag_value=white_list_tag, conf_value=white_listed, fb_del='\'',
                                           fe_del='/', sb_del='/', se_del='\'')
        data_logs.set_configuration_values(self=self, tag_value=black_list_tag, conf_value=black_listed, fb_del='\'',
                                           fe_del='/', sb_del='/', se_del='\'')
        log_analysis.set_location_lists_regex(self, white_listed, 'white')
        log_analysis.set_location_lists_regex(self, black_listed, 'black')

    def set_location_lists_regex(self, lists, w_b):
        for key in lists.keys():
            new_key = str()
            for x in range(0, 4, 1):
                if int(lists[key]) < (8 * x):
                    octet_range = pow(2, 8)
                else:
                    octet_range = pow(2, ((8 * (x + 1)) - int(lists[key])))
                if int(lists[key]) < (8 + (8 * x)):
                    octet = '[' + key.split('.', 4)[x] + '-' + str(int(key.split('.', 4)[x]) + octet_range) + ')'
                else:
                    octet = key.split('.', 4)[x]
                if x < 3:
                    new_key += octet + '\.'
                else:
                    new_key += octet
            if w_b == 'white':
                self.white_listed.append(new_key)
            elif w_b == 'black':
                self.black_listed.append(new_key)
            else:
                print('No list to append.')
                print(new_key)

    def horizontal_anomaly(self):
        pass

    def top_logins(self, rows=10):
        return self.formatted_log.groupby('username').size().sort_values(ascending=False).head(rows).to_frame()

    def top_successful_logins(self, rows=10):
        return self.event_indexed.loc[~self.event_indexed.index.isin(self.failure_values)].groupby(
            'username').size().sort_values(ascending=False).head(rows).to_frame()

    def top_failed_logins(self, rows=10):
        return self.event_indexed.loc[self.event_indexed.index.isin(self.failure_values)].groupby(
            'username').size().sort_values(ascending=False).head(rows).to_frame()

    def failed_login_anomaly(self, locked_account=3, interval_sec=300):

        duplicate_failure_values = 'A Kerberos authentication ticket (TGT) was rejected'
        unique_failure_values = ['A Kerberos authentication ticket (TGT) was rejected', 'Web Service Login Failed']
        account_indexed_log = self.formatted_log[self.formatted_log.eventName != duplicate_failure_values]
        account_indexed_log = account_indexed_log.set_index(self.column_headings['login_account'])

        failed_logins = self.formatted_log.set_index(['eventName']).loc[unique_failure_values].groupby(
            'username').groups.keys()
        print(failed_logins)
        print(len(failed_logins))
        for key in failed_logins:
            failed_count = 0
            # print(key)
            current_account = account_indexed_log.loc[[key]][['eventName', 'startTime']].sort_values('startTime')
            # print(current_account)
            #            if current_account.isin(failure_values)['eventName'].any():
            # print(current_account.eventName)
            #            current_account=current_account[current_account.eventName != duplicate_failure_values]
            failure_count = current_account.isin(unique_failure_values).groupby('eventName').size()[1]
            #            else:
            #                failure_count=0
            if failure_count >= locked_account:
                for failed in current_account['eventName'].isin(unique_failure_values):
                    # print(failed)
                    if failed:
                        failed_count += 1
                    else:
                        failed_count = 0
                    if failed_count >= locked_account:
                        self.failed_account_anomalies.append(
                            [key, current_account.reset_index().set_index(['eventName'])
                            .loc[current_account.reset_index().set_index(['eventName'])
                            .index.isin(unique_failure_values)].groupby('username')
                            .size()[0]])
                        break

        # for key in self.formatted_log.groupby(self.column_headings['login_account']).groups.keys():
        #            failed_count=0
        #            current_account=account_indexed_log.loc[[key]][['eventName','startTime']].sort_values('startTime')
        #            #print(current_account)
        #            if current_account.isin(failure_values)['eventName'].any():
        #                failure_count=current_account.isin(failure_values).groupby('eventName').size()[1]
        #            else:
        #                failure_count=0
        #            if failure_count >= locked_account:
        #                for failed in current_account['eventName'].isin(failure_values):
        #                    #print(failed)
        #                    if failed:
        #                        failed_count += 1
        #                    else:
        #                        failed_count = 0
        #                    if failed_count >= locked_account:
        #                        self.failed_account_anomalies.append(key)
        #                        break

        test_df = pd.DataFrame(self.failed_account_anomalies, columns=['username', 'Total'])
        return test_df

    #        return self.failed_account_anomalies


    def location_login_anomaly(self, interval_sec=900):
        df_cleaned = self.formatted_log[~self.formatted_log['srcIp'].str.contains('^128\\.172.*|^192\\.168.*')]
        df_cleaned_noDup = df_cleaned.drop_duplicates(['username', 'srcIp'])
        return df_cleaned_noDup.set_index(['srcIp']).groupby('username').size()[df_cleaned_noDup.set_index(['srcIp'])
                                                                                    .groupby('username')
                                                                                    .size().values > 3].reset_index()\
            .sort_values([0], ascending=False)


def main():
    logFile = log_analysis()
    topLogins = logFile.top_logins(15)
    # print(topLogins)
    # print(logFile.log_links(logFile.top_logins(15)))
    # loginAnomaly=logFile.failed_login_anomaly()
    # print(loginAnomaly)
    #    print(logFile.top_successful_logins(15))
    #    print(logFile.top_failed_logins(15))
    print(logFile.white_listed)
    print(len(logFile.white_listed))
    #    print(logFile.white_listed[0])
    #    print(logFile.black_listed)
    #    print(len(logFile.black_listed))
    #    print(logFile.black_listed[0])
    print(logFile.location_login_anomaly())


#    print(master_log.head())
#    print(logFile.failed_account_anomalies)
#    print(logFile.formatted_log[logFile.formatted_log.username == 'user-5941']['eventName'])

if __name__ == "__main__":
    main()




# anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]
# anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])]['eventName'].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed'])
# failure_count=anonymousfiltered[['eventName','startTime']].sort_values('startTime').loc[anonymous_indexed.index.isin(['user-9618'])].isin(['A Kerberos authentication ticket (TGT) was rejected','Web Service Login Failed']).groupby('eventName').size()[1]
