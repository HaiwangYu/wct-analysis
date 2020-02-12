void TH1_diff(const char* hname, const char* f1, const char* f2) {
	TFile* tf1 = TFile::Open(f1, "read");
	TFile* tf2 = TFile::Open(f2, "read");

	TH1* h1 = (TH1*) tf1->Get(hname);
	TH1* h2 = (TH1*) tf2->Get(hname);

	h1->Add(h2,-1);

	h1->Draw("colz");
}
