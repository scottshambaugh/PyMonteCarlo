from scipy.stats import uniform, rv_discrete
from PyMonteCarlo.MCSim import MCSim
from PyMonteCarlo.mc_plot import mc_plot
from PyMonteCarlo.mc_multi_plot import mc_multi_plot
from PyMonteCarlo.order_statistics import sig2pct

from rocket_example_sim import rocket_example_sim
from rocket_example_preprocess import rocket_example_preprocess
from rocket_example_postprocess import rocket_example_postprocess
fcns ={'preprocess' :rocket_example_preprocess,   \
       'run'        :rocket_example_sim,          \
       'postprocess':rocket_example_postprocess}

ndraws = 8
seed=12362398

def rocket_example_run_script():
    sim = MCSim(name='Rocket', ndraws=ndraws, fcns=fcns, firstcaseisnom=True, seed=seed, cores=1)
    
    sim.addInVar(name='Wind Azi [deg]', dist=uniform, distargs=(0, 360))
    sim.addInVar(name='Wind Speed [m/s]', dist=uniform, distargs=(0, 2))
    
    para_fail_dist = rv_discrete(name='para_fail_dist', values=([1, 2], [0.8, 0.2]))
    para_fail_nummap = {1:False, 2:True}
    sim.addInVar(name='Parachute Failure', dist=para_fail_dist, distargs=(), nummap=para_fail_nummap)

    sim.runSim()
    
    print(sim.runtime)
    
    sim.mcoutvars['Distance [m]'].addVarStat(stattype='gaussianP', statkwargs={'p':0.90, 'c':0.50})
    sim.mcoutvars['Distance [m]'].addVarStat(stattype='gaussianP', statkwargs={'p':0.10, 'c':0.50})
    #print(sim.mcoutvars['Landing Dist [m]'].stats())
    mc_plot(sim.mcoutvars['Time [s]'], sim.mcoutvars['Distance [m]'])
    #mc_plot(sim.mcoutvars['Time [s]'], sim.mcoutvars['|Velocity| [m/s]'])
    #mc_plot(sim.mcoutvars['Landing Dist [m]'])
    #mc_plot(sim.mcoutvars['Landing E [m]'], sim.mcoutvars['Landing N [m]'])
    #mc_plot(sim.mcoutvars['Time [s]'], sim.mcoutvars['Flight Stage'])    
    #mc_plot(sim.mcoutvars['Position [m]'])
    mc_plot(sim.mcoutvars['Easting [m]'], sim.mcoutvars['Northing [m]'], sim.mcoutvars['Altitude [m]'], title='Model Rocket Trajectory')
    #import matplotlib.pyplot as plt
    #plt.savefig('rocket_trajectory.png')
    mc_multi_plot(sim.mcoutvars['Landing Dist [m]'], sim.mcinvars['Wind Speed [m/s]'], title='Wind Speed vs Landing Distance')
    #plt.savefig('wind_vs_landing.png')
    
    return sim

if __name__ == '__main__':
    sim = rocket_example_run_script()
    