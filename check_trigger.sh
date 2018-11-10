INPUT_FILE="/afs/cern.ch/work/l/lcadamur/private/YR_bbbb_analysis/CMSSW_9_3_2/src/bbbbYRanalysis/histofiller/bbbbAnalysis/trg_impact_study/outPlotter.root"
for var in BDTG_nomasscut; do
    for sel in baseline_SR baseline50_SR baseline55_SR baseline60_SR baseline65_SR baseline70_SR baseline75_SR baseline80_SR; do
        cardname=card_${var}_${sel}.txt
        wsname=card_${var}_${sel}.root
        echo ""
        echo ""
        echo ".... making card for var: $var, sel: $sel"
        python make_datacard.py --var $var --sel $sel --cardOut cards/${cardname} --fileIn ${INPUT_FILE}
        echo ".... making workspace"
        cd cards/
        text2workspace.py ${cardname}
        combine -M Significance  -t -1 --expectSignal 1 -n ${var}_${sel} ${wsname}
        cd ..
    done
done
