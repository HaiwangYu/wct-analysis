#include <TVector3.h>

#include <fstream>
#include <iomanip>
#include <sstream>
#include <iostream>

using namespace std;

double project_polar(const TVector3& t, const TVector3&n, const TVector3&z) {
    auto tp = t-t.Dot(n)*n;
    return TMath::ACos(tp.Dot(z)/tp.Mag()/z.Mag())/TMath::Pi()*180.;
}

TVector3 same_thetaxz_plane_norm(
  const double thetaxz, // degree
  const double rot //degree
  ){
  TVector3 ret(1,0,0); // inital norm as X
  ret.RotateY(thetaxz/180.*TMath::Pi());
  ret.RotateX(rot/180.*TMath::Pi());
  // ret.Print();
  return ret;
}

void angle(const double thetaxz_U, const double thetaxz_V) {

  const double UFromVert = -35.7; // degree
  const double VFromVert = -UFromVert; // degree

  auto vu = same_thetaxz_plane_norm(thetaxz_U, UFromVert);
  auto vv = same_thetaxz_plane_norm(thetaxz_V, VFromVert);

  auto v = vu.Cross(vv);

  v.Print();

  v *= -1.;

  cout
  << "XZ, YZ: "
  << "[ " << TMath::ATan2(v.X(), v.Z()) / TMath::Pi() * 180.
  << "  " << TMath::ATan2(v.Y(), sqrt(1-v.Y()*v.Y())) / TMath::Pi() * 180.
  << " ]"
  << endl;

  const TVector3 X(1,0,0);
  const TVector3 nu(0,TMath::Cos(UFromVert/180.*TMath::Pi()),TMath::Sin(UFromVert/180.*TMath::Pi()));
  const TVector3 nv(0,TMath::Cos(VFromVert/180.*TMath::Pi()),TMath::Sin(VFromVert/180.*TMath::Pi()));


  cout
  << "Test:"
  << "[ " << 90 - project_polar(v, nu, X)
  << "  " << 90 - project_polar(v, nv, X)
  << " ]"
  << endl;
}
