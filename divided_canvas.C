#include "TCanvas.h"
#include "TLatex.h"

void divided_canvas(){
    TLatex * lat = new TLatex();
    TCanvas * c1 = new TCanvas("c1", "c1 title", 600, 600);
    c1->Divide(3, 2);
    for( int i=1; i<6+1; i++ ){// 6 = 3 * 2
        c1->cd(i);
        lat->DrawLatexNDC(.3, .5, Form("Pad #%d", i));
    }
    c1->cd();
    c1->Update();
}
