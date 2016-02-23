#!/usr/env
import pandas as pd
import re
class data_logs(object):
    def __init__(self):
        self.conf_file=data_logs.retrieve_conf_file()
        self.log_location=data_logs.retrieve_log_location(self,self.conf_file)
        self.file_type=data_logs.retrieve_file_type(self,self.conf_file)
        master_log=data_logs.retrieve_data(self,self.log_location,self.file_type)
        #print(len(master_log))
        self.column_headings=data_logs.retrieve_column_headings(self,self.conf_file)
        #print(column_headings.values())
        self.formatted_log=data_logs.format_data(self,master_log,self.column_headings)
        #print(self.formatted_log.head())
    def retrieve_conf_file():
        conf_file = open('./Configuration/log.conf')
        return conf_file
    def retrieve_log_location(self,conf_file):
        for line in conf_file:
            if re.match('source_file', line):
                return line.split('\'', 1)[1].split('\'',1)[0]
    def retrieve_file_type(self,conf_file):
        for line in conf_file:
            if re.match('source_file_type', line):
                return line.split('\'', 1)[1].split('\'',1)[0]
     #   return re.search('source_file',conf_file)
    def retrieve_data(self,log_location, file_type):
        if file_type == 'csv':
            log_data = pd.read_csv(log_location)
            return log_data
        else:
            return 'invalid data type'
    def retrieve_column_headings(self,conf_file):
        column_keys=['standardized_time','human_readable_time','source_ip','destination_ip','login_account',
                     'log_source_device','log_message']
        column_headings={}
        for key in column_keys:
            for line in conf_file:
                if re.match(key, line):
                    column_headings[key]=line.split('\'', 1)[1].split('\'',1)[0]
                    break
        for line in conf_file:
            if re.match('custom[01-99]', line):
                column_headings[line.split('=', 1)[0]]=line.split('\'', 1)[1].split('\'',1)[0]
        return column_headings
    def format_data(self,log_data, column_headings):
        #print(log_data.columns) #used for debugging only
        #print(column_headings)  #used for debugging only
        formatted_log=pd.DataFrame()
        for key in column_headings:
            if log_data[column_headings[key]].any():
                formatted_log.loc[:,column_headings[key]]=log_data[column_headings[key]]
            else:
                print(column_headings[key])
        return formatted_log
    #def analyze_data():

def main():
    df=data_logs()
    print(df.formatted_log.head())
    #conf_file=data_logs.retrieve_conf_file()
    #log_location=data_logs.retrieve_log_location(conf_file)
    #file_type=data_logs.retrieve_file_type(conf_file)
    #master_log=data_logs.retrieve_data(log_location,file_type)
    #print(len(master_log))
    #column_headings=data_logs.retrieve_column_headings(conf_file)
    #print(column_headings.values())
    #formatted_log=data_logs.format_data(master_log,column_headings)
    #print(formatted_log.head())
#    print(master_log.head())
if __name__ == "__main__":
    main()