from pathlib                      import Path
from rohdeschwarz.instruments.vna import Vna


# constants
VNA_IP_ADDRESS   = '192.168.86.199'
VNA_GPIB_ADDRESS = 20  # requires pyvisa, NI VISA


# paths
root_path    = Path(__file__).parent.resolve()
data_path    = root_path / 'data'
vna_log_file = data_path / 'scpi.log'
diagram_file = data_path / 'diagram1.png'
formatted_trace_data_file = data_path / 'trc1-formatted.csv'
complex_trace_data_file   = data_path / 'trc1-complex.csv'

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
channel.stop_frequency_Hz  = 20e9
channel.points             = 201
channel.if_bandwidth_Hz    = 1e3
channel.power_dBm          = -10
assert not vna.errors

# configure trace
trace = vna.trace('Trc1')
trace.parameter = 'S21'
trace.format    = 'MLOG'
trace.autoscale()
assert not vna.errors

# configure diagram
diagram = vna.diagram(1)
diagram.title = 'S21 Magnitude (dB)'
assert not vna.errors

# perform one "manual" sweep
vna.continuous_sweep = False
vna.sweep()
assert not vna.errors

# save trace data
trace.save_data_locally(str(formatted_trace_data_file))
trace.save_complex_data_locally(str(complex_trace_data_file))
assert not vna.errors

# save diagram screenshot
diagram.save_screenshot_locally(str(diagram_file), image_format='PNG')
assert not vna.errors
