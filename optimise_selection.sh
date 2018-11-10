# INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_4/outPlotter.root"
# INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_preapp/outPlotter.root"
# INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg/outPlotter.root"
# INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg_lepveto/outPlotter.root"
INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/various_plots_BDTallBkg_lepveto2/outPlotter.root"

for var in BDTG_nomasscut BDTG_4_masscut BDTG_6_masscut BDTG_7_masscut; do
    # for sel in finalsel_SR baseline_SR; do
    for sel in finalselnolepnoovrlp_SR finalselnolep_SR finalsel_SR; do
# for var in BDTG_nomasscut; do
#     for sel in baseline_SR; do
        cardname=card_${var}_${sel}.txt
        wsname=card_${var}_${sel}.root
        echo ""
        echo ""
        echo ".... making card for var: $var, sel: $sel"
        python make_datacard.py --var $var --sel $sel --cardOut cards/${cardname} --fileIn ${INPUT_FILE}
        echo ".... making workspace"
        cd cards/
        text2workspace.py ${cardname}
        combine -M Significance  -S 0 -t -1 --expectSignal 1 -n ${var}_${sel} ${wsname}
        cd ..
    done
done
