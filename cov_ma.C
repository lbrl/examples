// https://root.cern.ch/root/htmldoc/guides/users-guide/FittingHistograms.html#fit-result

void cov_ma(){
    TH1F h1("h1", "h1", 20, -10, 10);
    TF1 * f1 = new TF1("f1", "gausn(0) + gausn(3) + pol0(6)", -10, 10);
    f1->SetParameters(10, 0, 1, 5, .1, 2, 2./20);
    f1->SetParNames("N1", "m1", "s1", "N2", "m2", "s2", "c0");
    for(int i=0; i<5000; i++)
        h1.Fill(f1->GetRandom());
    TFitResultPtr res = h1.Fit(f1, "s");
    TMatrixDSym cov = res->GetCovarianceMatrix();
    for(int i=0; i<7; i++){
        for(int j=0; j<7; j++){
            cout << cov(i, j) << "  ";
        }
        cout << "\n";
    }
    // Calculate the sum of N1 and N2, and its error.
    float N1 = f1->GetParameter(0);
    float N2 = f1->GetParameter(3);
    float N = N1 + N2;
    // Proper error propagation.
    float eN = sqrt( cov(0,0) + cov(3,3) + 2*cov(0,3) );
    // Non-proper error propagation.
    float npeN = sqrt( cov(0,0) + cov(3,3) );
    cout << "N = " << N << "\n";
    cout << "eN = " << eN << "\n";
    cout << "npeN = " << npeN << "\n";
}
