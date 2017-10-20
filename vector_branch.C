#include <TFile.h>
#include <TTree.h>
#include <TRandom2.h>
#include <vector>

struct mystru{
    int a;
    double b;
    float c[3];
};


struct strct_4x4{
    double e[4];// Energy [1st track, 2nd track, 1st photon, 2nd photon].
    double p[4];// Momentum.
    double t[4];// Polar angle theta.
    double f[4];// Azimuthal angle phi.
    double mpi0;// Invariant mass of two photons (particle indexes are 2 and 3).
};
struct strct_pair{
    int id[2];// Indexes of photons from the considering pair in the raw parameter arrays pE, pP,.. , dpE,.. .
    double chi2_4Cmpi0;
    double chi2_4C;
    strct_4x4 eve_4Cmpi0;
    strct_4x4 eve_4C;
};
struct strct_single{
    int id[1];
    double chi2_4CM1mpi0;
    double chi2_4CM1;
    strct_4x4 eve_4CM1mpi0;
    strct_4x4 eve_4CM1;
};
void fill_pair(strct_pair * pair){
    pair->id[0] = 2;
    pair->id[1] = 3;
    pair->chi2_4Cmpi0 = 2.33;
    pair->chi2_4C = 1.22;
    //////////////////////////
    pair->eve_4C.mpi0 = 130.12;
    pair->eve_4Cmpi0.mpi0 = 130.12;
    for(int i=0; i<4; i++){
        pair->eve_4C.e[i] = 10.+i;
        pair->eve_4C.p[i] = 11.+i;
        pair->eve_4C.t[i] = 12.+i;
        pair->eve_4C.f[i] = 13.+i;
        pair->eve_4Cmpi0.e[i] = 20.+i;
        pair->eve_4Cmpi0.p[i] = 21.+i;
        pair->eve_4Cmpi0.t[i] = 22.+i;
        pair->eve_4Cmpi0.f[i] = 23.+i;
    }
}


void vector_branch(){
    std::vector <float> vf;
    std::vector <mystru> vms;
    mystru mys;
    ///////////////////////////////////////////////////////////
    TRandom2 rn;
    strct_pair pair;
    // strct_single single;
    std::vector <strct_pair> vpair;
    // std::vector <strct_single> vsingle;
    ///////////////////////////////////////////////////////////
    TFile * Fout = new TFile("vector_branch.root", "recreate");
    TTree * t = new TTree("t", "tree");
    t->Branch("mys", &mys);
    t->Branch("vf", &vf);
    t->Branch("vms", &vms);
    t->Branch("vpair", &vpair);
    // t->Branch("vsingle", &vsingle);
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
        vpair.clear();
        fill_pair(&pair);
        vpair.push_back(pair);
        vpair.push_back(pair);
        vpair.push_back(pair);
        ///////////////////////////////////
        t->Fill();
    }
    t->Write();
    Fout->Close();
}

#ifdef __MAKECINT__
#pragma link C++ class mystru+;
#pragma link C++ class vector<mystru>+;
#pragma link C++ class strct_4x4+;
#pragma link C++ class strct_pair+;
// #pragma link C++ class strct_single+;
#pragma link C++ class vector<strct_pair>+;
// #pragma link C++ class vector<strct_single>+;
#endif
