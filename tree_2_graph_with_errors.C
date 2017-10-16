void tree_2_graph_with_errors(){
    TTree * t = new TTree("t", "tree with errors");
    double x, xe, y, ye;
    t->Branch("x", &x, "x/D");
    t->Branch("y", &y, "y/D");
    t->Branch("xe", &xe, "xe/D");
    t->Branch("ye", &ye, "ye/D");
    TRandom2 r;
    for(int i=0; i<10; i++){
        x = i;
        xe = .05;
        x = x + r.Gaus(0, xe);
        y = i*10 + 2.;
        ye = sqrt( y );
        y = y + r.Gaus(0, ye);
        t->Fill();
    }
    int n = t->Draw("x:y:xe:ye", "", "goff");
    TGraphErrors * gr = new TGraphErrors(n, t->GetV1(), t->GetV2(), t->GetV3(), t->GetV4());
    TCanvas * c1 = new TCanvas("c1", "c1", 600, 600);
    gr->Draw("ap");
    ////////////////////////////////////
    gr->Fit("pol1");
    ////////////////////////////////////
    c1->Update();
}
