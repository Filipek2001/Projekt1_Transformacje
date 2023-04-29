from math import sin, cos, sqrt, atan, degrees
import math
import numpy as np

class Transformator:
    def __init__(self, model: str = "wgs84"):

        if model == "wgs84":
            self.a = 6378137.0 # semimajor_axis
            self.b = 6356752.31424518 # semiminor_axis
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
            self.m = 0.999923
            self.m_0 = 0.9993
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.ecc = sqrt(2 * self.flat - self.flat ** 2) # eccentricity  WGS84:0.0818191910428
        self.ecc2 = (2 * self.flat - self.flat ** 2) # eccentricity**2
        self.method_dict = {
        "XYZBLH": self.XYZtoBLH,
        "BLHXYZ": self.BLHtoXYZ,
        "XYZNEUp": self.XYZtoNEUp,
        "BLXY2000":self.BLto2000,
        "BLXY1992":self.BLto1992,
        "XYZXY2000":self.XYZto2000,
        "XYZXY1992":self.XYZto1992
        }
    def set_model(self, model):
        if model == "wgs84":
            self.a = 6378137.0 # semimajor_axis
            self.b = 6356752.31424518 # semiminor_axis
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
            self.m = 0.999923
            self.m_0 = 0.9993


    def XYZtoBLH(self, X, Y, Z, radians):
        r = sqrt(X**2 + Y**2)
        lat_prev = atan(Z / (r * (1 - self.ecc2)))
        N = self.a / sqrt(1 - self.ecc2 * (sin(lat_prev)) ** 2)
        h = r / cos(lat_prev) - N
        lat_next = atan((Z / r) * (((1 - self.ecc2 * N / (N + h))**(-1))))
        epsilon = 0.0000001 / 206265
        while abs(lat_prev - lat_next) < epsilon:
            lat_prev = lat_next
            N = self.a / sqrt(1 - self.ecc2 * (sin(lat_prev)) ** 2)
            h = r / cos(lat_prev) - N
            lat_next = atan((Z / r) * (((1 - self.ecc2 * N / (N + h))**(-1))))
        phi = lat_prev
        lam = atan(Y / X)
        N = self.a / sqrt(1 - self.ecc2 * (sin(phi)) ** 2)
        h = r / cos(phi) - N
        return degrees(phi), degrees(lam), h

    def XYZto2000(self, X, Y, Z, bool):
        phi, lam, h = self.XYZtoBLH(X, Y, Z, bool)
        X, Y = self.BLto2000(phi, lam, 0, False)
        return X, Y

    def XYZto1992(self, X, Y, Z, bool):
        phi, lam, h = self.XYZtoBLH(X, Y, Z, bool)
        x, y = self.BLto1992(phi, lam, 0, False)
        return x, y

    def BLHtoXYZ(self, phi, lam, h, radians:bool):
        """conversion uses radians"""
        if not radians: phi, lam = math.radians(phi), math.radians(lam)
        N = self.a / sqrt(1 - self.ecc2 * (sin(phi)) ** 2)
        X = (N + h) * cos(phi) * cos(lam)
        Y = (N + h) * cos(phi)*sin(lam)
        Z = (N * (1 - self.ecc2) + h) * sin(phi)
        return X, Y, Z

    def XYZtoNEUp(self, arguments):
        X, Y, Z, phi, lam, h = arguments
        Na = self.a/math.sqrt(1 - self.ecc2 *((math.sin(np.deg2rad(phi))**2)))
        XYZs = np.array([X,Y,Z])

        Xa = (Na+h)*math.cos(phi)*math.cos(lam)
        Ya = (Na+h)*math.cos(phi)*math.sin(lam)
        Za = (Na*(1-self.ecc2)+h)*math.sin(phi)
        XYZa = np.array([Xa,Ya,Za])
        dX = XYZs-XYZa
        R = np.array([[-sin(phi)*cos(lam), -sin(lam), cos(phi)*cos(lam)],
                            [-sin(phi)*sin(lam), cos(lam), cos(phi)*sin(lam)],
                            [cos(phi)          ,    0    , sin(phi)         ]])
        neu = R.dot(dX)
        return neu


    def BLto2000(self, phi, lam, z, radians:bool):
        if not radians: phi, lam = math.radians(phi), math.radians(lam)
        N = self.a/math.sqrt(1-self.ecc2*math.sin(phi)**2)
        t = np.tan(phi)
        e_2 = self.ecc2/(1-self.ecc2)
        n2 = e_2 * (np.cos(phi))**2
        lam = math.degrees(lam)
        if 16.5 > lam > 13.5 :
            s = 5
            lam0 = 15
        elif 19.5 > lam > 16.5 :
            s = 6
            lam0 = 18
        elif 22.5 > lam > 19.5:
            s = 7
            lam0 = 21
        #elif 25.5 > lam > 22.5:
        else:
            s = 8
            lam0 = 24
        lam = math.radians(lam)
        lam0 = math.radians(lam0)
        l = lam - lam0

        A0 = 1 - (self.ecc2/4) - ((3*(self.ecc2**2))/64) - ((5*(self.ecc2**3))/256)
        A2 = (3/8) * (self.ecc2 + ((self.ecc2**2)/4) + ((15 * (self.ecc2**3))/128))
        A4 = (15/256) * (self.ecc2**2 + ((3*(self.ecc2**3))/4))
        A6 = (35 * (self.ecc2**3))/3072

        sig = self.a * ((A0*phi) - (A2*np.sin(2*phi)) + (A4*np.sin(4*phi)) - (A6*np.sin(6*phi)))
        x = sig + ((l**2)/2) * N *np.sin(phi) * np.cos(phi) * (1 + ((l**2)/12) * ((math.cos(phi))**2) * (5 - t**2 + 9*n2 + 4*(n2**2)) + ((l**4)/360) * ((math.cos(phi))**4) * (61 - (58*(t**2)) + (t**4) + (270*n2) - (330 * n2 *(t**2))))
        y = l * (N*math.cos(phi)) * (1 + ((((l**2)/6) * (math.cos(phi))**2) * (1-t**2+n2)) +  (((l**4)/(120)) * (math.cos(phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14*n2) - (58*n2*(t**2))))

        x00 = round(self.m * x, 3)
        y00 = round(self.m * y + (s*1000000) + 500000, 3)
        return(x00, y00)

    def BLto1992(self, phi, lam, z, radians:bool):
        if not radians: phi, lam = math.radians(phi), math.radians(lam)
        N = self.a/(np.sqrt(1-self.ecc2 * np.sin(phi)**2))
        t = np.tan(phi)
        e_2 = self.ecc2/(1-self.ecc2)
        n2 = e_2 * (np.cos(phi))**2

        lam_00 = math.radians(19)
        l = lam - lam_00

        A0 = 1 - (self.ecc2/4) - ((3*(self.ecc2**2))/64) - ((5*(self.ecc2**3))/256)
        A2 = (3/8) * (self.ecc2 + ((self.ecc2**2)/4) + ((15 * (self.ecc2**3))/128))
        A4 = (15/256) * (self.ecc2**2 + ((3*(self.ecc2**3))/4))
        A6 = (35 * (self.ecc2**3))/3072


        sig = self.a * ((A0*phi) - (A2*np.sin(2*phi)) + (A4*np.sin(4*phi)) - (A6*np.sin(6*phi)))

        x = sig + ((l**2)/2) * N *np.sin(phi) * np.cos(phi) * (1 + ((l**2)/12) * ((math.cos(phi))**2) * (5 - t**2 + 9*n2 + 4*(n2**2)) + ((l**4)/360) * ((math.cos(phi))**4) * (61 - (58*(t**2)) + (t**4) + (270*n2) - (330 * n2 *(t**2))))
        y = l * (N*math.cos(phi)) * (1 + ((((l**2)/6) * (math.cos(phi))**2) * (1-t**2+n2)) +  (((l**4)/(120)) * (math.cos(phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14*n2) - (58*n2*(t**2))))

        x92 = round(self.m_0*x - 5300000, 3)
        y92 = round(self.m_0*y + 500000, 3)
        return x92, y92


