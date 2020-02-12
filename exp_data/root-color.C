{
	TCanvas *c1  = new TCanvas("c1","c1",0,0,600,400);
	TF2 *f1 = new TF2("f1","x*x+y*y-1",-1,1,-1,1);
	Int_t palette[11];
	palette[0] = kBlue;
	palette[1] = kBlue-4;
	palette[2] = kBlue-7;
	palette[3] = kBlue-9;
	palette[4] = kBlue-10;
	palette[5] = kWhite;
	palette[6] = kRed-10;
	palette[7] = kRed-9;
	palette[8] = kRed-7;
	palette[9] = kRed-4;
	palette[10] = kRed;
	gStyle->SetPalette(kLightTemperature);
	f1->Draw("colz");
	return c1;
}
