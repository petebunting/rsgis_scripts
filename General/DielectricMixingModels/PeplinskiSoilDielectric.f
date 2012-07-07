c       Dielectic mixing model of Peplinski et. al. to calculate the complex dielectic of soil:
c
c		Peplinski, ULaby, Dobson, Dielectric Properties of Soils in the 0.3 to 1.3 GHz Range, 
c		IEEE Trans Geosci Rem Sensing, Vol 33, No. 3, pp 803-807, May 1995.
c		
c		with the corrections given in:
c		
c		Peplinski, ULaby, Dobson, Corrections to: Dielectric Properties of Soils in the 0.3 to 1.3 GHz Range,  
c		IEEE Trans Geosci Rem Sensing, Vol 33, No. 6, p 1340, Nov. 1995. 
c		
c		The T dependent form is given in:
c		F. T. Ulaby, R. K. Moore, and A. K. Fung, Microwave Remote Sensing, vol. III. Dedham, MA: Artech House, 1986, Appendix E.
c		
c		
        
        program dielecSoil
        
        real wavlen
        real am
        complex e
        real sand, clay, rhoB, mv
        real rhoS, alpa, epsWInf
        real twoPiTw, epsW0
        real betaReal, epsS
        real epsFwReal, epsRealPartA
        real epsRealPartB, epsReal
        real betaImg, sigmaEff
        real epsFwImgPartA, epsFwImgPartB
        real epsFwImg, epsImgPartA
        real espImgPartB, epsImg
        real pi
        real mVStep
        integer mVItt
        
        pi = 3.14159265
        
        
        wavlen = 0.68 ! Wavelenght 
        sand = 0.4    ! Sand percentage
        clay = 0.5    ! Clay percentage
        rhoB = 1.55   ! Bulk density
        mV = 0.05     ! Volumetric water content
        T = 20        ! Temperature
        rhoS = 2.66   ! Specific density of solid soil properties
        alpha = 0.65
        
        f=3.0e8/wavlen
        print*, 'wavelen', wavlen
        print*, 'f = ', f
        
        mV = 0.
        mVStep = 0.05
        do 400 mVItt=1,8
        mV = mV + mVStep
        
        epsWInf = 4.9 ! High frequency limit of dielectric constant of free water
        twoPiTw = 1.1109e-10 - (3.824e-12 * T)+ (6.938e-14 * T**2) - 
     1       (5.096e-16* T**3) ! Static dielectric constant for water.
        epsW0 = 88.045 - 0.4147*T+(6.295e-4 * T**2)+(1.075e-5 * T**3)
        betaReal = 1.2748 - (0.519 * sand) - (0.152 * clay) ! Real part of soil dependence constant
        epsS = ((1.01 + (0.44 * rhoS))*(1.01 + (0.44*rhoS)))-0.062 !Dielectric constant of solid soils;
        epsFwReal = epsWInf + (epsW0 - epsWInf) / (1+((f
     1       * twoPiTw )*(f * twoPiTw )))
        epsRealPartA = 1 + (rhoB / rhoS) * ((epsS**alpha) -1)
        epsRealPartB =  ((mV**betaReal) * (epsFwReal**alpha)) -mV
        epsReal = (epsRealPartA + epsRealPartB)**(1/alpha)

        if(f.lt.1.4e9) sigmaEff = 0.0467 + (0.2204 * rhoB) -
     1           (0.4111 * sand) + (0.6614 * clay)
        else sigmaEff = -1.645 + (1.939 * rhoB) - (2.25622 * sand) +
     1   (1.594 * clay)

        betaImg = 1.33797-(0.603*sand)-(0.166*clay)

        epsFwImgPartA = ((f * twoPiTw)  * (epsW0 -
     1   epsWInf)) /  (1 + ((f * twoPiTw )**2))
        epsFwImgPartB = (sigmaEff / (f * twoPiTw))
     1   - ((rhoS - rhoB) / (rhoS * mV));
        epsFwImg = epsFwImgPartA + epsFwImgPartB;
        epsImgPartA = mV**betaImg
        espImgPartB = epsFwImg**alpha
        epsImg = (epsImgPartA*espImgPartB)**(1/alpha)

        e = cmplx(epsReal,epsImg)
        
        print*, mV, epsReal, epsImg
        
  400  continue     
        
        end

