import subprocess
import math
import argparse

def sin_to_cos(sinba):
    return math.sin(math.pi/2. - math.asin(sinba))
def cos_to_sin(cosba):
    return math.cos(math.pi/2. - math.acos(cosba))

def get_br(sinba, m12, tanb, thdm, decay='H  -> h  h', m_A=500):
    output = subprocess.check_output(["./CalcPhys", "125", f"{m_A}", f"{m_A}", f"{m_A}", f"{sinba}", "0.",  "0.", f"{m12}", f"{tanb}", f"{thdm}", "out"])
    try:
        out = [line for line in output.decode().splitlines() if decay in line][0]
        return float(out.split()[-2]), float(out.split()[-1])
    except IndexError: # output doesn't contain H->hh line if B is zero
        return 0., 0.

parser = argparse.ArgumentParser()
parser.add_argument("mass", help="mA = mH = mHp", type=float)
parser.add_argument("cosba", help="cos(b - a)", type=float)
parser.add_argument("tanb", help="tan b", type=float)
parser.add_argument("type", choices=[1, 2, 3, 4], help="2HDM type", type=int)
args = parser.parse_args()

m_A = args.mass
tanb = args.tanb
beta = math.atan(tanb)
m12 = m_A**2 * tanb/(1. + tanb**2) # SM-like limit from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG2HDM
thdm = args.type

sinba = cos_to_sin(args.cosba)

print(f'Calculated sin(b-a) = {sinba}, m12 = {m12} GeV')

output = subprocess.check_output(["./CalcPhys", "125", f"{m_A}", f"{m_A}", f"{m_A}", f"{sinba}", "0.",  "0.", f"{m12}", f"{tanb}", f"{thdm}", "out"])
for line in output.decode().splitlines():
    print(line)
