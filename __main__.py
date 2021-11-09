import csv
from   pathlib                      import Path
from   rohdeschwarz.instruments.vna import Vna


# constants
VNA_IP_ADDRESS   = 'localhost'
VNA_GPIB_ADDRESS = 20  # requires pyvisa, NI VISA


# paths
root_path    = Path(__file__).parent.resolve()
data_path    = root_path / 'data'
vna_log_file = data_path / 'scpi.log'
diagram_file = data_path / 'diagram1.png'
markers_file = data_path / 'markers.csv'

data_path.mkdir(exist_ok=True)


# init vna connection
vna = Vna()
vna.open_tcp(VNA_IP_ADDRESS)

# if using GPIB:
# vna.open('gpib', VNA_GPIB_ADDRESS)

# log scpi and errors
vna.open_log(str(vna_log_file))

# connected?
if not vna.id_string():
    raise Exception('Could not connect to VNA')

# clear previous scpi errors
vna.clear_status()

# start from preset:
#  - Channels: [1]
#  - Diagrams: [1]
#  - Traces:   ['Trc1']
vna.preset()

# configure channel
channel = vna.channel(1)
channel.start_frequency_Hz = 1e9
channel.stop_frequency_Hz  = 8e9
channel.points             = 201
channel.if_bandwidth_Hz    = 1e3
channel.power_dBm          = -10
assert not vna.errors

# configure trace1 (Trc1)
trace1 = vna.trace('Trc1')
trace1.parameter = 'S21'
trace1.format    = 'MLOG'
trace1.autoscale()
assert not vna.errors

# configure trace2 (Trc2)
vna.create_trace('Trc2', channel=1)
trace2           = vna.trace('Trc2')
trace2.parameter = 'S31'
trace2.format    = 'MLOG'
trace2.diagram   = 1  # new traces are hidden by default
trace2.autoscale()
assert not vna.errors

# configure diagram
diagram = vna.diagram(1)
diagram.title = 'S21, S31 Magnitude (dB)'
assert not vna.errors

# configure same markers for each trace
for trace_name in vna.traces:
    trace = vna.trace(trace_name)

    # create three markers
    trace.markers = [1, 2, 3]

    # marker 1 setup
    m1 = trace.marker(1)
    m1.x = 1e9

    # marker 2 setup
    m2 = trace.marker(2)
    m2.x = 2e9

    # marker 3 setup
    m3 = trace.marker(3)
    m3.x = 3e9
    assert not vna.errors

# perform one "manual" sweep
vna.continuous_sweep = False
vna.sweep()
assert not vna.errors

# save markers to csv
with markers_file.open('w') as f:
    # write csv header
    f.write('# trace, marker, x_Hz, y_dB\n')
    f.flush()

    # use csv writer for data
    csv_writer = csv.writer(f)

    for trace_name in vna.traces:
        trace = vna.trace(trace_name)

        for index in trace.markers:
            # write marker data to row
            marker = trace.marker(index)
            csv_writer.writerow([trace_name, marker.name, marker.x, marker.y])
            f.flush()
            assert not vna.errors

# save trace data
for trace_name in vna.traces:
    trace = vna.trace(trace_name)

    # save magnitude dB
    formatted_data_file = data_path / f'{trace_name}-formatted.csv'
    trace.save_data_locally(str(formatted_data_file))

    # save complex data
    complex_data_file = data_path / f'{trace_name}-complex.csv'
    trace.save_complex_data_locally(str(complex_data_file))
    assert not vna.errors

# save screenshot
diagram.save_screenshot_locally(str(diagram_file), image_format='PNG')
assert not vna.errors
