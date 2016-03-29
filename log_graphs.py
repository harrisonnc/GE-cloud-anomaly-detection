import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from flask import Flask, send_file
app = Flask(__name__)
from data_logs import data_logs


class graphics(data_logs):
    global graphArrays
    graphArrays=[]

    def totalGraph(self):
        df = data_logs()
        times = df.formatted_log['startTime'].tolist()
        times.sort()
        counter=1
        clumpcount=0
        time=times[0]
        clumps=[]
        clumptime=[]
        clumps.append(0)
        clumptime.append(time)

        for count in range(0, len(df.formatted_log)):
            if times[count]-time>=1200000:
                time=times[count]
                clumpcount=count-clumpcount
                clumptime+=[time]
                clumps+=[clumpcount]
                counter=counter+1
            elif count==len(df.formatted_log)-1:
                time=times[count]
                clumpcount=count-clumpcount
                clumptime+=[time]
                clumps+=[clumpcount]
                counter=counter+1
            else:
                pass

        graphArrays.append(clumptime)
        graphArrays.append(clumps)
        #plt.plot(clumptime, clumps)
        #plt.axis('tight')
        #plt.title('Total Logins over Time')
        #plt.ylabel('login attempts')
        #plt.xlabel('time (epoch)')
        #plt.tight_layout()
        #plt.savefig('./static/img/totalGraph.png')
        #plt.show()



    def failGraph(self):
        df = data_logs()

        times = df.formatted_log['startTime'].tolist()
        eventList = df.formatted_log['eventName'].tolist()
        eventList.sort()
        failure_value = ['A Kerberos authentication ticket (TGT) was rejected', 'Web Service Login Failed']
        times.sort()
        failcount = 0
        fails = []
        failtimes = []


        for count1 in range(1, len(df.formatted_log)):
            if eventList[count1] == failure_value[0]:
                fails += [failcount]
                failcount += 1
                failtimes += [times[count1]]
            else:
                fails+=[failcount]
                failtimes+= [times[count1]]
        graphArrays.append(failtimes)
        graphArrays.append(fails)
        #plt.clf()
        #plt.plot(failtimes, fails)
        #plt.axis('tight')
        #plt.title('Failed Logins over Time')
        #plt.ylabel('failed attempts')
        #plt.xlabel('time (epoch)')
        #plt.tight_layout()
        #plt.savefig('./static/img/failGraph.png')
        #plt.show()

    def successGraph(self):
        df = data_logs()
        times = df.formatted_log['startTime'].tolist()
        eventList = df.formatted_log['eventName'].tolist()
        eventList.sort()
        failure_value = ['A Kerberos authentication ticket (TGT) was rejected', 'Web Service Login Failed']
        times.sort()
        successCount = 1
        passes = []
        passtimes = []
        fails=0
        passcount=0
        time=times[0]
        passes.append(0)
        passtimes.append(time)


        #while failure_value[0] in eventList:
         #   eventList.remove(failure_value[0])

        for count in range(0, len(df.formatted_log)):
            if eventList[count] == failure_value[0]:
                fails=fails+1
            if times[count]-time>=1200000:
                time=times[count]
                passcount=count-passcount
                passtimes+=[time]
                passes+=[passcount-fails]
                successCount=successCount+1
            elif count==len(eventList)-1:
                time=times[count]
                passcount=count-passcount
                passtimes+=[time]
                passes+=[passcount-fails]
                successCount=successCount+1
            else:
                pass

        graphArrays.append(passtimes)
        graphArrays.append(passes)
        #plt.plot(passtimes, passes)
        #plt.axis('tight')
        # plt.axis([times[0],times[len(df.formatted_log)-1],0,logins[len(logins)-1]])
        #plt.title('Successful Logins over Time')
        #plt.ylabel('successful attempts')
        #plt.xlabel('time (epoch)')
        #plt.tight_layout()
        #plt.savefig('./static/img/successGraph.png')
        #plt.show()

    def main(self):
        graph = graphics()
        graph.totalGraph()
        graph.successGraph()
        graph.failGraph()
        plt.plot(graphArrays[0],graphArrays[1],'b',graphArrays[2],graphArrays[3],'g',graphArrays[4],graphArrays[5],'r')
        blue_patch = mpatches.Patch(color='blue', label='Total Logins')
        green_patch = mpatches.Patch(color='green', label='Successful Logins')
        red_patch = mpatches.Patch(color='red', label='Failed Logins')
        plt.legend(handles=[blue_patch,green_patch,red_patch],loc=2,shadow=True)
        plt.title('Login Rates over Time')
        plt.axis('tight')
        plt.savefig('./static/img/combinedGraph.png')

if __name__ == '__main__':
    graph = graphics()
    graph.totalGraph()
    graph.successGraph()
    graph.failGraph()
    plt.plot(graphArrays[0],graphArrays[1],'b',graphArrays[2],graphArrays[3],'g',graphArrays[4],graphArrays[5],'r')
    blue_patch = mpatches.Patch(color='blue', label='Total Logins')
    green_patch = mpatches.Patch(color='green', label='Successful Logins')
    red_patch = mpatches.Patch(color='red', label='Failed Logins')
    plt.legend(handles=[blue_patch,green_patch,red_patch],loc=2,shadow=True)
    plt.title('Login Rates over Time')
    plt.axis('tight')
    plt.savefig('./static/img/combinedGraph.png')
    #plt.show()