#!/usr/bin/env python3
import sys
import os

#
# * Calculates the density based off of Vs. Based on Nafe-Drake scaling relationship.
# *
# * @param vs The Vs value off which to scale.
# * @return Density, in g/m^3.
# */
def vs_2_density(vs):
  # Density scaling parameters
  p5 = -0.0024189659303912917
  p4 = 0.015600987888334450
  p3 = 0.051962399479341816
  p2 = -0.51231936640441489
  p1 = 1.2550758337054457
  p0 = 1.2948318548300342

  retVal = 0.0
  vs = vs / 1000.0
  retVal = p0 + p1 * vs + p2 * pow(vs, 2) + p3 * pow(vs, 3) + p4 * pow(vs, 4) + p5 * pow(vs, 5)
  retVal = retVal * 1000
  return retVal

# Density derived from Vp via Nafe-Drake curve, Brocher (2005) eqn 1. */
def vp_2_density(vp):
  # Convert m to km
  vp = vp * 0.001
  rho = vp * (1.6612 - vp * (0.4721 - vp * (0.0671 - vp * (0.0043 - vp * 0.000106))))
  if (rho < 1.0):
    rho = 1.0
  rho = rho * 1000.0;
  return rho
