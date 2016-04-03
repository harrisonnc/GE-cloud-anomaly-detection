#!/usr/env
import pandas as pd
import re
import operator


class data_logs(object):
    def __init__(self):
        self.conf_file = data_logs.retrieve_conf_file(self)
        self.log_location = data_logs.retrieve_log_location(self, self.conf_file)
        self.file_type = data_logs.retrieve_file_type(self, self.conf_file)
        master_log = data_logs.retrieve_data(self, self.log_location, self.file_type)
        # print(len(master_log))
        self.column_headings = data_logs.retrieve_column_headings(self, self.conf_file)
        # print(column_headings.values())
        self.formatted_log = data_logs.format_data(self, master_log, self.column_headings)
        # print(self.formatted_log.head()) #for troubleshooting purposes only

    def retrieve_conf_file(self):
        conf_file = open('./Configuration/log.conf')
        return conf_file

    def retrieve_log_location(self, conf_file):
        for line in conf_file:
            if re.match('source_file', line):
                return line.split('\'', 1)[1].split('\'', 1)[0]

    def retrieve_file_type(self, conf_file):
        for line in conf_file:
            if re.match('source_file_type', line):
                return line.split('\'', 1)[1].split('\'', 1)[0]

    def retrieve_data(self, log_location, file_type):
        if file_type == 'csv':
            log_data = pd.read_csv(log_location)
            return log_data
        else:
            return 'invalid data type'

    def set_configuration_values(self, tag_value, conf_value, fb_del='\'', fe_del='\'', sb_del='\'', se_del='\''):
        for line in self.conf_file:
            if re.match(tag_value, line):
                conf_value[line.split(fb_del, 1)[1].split(fe_del, 1)[0]] = line.split(sb_del, 1)[1].split(se_del, 1)[0]
        self.conf_file.seek(0, 0)

    def retrieve_column_headings(self, conf_file):
        column_keys = ['standardized_time', 'human_readable_time', 'source_ip', 'destination_ip', 'login_account',
                       'log_source_device', 'log_message']
        column_headings = {}
        for key in column_keys:
            for line in conf_file:
                if re.match(key, line):
                    column_headings[key] = line.split('\'', 1)[1].split('\'', 1)[0]
            self.conf_file.seek(0, 0)
        for line in conf_file:
            if re.match('custom[01-99]', line):
                column_headings[line.split('=', 1)[0]] = line.split('\'', 1)[1].split('\'', 1)[0]
        self.conf_file.seek(0, 0)
        return column_headings

    def format_data(self, log_data, column_headings):
        # print(log_data.columns) #used for debugging only
        # print(column_headings)  #used for debugging only
        formatted_log = pd.DataFrame()
        for key in column_headings:
            if log_data[column_headings[key]].any():
                formatted_log.loc[:, column_headings[key]] = log_data[column_headings[key]]
            else:
                print(column_headings[key])
        return formatted_log

    def search_log(self, search_value, log_category='username'):
        # trimmed_columns=('human_readable_time','source_ip','destination_ip','log_source_device','log_message')
        df_indexed = self.formatted_log.set_index([log_category])
        return df_indexed.loc[[search_value]].sort_values(self.column_headings['standardized_time'])[['startDateTime',
                                                                                                      'srcIp', 'destIp',
                                                                                                      'deviceName',
                                                                                                      'eventName']]

    def log_links(self, log_to_link):
        #print(log_to_link)
        linker_log = log_to_link.reset_index()
        linker = linker_log['username']
        final_linker = []
        #print(linker)
        for n, i in enumerate(linker):
            # print(n)
            final_linker.append(' <a href=\"' + linker[n] + '\">' + linker[n] + '</a>')
        # print('****')
        # print(final_linker)
        # print(str(len(linker))+' : '+str(len(linker_log.groupby('username').groups.keys())))  #for testing purposes only
        #print(linker_log.groupby('username').groups.keys())
        sorted_linker_list = sorted(linker_log.groupby('username').groups.items(), key=operator.itemgetter(1))
        sorted_linker_log = [i[0] for i in sorted_linker_list]
        #print(sorted_linker_log)
        #print(final_linker)
        linker_log['username'] = linker_log['username'].replace(to_replace=sorted_linker_log, value=final_linker)
        linker_log.columns = ['UserName', 'Total']
        return linker_log


def main():
    df = data_logs()
    print(df.head())
    # print(df.search_log('user-7459'))
    # print(df.log_links(df.search_log('user-7459')))
    # conf_file=data_logs.retrieve_conf_file()
    # log_location=data_logs.retrieve_log_location(conf_file)
    # file_type=data_logs.retrieve_file_type(conf_file)
    # master_log=data_logs.retrieve_data(log_loca   tion,file_type)
    # print(len(master_log))
    # column_headings=data_logs.retrieve_column_headings(conf_file)
    # print(column_headings.values())
    # formatted_log=data_logs.format_data(master_log,column_headings)
    # print(formatted_log.head())


#    print(master_log.head())
if __name__ == "__main__":
    main()
