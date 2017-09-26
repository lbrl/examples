#include "TCanvas.h"
#include "TH1.h"
#include "TF1.h"
#include "TMath.h"

void several_functions(){
    TCanvas * c1 = new TCanvas("c1", "c1 title", 800, 400);
    c1->Divide(2, 1);
    TH1D *  h[2];
    TF1 *  f1[2];
    TF1 *  f2[2];
    for( int i=0; i<2; i++ ){
        c1->cd(i+1);
        h[i] = new TH1D( Form("h_%d", i), "h title", 100, -10, 10);
        ///////////////////////////////////////////////////////////////////
        f1[i] = new TF1( Form("f1_%d", i), "gaus(0)", -10, 10);
        f1[i]->SetParameters(10, 1, 2);
        f1[i]->SetLineColor(kRed);
        f1[i]->SetLineWidth(1);
        ///////////////////////////////////////////////////////////////////
        f2[i] = new TF1( Form("f2_%d", i), "gaus(0) + pol0(3)", -10, 10);
        f2[i]->SetParameters(10, 1, 2, .5);
        f2[i]->SetLineColor(kBlue);
        f2[i]->SetLineWidth(1);
        ///////////////////////////////////////////////////////////////////
        h[i]->FillRandom( f2[i]->GetName(), 500);
        h[i]->Fit( f1[i], "lr", "goff");
        h[i]->Fit( f2[i], "lr+", "goff");
        h[i]->Draw();
        f1[i]->Draw("same");
        f2[i]->Draw("same");
    }
    c1->cd();
    c1->Update();
}
