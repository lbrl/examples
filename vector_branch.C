#include <TFile.h>
#include <TTree.h>
#include <vector>

struct mystru{
    int a;
    double b;
    float c[3];
};


void vector_branch(){
    std::vector <float> vf;
    std::vector <mystru> vms;
    mystru mys;
    TFile * Fout = new TFile("vector_branch.root", "recreate");
    TTree * t = new TTree("t", "tree");
    t->Branch("mys", &mys);
    t->Branch("vf", &vf);
    t->Branch("vms", &vms);
    for(int i=0; i<10; i++){
        mys.a = i;
        mys.b = sqrt(i);
        for(int j=0; j<3; j++){
            mys.c[j] = sqrt( pow(i, j+3) );
        }
        ///////////////////////////////////
        vf.clear();
        vf.push_back(sqrt(i)+i);
        vf.push_back(sqrt(i)-i);
        ///////////////////////////////////
        vms.clear();
        vms.push_back(mys);
        vms.push_back(mys);
        ///////////////////////////////////
        t->Fill();
    }
    t->Write();
    Fout->Close();
}

#ifdef __MAKECINT__
#pragma link C++ class mystru+;
#pragma link C++ class vector<mystru>+;
#endif
