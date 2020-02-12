import numpy as np

import matplotlib.pyplot as plt

import matplotlib.colors as mcolors

from matplotlib import cm

# ANCHOR: configuration start

o = np.array([0,0,0])

Wx,Wy,Wz = np.array([1,0,0]), np.array([0,1,0]), np.array([0,0,1])



# *** use APA1 as reference ***

# *** wire direction -> y ***

# *** pitch direction -> z ***

wire_rotation = 35.7



UplaneRotation = np.radians(wire_rotation)

Ux = Wx

Uy = np.array([0,np.cos(UplaneRotation),-np.sin(UplaneRotation)])

Uz = np.array([0,np.sin(UplaneRotation),np.cos(UplaneRotation)])



VplaneRotation = np.radians(-wire_rotation)

Vx = Wx

Vy = np.array([0,np.cos(VplaneRotation),-np.sin(VplaneRotation)])

Vz = np.array([0,np.sin(VplaneRotation),np.cos(VplaneRotation)])

# ANCHOR: configuration end



# ANCHOR: part1 - cal thetaxz for one track - start

def fun_normalVector(p0,p1,p2):

    a = (p1[1]-p0[1])*(p2[2]-p0[2])-(p2[1]-p0[1])*(p1[2]-p0[2])

    b = (p2[0]-p0[0])*(p1[2]-p0[2])-(p1[0]-p0[0])*(p2[2]-p0[2])

    c = (p1[0]-p0[0])*(p2[1]-p0[1])-(p2[0]-p0[0])*(p1[1]-p0[1])

    return np.array([a,b,c])/np.sqrt(a**2+b**2+c**2)

nWxz = fun_normalVector(o,Wx,Wz) # Wy

nUxz = fun_normalVector(o,Ux,Uz) # Uy

nVxz = fun_normalVector(o,Vx,Vz) # Vy



def fun_projectionPoint(pi,p0,n):

    # cal pi's projection point on plane formed by p0 and n

    t = n[0]*p0[0]+n[1]*p0[1]+n[2]*p0[2]

    t -= n[0]*pi[0]+n[1]*pi[1]+n[2]*pi[2]

    t /= np.sqrt(n[0]**2+n[1]**2+n[2]**2)

    return np.array([pi[0]+n[0]*t,pi[1]+n[1]*t,pi[2]+n[2]*t])



def fun_angle(v1,v2):

    dot = v1[0]*v2[0]+v1[1]*v2[1]+v1[2]*v2[2]

    amp1 = np.sqrt(v1[0]**2+v1[1]**2+v1[2]**2)

    amp2 = np.sqrt(v2[0]**2+v2[1]**2+v2[2]**2)

    if (amp1<=0 or amp2 <= 0):

        return None

    costheta = dot/amp1/amp2

    return np.degrees(np.arccos(costheta))



def fun_cal_thetaXZ(track, wire, pitch):

    return fun_angle(fun_projectionPoint(track,o,wire),pitch)



def fun_ccs2scs(ccs):

    x, y, z = ccs[0], ccs[1], ccs[2]

    r = np.sqrt(x**2+y**2+z**2)

    theta = 90 if z==0 else math.degrees(np.arctan(np.sqrt(x**2+y**2)/z))

    fai = 90 if x==0 else math.degrees(np.arctan(y/x))

    scs = np.array([r,theta,fai])

    return scs



def fun_scs2ccs(scs):

    r, theta, fai = scs[0], np.radians(scs[1]), np.radians(scs[2])

    x = r*np.sin(theta)*np.cos(fai)

    y = r*np.sin(theta)*np.sin(fai)

    z = r*np.cos(theta)

    ccs = np.array([x,y,z])

    return ccs



def fun_test():

    thetaxzs = [0,1,3,5,10,20,30,45,60,75,80,82,84,89,90]

    for i in thetaxzs:

        print(i)

        rad = np.radians(i)

        track = np.array([np.sin(rad),0,np.cos(rad)])

        print(("%.10f\t%.10f\t%.10f")%(fun_cal_thetaXZ(track,Uy,Uz),

                                       fun_cal_thetaXZ(track,Vy,Vz),

                                       fun_cal_thetaXZ(track,Wy,Wz)))

        

        Trk_scs = np.array([1, i, 0])

        Trk_ccs = fun_scs2ccs(Trk_scs)

        print(("%.10f\t%.10f\t%.10f\n")%(fun_cal_thetaXZ(Trk_ccs,Uy,Uz),

                                         fun_cal_thetaXZ(Trk_ccs,Vy,Vz),

                                         fun_cal_thetaXZ(Trk_ccs,Wy,Wz)))



def fun_gen_space(filename,nPoint):

    np.random.seed(1246)

    theta = np.random.rand(nPoint)*180

    fai = np.random.rand(nPoint)*360

    thetaxz_U = np.zeros(nPoint)

    thetaxz_V = np.zeros(nPoint)

    thetaxz_W = np.zeros(nPoint)

    for i in range(nPoint):

        track = fun_scs2ccs(np.array([1,theta[i],fai[i]]))

        thetaxz_U[i] = fun_cal_thetaXZ(track, Uy, Uz)

        thetaxz_V[i] = fun_cal_thetaXZ(track, Vy, Vz)

        thetaxz_W[i] = fun_cal_thetaXZ(track, Wy, Wz)

    np.savez(filename,thetaxz_U=thetaxz_U,thetaxz_V=thetaxz_V,thetaxz_W=thetaxz_W)    



def fun_read_space(filename):

    filein = np.load(filename)

    thetaxz_U = filein['thetaxz_U']

    thetaxz_V = filein['thetaxz_V']

    thetaxz_W = filein['thetaxz_W']

    print(len(thetaxz_U),len(thetaxz_V),len(thetaxz_W))

    fun_draw_space(thetaxz_U,thetaxz_V,'$\\theta_{xz}$ [U]','$\\theta_{xz}$ [V]','UVthetaxz')

    fun_draw_space(thetaxz_U,thetaxz_W,'$\\theta_{xz}$ [U]','$\\theta_{xz}$ [W]','UWthetaxz')

    fun_draw_space(thetaxz_V,thetaxz_W,'$\\theta_{xz}$ [V]','$\\theta_{xz}$ [W]','VWthetaxz')



def fun_draw_space(thetaxz_X,thetaxz_Y,xlabel,ylabel,figname):

    edges = np.arange(91)

    fig, ax = plt.subplots(1, 1, figsize=(7,6))

    pcmdata = np.histogram2d(thetaxz_X,thetaxz_Y,[edges,edges])

    print(pcmdata[0].max())

    pcmobj = ax.pcolormesh(edges,edges,pcmdata[0],

                           norm=mcolors.LogNorm(),

                           cmap=cm.jet,vmax=2e4,vmin=1)

    fontsize = 12

    ax.set_xlabel(xlabel,fontsize=fontsize*1.5)

    ax.set_ylabel(ylabel,fontsize=fontsize*1.5)

    ax.set_aspect('equal', 'box')

    ax.minorticks_on()

    tw = 1

    ax.tick_params(which='major',labelsize=fontsize,length=8,width=tw,pad = 10,

                   bottom=True,top=True,left=True,right=True,

                   direction='in')

    ax.tick_params(which='minor',labelsize=fontsize,length=4,width=tw,

                   bottom=True,top=True,left=True,right=True,

                   direction='in')

    for spines in ax.spines.values():

        spines.set_lw(tw)

    

    cb = fig.colorbar(pcmobj,ax=ax,shrink=0.92)

    cb.ax.tick_params(which='major',labelsize = fontsize,length=8,width=tw,direction='in')

    cb.ax.tick_params(which='minor',labelsize = fontsize,length=4,width=tw,direction='in')

    cb.outline.set_lw(tw)

    fig.tight_layout()

    fig.show()

    fig.savefig(figname+'.svg')

    fig.savefig(figname+'.png')

    

# ANCHOR: part1 - cal thetaxz for one track - end



# ANCHOR: part2 - generate track from thetaXZ - start

def fun_DegeneracyPlaneNormalVector(thetaXZ, rotation):

    thetaXZ, rotation = np.radians(thetaXZ), np.radians(rotation)

    return np.array([-np.cos(thetaXZ),

                     np.sin(thetaXZ)*np.sin(rotation),

                     np.sin(thetaXZ)*np.cos(rotation)])



def fun_CrossProduct(n1,n2):

    s1 = n1[1]*n2[2]-n1[2]*n2[1]

    s2 = n1[2]*n2[0]-n1[0]*n2[2]

    s3 = n1[0]*n2[1]-n1[1]*n2[0]

    norm = np.sqrt(s1**2+s2**2+s3**2)

    return o if norm==0 else np.array([s1,s2,s3])/norm



def fun_test1():

    rad = np.radians(45)

    track = np.array([np.sin(rad),0,np.cos(rad)])

    thetaxz_U = fun_cal_thetaXZ(track, Uy, Uz)

    thetaxz_V = fun_cal_thetaXZ(track, Vy, Vz)

    print(track)

    print(thetaxz_U)

    print(thetaxz_V)

    Unormal = fun_DegeneracyPlaneNormalVector(thetaxz_U, wire_rotation)

    Vnormal = fun_DegeneracyPlaneNormalVector(thetaxz_V, -wire_rotation)

    print(fun_CrossProduct(Wy, Unormal))

    print(fun_CrossProduct(Wy, Unormal))

    print(fun_CrossProduct(Unormal, Vnormal))

    print(fun_cal_thetaXZ(fun_CrossProduct(Unormal, Vnormal),Wy,Wz))

    return



def fun_gen_track_thetaxzUV(thetaxz_U, thetaxz_V):

    Unormal = fun_DegeneracyPlaneNormalVector(thetaxz_U, wire_rotation)

    Vnormal = fun_DegeneracyPlaneNormalVector(thetaxz_V, -wire_rotation)

    return fun_CrossProduct(Unormal, Vnormal)

    

def fun_gen_track_thetaxzUW(thetaxz_U, thetaxz_W):

    Unormal = fun_DegeneracyPlaneNormalVector(thetaxz_U, wire_rotation)

    Wnormal = fun_DegeneracyPlaneNormalVector(thetaxz_W, 0)

    return fun_CrossProduct(Unormal, Wnormal)



def fun_gen_track_thetaxzVW(thetaxz_V, thetaxz_W):

    Vnormal = fun_DegeneracyPlaneNormalVector(thetaxz_V, -wire_rotation)

    Wnormal = fun_DegeneracyPlaneNormalVector(thetaxz_W, 0)

    return fun_CrossProduct(Wnormal, Vnormal)



def fun_cal_thetaXZ_U(track):

    return fun_cal_thetaXZ(track, Uy, Uz)

def fun_cal_thetaXZ_V(track):

    return fun_cal_thetaXZ(track, Vy, Vz)

def fun_cal_thetaXZ_W(track):

    return fun_cal_thetaXZ(track, Wy, Wz)



def fun_gen_thetaxz_map(tag):

    nbins = 90

    edges = np.arange(91)

    centers = (edges[1:]+edges[:-1])/2

    fig, ax = plt.subplots(1, 1, figsize=(7,6))

    pcmdata = np.zeros([nbins,nbins])

    if tag=='UVW': fun_gen_track_tag,y,z = fun_gen_track_thetaxzUV,Wy,Wz

    elif tag=='UWV': fun_gen_track_tag,y,z = fun_gen_track_thetaxzUW,Vy,Vz

    elif tag=='VWU': fun_gen_track_tag,y,z = fun_gen_track_thetaxzVW,Uy,Uz

    else : return

    for i in range(nbins):

        for j in range(nbins):

            pcmdata[i][j] = fun_cal_thetaXZ(fun_gen_track_tag(centers[i],centers[j]),y,z)

    pcmobj = ax.pcolormesh(edges,edges,pcmdata,vmax=90,vmin=0)

    fontsize = 12

    ax.set_xlabel('$\\theta_{xz}$ [%s]'%tag[0],fontsize=fontsize*1.5)

    ax.set_ylabel('$\\theta_{xz}$ [%s]'%tag[1],fontsize=fontsize*1.5)

    ax.set_aspect('equal', 'box')

    ax.minorticks_on()

    tw = 1

    ax.tick_params(which='major',labelsize=fontsize,length=8,width=tw,pad = 10,

                   bottom=True,top=True,left=True,right=True,

                   direction='in')

    ax.tick_params(which='minor',labelsize=fontsize,length=4,width=tw,

                   bottom=True,top=True,left=True,right=True,

                   direction='in')

    for spines in ax.spines.values():

        spines.set_lw(tw)

    

    cb = fig.colorbar(pcmobj,ax=ax,shrink=0.92)

    cb.ax.minorticks_on()

    cb.ax.tick_params(which='major',labelsize = fontsize,length=8,width=tw,direction='in')

    cb.ax.tick_params(which='minor',labelsize = fontsize,length=4,width=tw,direction='in')

    cb.outline.set_lw(tw)

    cb.ax.set_ylabel('$\\theta_{xz}$ [%s]'%tag[2],fontsize=fontsize*1.5)

    fig.tight_layout()

    fig.show()

    fig.savefig('thetaxz_'+tag+'_map.svg')

    fig.savefig('thetaxz_'+tag+'_map.png')

# ANCHOR: part2 - generate track from thetaXZ - end

def fun_xyz_to_thetaXZ_thetaYZ(v):
    print(v)
    thetaXZ = np.arctan2(v[0],v[2])
    thetaYZ = np.arctan2(v[1],v[2])
    return np.array([thetaXZ, thetaYZ])/np.pi*180.



if __name__=='__main__':
    print(fun_xyz_to_thetaXZ_thetaYZ(fun_gen_track_thetaxzUV(89,45)))

    pass

