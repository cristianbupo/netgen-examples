import numpy as np
import ngsolve as ng

def SolveCondense(a, res, solver, w):
    if a.condense:
        res.data += a.harmonic_extension_trans * res
        w.data = solver * res
        w.data += a.harmonic_extension * w
        w.data += a.inner_solve * res
    else:
        w.data = solver * res

def NewtonWithLinesearch(a, x, maxnewton=25, abserror=1e-6, relerror=1e-6, min_damping=1e-4, inverse="", factor=1, scene=None, damp=1, printing=False):

    res = x.CreateVector()
    xhelp = x.CreateVector()
    reshelp = res.CreateVector()
    whelp = res.CreateVector()
    w = x.CreateVector()
    
    jj = 0
    
    a.Apply(x, res)
    res[~a.space.FreeDofs()] = 0.
    normres = ng.Norm(res)


    maxres = normres
    if printing: print(f"initial residual {normres}") 

    if normres == 0: return (0,0) 

    while jj < maxnewton:
        jj += 1

        a.AssembleLinearization(x)
        inv = a.mat.Inverse(a.space.FreeDofs(a.condense), inverse=inverse)

        SolveCondense(a, res, inv, w)
        norm_update = ng.Norm(w)

        damping = damp

        xhelp.data = x - damping*w
        a.Apply(xhelp, reshelp)
        
        reshelp[~a.space.FreeDofs()] = 0.
        normreshelp = ng.Norm(reshelp)
                    
        SolveCondense(a, reshelp, inv, whelp)

        
        while ((damping >= min_damping and ng.Norm(whelp) >= factor*norm_update) \
                or np.isnan(normreshelp)):
            if damping < min_damping: 
                if printing: print("break as residual is ", ng.Norm(whelp), " for damping ", damping)
                return (normreshelp, jj)
            
            damping *= 0.5
            xhelp.data = x - damping*w
            
            a.Apply(xhelp, reshelp)
            
            reshelp[~a.space.FreeDofs()] = 0.
            normreshelp = ng.Norm(reshelp)

            SolveCondense(a, reshelp, inv, whelp)


        x.data = xhelp
        a.Apply(x, res)
        res[~a.space.FreeDofs()] = 0.
        normres = normreshelp

        
        if printing: print("newton step ", jj, " res ", normres, "damping",  damping)
        if scene: scene.Redraw()
        

        maxres = max(maxres, normres)
        
        if (normres < maxres*relerror or normres < abserror) and jj > 0:
            if printing: print("newtonsteps: ", jj, ", res ", normres," < ", relerror, "*", maxres)
            return (0, jj)
        
        if np.isnan(normres):
            if printing: print("break as residual is nan")
            break

    print("Newton did not converge")
    return (normres, jj)   

