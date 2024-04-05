from optparse import OptionParser
import json
import os
import pandas as pd

class iperf3_dataParser(object):
    def getOptionParser(self):
        usage = '%prog [ -f FOLDER | -o OUT | -p PLOTFILES | -a AXIS_NAMES | -n PERCENTAGE | -v ]'
        return OptionParser(usage=usage)

    def parseOptions(self, args):
        parser = self.getOptionParser()
        parser.add_option('-f', '--folder', metavar='FILE',
                      type='string', dest='foldername',
                      help='Input folder absolute path. [Input Format: /Users/iperfExp]')

        parser.add_option('-o', '--output', metavar='OUT',
                      type='string', dest='output', default="iperf.png",
                      help='Plot file name. [Input Format: iperf.png]')

        parser.add_option('-p', '--plotfiles', metavar='PLOT_FILES',
                      type='string', dest='plotFiles', default="",
                      help='Choose files to be plotted. If no specified, all files in folder. [Input Format: f1,f2,f3]')
        
        parser.add_option('-a', '--axisNames', metavar='AXIS_NAMES',
                      type='string', dest='axisNames', default="Time(seconds),Throughput(Mbit/s)",
                      help='Choose axis names. If no specified Time(seconds) and Throughput(Mbit/s). [Input Format: f1,f2,f3]')

        parser.add_option('-n', '--percentage', metavar='PERCENTAGE', 
                          type='int', dest='percentage', default='100', 
                          help='Percentage of difference from the average of the values, beyond which the values ​​are discarded')

        parser.add_option('-v', '--verbose',
                      dest='verbose', action='store_true', default=False,
                      help='Verbose debug output to stderr.')

        options, _ = parser.parse_args(args)
        # print(options)
        if not options.foldername:
            parser.error('Foldername is required.')
        else:
            self.foldername = options.foldername

        if options.plotFiles=="":
            self.plotFiles=[]
        else:
            self.plotFiles = map(lambda x:x.strip(), options.plotFiles.split(",")) if "," in options.plotFiles else [options.plotFiles.strip()]

        self.axisNames = map(lambda x:x.strip(), options.axisNames.split(",")) if "," in options.axisNames else [options.axisNames.strip()]

        self.output = options.output

        self.percentage = options.percentage
        return (self.foldername, self.output, list(self.plotFiles), list(self.axisNames), self.percentage)

    def generate_BW(self, iperf):
        """Do the actual formatting."""
        idx=[]
        value=[]
        duration = iperf.get('start').get('test_start').get('duration')
        for i in iperf.get('intervals'):
            for ii in i.get('streams'):
                if (round(float(ii.get('start')), 0)) <= duration:
                    idx.append(round(float(ii.get('start')), 0))
                    value.append(round(float(ii.get('bits_per_second')) / (1024*1024), 3))
        return pd.Series(value, index=idx)

    def get_plotFiles(self,foldername, plotFiles):
        # print(foldername, plotFiles, noPlotFiles)
        if len(plotFiles)==0:
            for root, dirs, files in os.walk(foldername, topdown=False):
                for filename in files:
                    plotFiles.append(filename)
        else:
            for root, dirs, files in os.walk(foldername, topdown=False):
                i=0;
                while i < len(plotFiles):
                    if plotFiles[i] not in files:
                        del plotFiles[i]
                    else:
                        i = i+1;
        
        return plotFiles

    def get_dataset(self, plotFiles, foldername):
        datasetIndex=[]
        raw_arrays=[]
        for name in plotFiles:
            if "json" in name:
                datasetIndex.append(name.replace(".json",""))
            else:
                datasetIndex.append(name)
            file_path = foldername+os.path.sep+str(name)
            with open(file_path, 'r') as fh:
                data = fh.read()

            try:
                iperf = json.loads(data)
            except Exception as ex:  # pylint: disable=broad-except
                print('Could not parse JSON from file (ex): {0}'.format(str(ex)))

            raw_arrays.append(self.generate_BW(iperf))

        dataset=pd.concat(raw_arrays, axis=1)
        dataset.columns=datasetIndex
        dataset.index.names=['start']
        # dataset.apply(lambda x: x.fillna(x.mean(),inplace=True),axis=0)
        dataset = dataset.fillna(method='ffill')

        return dataset