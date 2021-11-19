from   cmath   import phase
import csv
from   gimbal  import Gimbal
from   pathlib import Path
from   rohdeschwarz.instruments.vna import Vna


# constants
VNA_IP_ADDRESS   = '192.168.86.199'
VNA_GPIB_ADDRESS = 20  # requires pyvisa, NI VISA
POSITIONS        = [1, 2, 3, 4, 5]
FREQUENCIES_Hz   = [1e9, 2e9, 3e9, 4e9, 5e9, 6e9, 7e9, 8e9]

# paths
root_path = Path(__file__).parent.resolve()
data_path = root_path / 'data'
data_path.mkdir(exist_ok=True)

# file paths
log_file  = root_path / 'vna.log'
data_file = root_path / 'data' / 'data.csv'

# init vna connection
vna = Vna()
vna.open_tcp(VNA_IP_ADDRESS)

# if using GPIB:
# vna.open('gpib', VNA_GPIB_ADDRESS)

# log scpi and errors
vna.open_log(str(log_file))

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

# configure channel for CW
channel = vna.channel(1)
channel.sweep_type      = 'POIN'
channel.points          = 1
channel.if_bandwidth_Hz = 1e3
channel.power_dBm       = -10
assert not vna.errors

# configure trace
trace = vna.trace('Trc1')
trace.parameter = 'S21'
assert not vna.errors

# stop sweeping
vna.manual_sweep = True

# init gimbal
gimbal = Gimbal()

# perform CW sweeps
data = []
for freq_Hz in FREQUENCIES_Hz:
    print(f'freq: {freq_Hz}')
    # set CW frequency
    channel.frequency_Hz = freq_Hz

    for position in POSITIONS:
        print(f'  position: {position}')

        # position gimbal
        gimbal.position = position
        gimbal.wait_for_position()

        # scpi to start sweep
        vna.start_sweeps()

        # scpi to block until sweep end
        vna.pause(timeout_ms=10_000)

        # retrieve complex data (re, im)
        s21 = trace.y_complex[0]
        data.append([freq_Hz, position, abs(s21), phase(s21)])

# write csv
with data_file.open('w') as f:
    csv_writer = csv.writer(f)

    # write header
    header = ['freq_Hz', 'position', 'abs(s21)', 'phase_rad(s21)']
    csv_writer.writerow(header)

    # write data
    csv_writer.writerows(data)
