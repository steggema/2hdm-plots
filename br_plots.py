import subprocess
import math
from tqdm import tqdm

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
        return 0.000000001, 0.0000000001

boson_to_label = { # B2G-23-002 convention
    'A': 'A',
    'H': 'X',
    'h': 'H',
}


m_A = 500.
tanb = 5
beta = math.atan(tanb)
m12 = 0.
m12 = math.cos(beta)*math.sin(beta)*m_A**2
m12 = m_A**2 * tanb/(1. + tanb**2) # SM-like limit from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG2HDM
thdm = 2

print(f'General parameters: tan(beta) = {tanb}, m12 = {m12}, type = {thdm}')

decay = 'H  -> h  h'
# decay = 'A  -> Z  h'

for cosba in [0, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1]:
    sinba = cos_to_sin(cosba)
    
    width, br = get_br(sinba, m12, tanb, thdm, decay)
    
    print(f'BR({decay}) for cos(beta - alpha) = {cosba:.3f} is {br:.3f}; partial width {width:.3f} ')



import ROOT
from tdrstyle import setTDRStyle
style = setTDRStyle()
style.SetPalette(ROOT.kFuchsia)
ROOT.TColor.InvertPalette()
style.SetNumberContours(256)


def make_hist(thdm, cosba, decay='H  -> h  h', decay_tag='Htohh'):
    style.SetOptStat(0)
    h2 = ROOT.TH2F('B', '', 75, 250., 1000., 99, 0.2, 20.)

    print(f'\nGeneral parameters: cos(beta - alpha) = {cosba},  type = {thdm}')
    sinba = cos_to_sin(cosba)

    for i in tqdm(range(99)):
        tanb = (i+1) * 0.1
        # beta = math.atan(tanb)
        for j in range(75):
            m_A = 250. + j*10.
            m12 = m_A**2 * tanb/(1. + tanb**2) # SM-like limit from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG2HDM - it's the same as the line below

            width, br = get_br(sinba, m12, tanb, thdm, decay, m_A)
            
            # print(f'BR({decay}) for tanb = {tanb} m_A = {m_A:.0f} is {br:.3f} partial width {width:.3f} ')
            h2.SetBinContent(j+1, i+1, br)
    style.cd()
    cv = ROOT.TCanvas()
    boson = decay[0]
    h2.GetXaxis().SetTitle('m_{' + f'{boson_to_label[boson]}' + '} [GeV]')
    h2.GetYaxis().SetTitle('tan #beta')
    h2.GetZaxis().SetTitle('#bf{#it{#Beta}}(X #rightarrow HH)' if decay == 'H  -> h  h' else '#bf{#it{#Beta}}(A #rightarrow ZH)')
    h2.SetContour(40)
    h2.Draw('COLZ')

    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(11)
    latex.SetNDC()

    l = cv.GetLeftMargin()
    t = cv.GetTopMargin()
    latex.DrawLatex(l + 0.02, 1-t + 0.02, f'2HDM type {thdm}  cos(#beta - #alpha) = {cosba}')

    cv.SaveAs(f'B_{decay_tag}_type{thdm}_cosba{cosba}.pdf')
    cv.SaveAs(f'B_{decay_tag}_type{thdm}_cosba{cosba}.root')





def make_hist_fixedm(thdm, mass, decay='H  -> h  h', decay_tag='Htohh'):
    style.SetOptStat(0)
    h2 = ROOT.TH2F('B', '', 50, -0.05, 0.05, 99, 0.2, 20.)

    print(f'\nGeneral parameters: m_H = {mass},  type = {thdm}')

    for i in tqdm(range(99)):
        tanb = (i+1) * 0.1
        for j in range(50):
            cosba = -0.05 + j * 0.1/50.
            m_A = mass
            m12 = m_A**2 * tanb/(1. + tanb**2) # SM-like limit from https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCHWG2HDM - it's the same as the line below

            sinba = cos_to_sin(cosba)

            width, br = get_br(sinba, m12, tanb, thdm, decay, m_A)
            
            # print(f'BR({decay}) for tanb = {tanb} m_A = {m_A:.0f} is {br:.3f} partial width {width:.3f} ')
            h2.SetBinContent(j+1, i+1, br)
    style.cd()
    cv = ROOT.TCanvas()

    h2.GetXaxis().SetTitle('cos(#beta - #alpha)')
    h2.GetXaxis().SetNdivisions(505)
    h2.GetYaxis().SetTitle('tan #beta')
    h2.GetZaxis().SetTitle('#bf{#it{#Beta}}(X #rightarrow HH)' if decay == 'H  -> h  h' else '#bf{#it{#Beta}}(A #rightarrow ZH)')
    h2.SetContour(40)
    h2.Draw('COLZ')

    latex = ROOT.TLatex()
    latex.SetTextFont(42)
    latex.SetTextAlign(11)
    latex.SetNDC()

    l = cv.GetLeftMargin()
    t = cv.GetTopMargin()

    boson = decay[0]
    latex.DrawLatex(l + 0.02, 1-t + 0.03, f'2HDM type {thdm} m_{{{boson_to_label[boson]}}} = {mass} GeV')

    cv.SaveAs(f'B_{decay_tag}_type{thdm}_mH{mass}.pdf')
    cv.SaveAs(f'B_{decay_tag}_type{thdm}_mH{mass}.root')



for decay, decay_tag in [('A  -> Z  h', 'AtoZh'), ('H  -> h  h', 'Htohh')]:
    
    for thdm in [1, 2, 3, 4]:
        for mass in [300, 500]: #, 700]:
            make_hist_fixedm(thdm, mass, decay, decay_tag)
        for cosba in [0.02]: #[0.05, 0.001, 0.01, 0.02]:
            make_hist(thdm, cosba, decay, decay_tag)
