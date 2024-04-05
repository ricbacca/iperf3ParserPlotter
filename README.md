# iperf3ParserPlotter

## 1.Introduction
Iperf3 parser plotter is a graphing tool to generate statistical chart for iperf3 experimental result. Iperf3 output json file as result, which is not easy to view straightforwardly. This plotter will transform json data into a line chart, eventually discarding some values based on value's averages.

## 2.Requirements
Ipef3 parser plotter runs on Python, version 2.7+ and 3.3+. Plotting requires matplotlib and pandas to be pre-installed. Replace pip wit pip3 if python3 is used.

```
pip install pandas
pip install matplotlib
```

## 3.Quick start
Execute iperf testing, with Json output configured (-J).

`iperf3 -c 10.99.99.1 -u -b 0 -l 1512 -t 60 -J > prova.json`
 - u = UDP
 - b = BANDWIDTH (0 means unlimited)
 - l = BLOCKS LENGTH in Byte
 - t = experiment duration in seconds
 - J = json output

Run the following command.

```
python3 iperf3_main.py -f ./json_files_folder
```

In default, iperf3 parser plotter will generate a chart eventually with normalized values based on 'percentage' argument.

## 4.Configuration

```
Usage: iperf3_main.py [ -f FOLDER | -o OUT | -p PLOTFILES | -a AXIS_NAMES | -n PERCENTAGE | -v ]

Options:
  -h, --help            show this help message and exit
  -f FILE, --folder=FILE
                        Input folder absolute path. [Input Format:
                        /Users/iperfExp]
  -o OUT, --output=OUT  Plot file name. [Input Format: iperf.png]
  -p PLOT_FILES, --plotfiles=PLOT_FILES
                        Choose files to be plotted. If no specified, all files
                        in folder. [Input Format: f1,f2,f3]
  -a AXIS_NAMES, --axisNames=AXIS_NAMES
                        Choose axis names. If no specified Time(seconds) and
                        Throughput(Mbit/s). [Input Format: f1,f2,f3]
  -n PERCENTAGE, --percentage=PERCENTAGE
                        Percentage of difference from the average of the
                        values, beyond which the values ​​are discarded
  -v, --verbose         Verbose debug output to stderr.
```

**The parameter -f is necessary**, representing input source data.

Iperf3 parser plotter provides other flexible parameters for customizing different user scenarios. We list a few example here.

- plot only two files in input source data folder.

	```	
	python3 iperf3_main.py -f input_folder \
	-p file_1.json,file_2.json
	```

- plot all files, discard (being replaced with average value) the ones different from average values (in his column) more than 15%, also assign different names to axis in graphs.
	
	```
	python3 iperf3_main.py -f input_folder \
	-n 15 \
	-a X_AXIS,Y_AXIS
	```