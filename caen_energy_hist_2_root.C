///  How to use:
///  $ root 'caen_energy_hist_2_root.C("CdPbLiWO4_Dy_2017-12-06_003_eh_0.dat", "CdPbLiWO4_Dy_2017-12-06_003_eh_0.root")' -b -q
///  $ root 'caen_energy_hist_2_root.C+("CdPbLiWO4_Dy_2017-12-06_003_eh_0.dat", "CdPbLiWO4_Dy_2017-12-06_003_eh_0.root")' -b -q

#include <fstream>
#include "TFile.h"
#include "TH1I.h"

int caen_energy_hist_2_root(std::string finname, std::string Foutname){
    std::ifstream fin(finname.c_str());
    int nbin = 32768;// The number of bins.
    TFile * Fout = new TFile(Foutname.c_str(), "recreate");
    TH1I * h = new TH1I("h", "energy spectrum", nbin, 0, nbin);
    int bin, val;
    while( fin >> bin >> val ){// Read the opened file line by line. The file supposed to have two integers by line.
        if( bin+1 < nbin ){// Skip the last bin, because it commonly contains a cabbage value.
            h->SetBinContent(bin+1, val);// Add shift, beacuse the zero-bin is an underflow bin in TH1.
        }
    }
    h->Write();
    Fout->Close();
    return 0;
}
