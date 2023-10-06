import ROOT
import argparse
from tdrstyle import setTDRStyle
style = setTDRStyle()
style.SetPalette(ROOT.kFuchsia)
ROOT.TColor.InvertPalette()
style.SetNumberContours(256)

# Parse two arguments: MSSM type and br

parser = argparse.ArgumentParser()
parser.add_argument('mssm', default='hMSSM', choices=['hMSSM', 'mH125EFT'], help='MSSM type')
parser.add_argument('br', default='A_Zh', choices=['A_Zh', 'H_hh'], help='Branching ratio')

args = parser.parse_args()
mssm = args.mssm
br = args.br


if mssm == 'hMSSM':
    mssm_title = 'hMSSM'
    br_file = '/Users/jan/Downloads/hMSSM_13TeV.root'
elif mssm == 'mH125EFT':
    br_file = '/Users/jan/Downloads/mh125EFT_13.root'
    mssm_title =  'M_{h,EFT}^{125}'

f = ROOT.TFile.Open(br_file)
h = f.Get(f'br_{br}')

style.cd()
cv = ROOT.TCanvas()

h.UseCurrentStyle()
h.GetXaxis().SetTitle('m_{A} [GeV]')
h.GetXaxis().SetNdivisions(505)
h.GetYaxis().SetTitle('tan #beta')
h.GetYaxis().SetRangeUser(1., 10. if mssm == 'mH125EFT' else 20.)
h.GetXaxis().SetRangeUser(200., 1000.)
h.GetZaxis().SetTitle('#bf{#it{#Beta}}(X #rightarrow HH)' if br == 'H_hh' else '#bf{#it{#Beta}}(A #rightarrow ZH)')
h.SetContour(40)
h.Draw('COLZ')


latex = ROOT.TLatex()
latex.SetTextFont(42)
latex.SetTextAlign(11)
latex.SetNDC()

l = cv.GetLeftMargin()
t = cv.GetTopMargin()

latex.DrawLatex(l + 0.02, 1-t + 0.02, f'{mssm_title}')

cv.SaveAs(f'B_{br}_{mssm}.pdf')
cv.SaveAs(f'B_{br}_{mssm}.root')
