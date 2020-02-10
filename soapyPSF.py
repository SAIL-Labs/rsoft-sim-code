import soapy

sim = soapy.Sim("o_loop.yaml")
sim.aoinit()
sim.makeIMat()
sim.aoloop()
