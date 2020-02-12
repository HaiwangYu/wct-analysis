void rootlogon(){
	//gStyle->SetPalette(kTemperatureMap);
	const int nb = 49; // color intervals at colorbar
	static Int_t  colors[nb];
	const UInt_t Number = 3;
	Double_t Red[Number]   = { 0.0, 1.0, 1.0 };
	Double_t Green[Number] = { 0.0, 1.0, 0.0 };
	Double_t Blue[Number]  = { 1.0, 1.0, 0.0 };
	Double_t Stops[Number] = { 0.0, 0.5, 1.0 };
	Int_t FI = TColor::CreateGradientColorTable(Number,Stops,Red,Green,Blue,nb);
	for (int i=0; i<nb; i++) colors[i] = FI+i;
	gStyle->SetPalette(nb,colors);
	gStyle->SetOptStat(0);
}
