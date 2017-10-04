struct mystru{
    int a;
    double b;
    float c[3];
};

void branch_with_struct(){
    int a;
    mystru mys;
    TFile * Fout = new TFile("branch_with_struct.root", "recreate");
    TTree * t = new TTree("t", "tree");
    t->Branch("a", &a, "a/I");// The same name as in the structure.
    t->Branch("mys", &mys);
    for(int i=0; i<10; i++){
        a = 100+i;
        mys.a = i;
        mys.b = sqrt(i);
        for(int j=0; j<3; j++){
            mys.c[j] = sqrt( pow(i, j+3) );
        }
        t->Fill();
    }
    t->Write();
    Fout->Close();
}

//////////////////////////////////////////
//
//  How to work with a strcut in a tree.
//
//  Give differen results.
//  t->Draw("a");
//  t->Draw("mys.a");
//
//  Give the same result.
//  t->Draw("mys.b");
//  t->Draw("b");
//
//  Works too.
//  t->Draw("c[1]:c[2]");
//  t->Draw("mys.c[1]:c[2]");
//
//////////////////////////////////////////
