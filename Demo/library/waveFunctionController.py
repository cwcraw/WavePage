from django.shortcuts import render
import json
import plotly
import plotly.express as px
from Demo.library.potentialEnum import PotentialEnum
from Demo.library.waveFunctionCalculator import WaveCalc


class WaveFunctionController:
    @staticmethod
    def view(request, potential):
        try:
            potential = PotentialEnum(potential.lower())
        except ValueError:
            return render(request, "potentialError.html", {"potential": potential})

        graphJSON, pot_plot = WaveFunctionController.__getPlots__(potential)
        text = WaveFunctionController.__getText__(potential)

        return render(
            request,
            "waveFunctionPage.html",
            {
                "graphJSON": graphJSON,
                "potential": potential.value,
                "text": text,
                "pot_plot": pot_plot,
            },
        )

    def __getPlots__(potential):
        output = []
        E_val, E_vec, V, x = WaveCalc(potential)

        energy_levels = range(0, 6, 1)
        for i in energy_levels:
            y = E_vec[:, i] ** 2 / max(E_vec[:, i] ** 2)
            output.append(
                json.dumps(
                    {
                        "x": list(x),
                        "y": list(y),
                        "type": "scatter",
                        "name": "Square of the Wave Function",
                        "mode": "lines+markers",
                        "color": "red",
                    },
                    cls=plotly.utils.PlotlyJSONEncoder,
                )
            )
            max_V = (1, max(V))[int(max(V) > 0)]
            # V = [x / (max(V), 1)[int(max(V)) == 0] for x in V]
            V = [x / max_V for x in V]
            pot_plot = json.dumps(
                {"x": list(x), "y": list(V), "type": "line", "name": "Potential"},
                cls=plotly.utils.PlotlyJSONEncoder,
            )

        return [output, pot_plot]

    def __getText__(potential):
        potential_info = {
            potential.STEP.value: {
                "name": "Step Potential",
                "text": "Sorry team I cannot, for the life of me, remember the boundary conditions at the step that lead to the behavior observed at high energy levels. Do note, however, that at lower energies we see the expected decay behavior, as the particle does not have enough energy to reside in the high potential step.",
            },
            potential.BARRIER.value: {
                "name": "Low Barrier Potential",
                "text": 'A finite barrier can demonstrate quantum tunnelling. We can see that in the region of the barrier the probibility density drops towards 0, but the particle can be found on both sides of the barrier. Increaseing the "height" of the barrier would lower the likelihood of tunneling until the particle is found on only oneside. Note that there are two degenerate states, representing the particle initialy being on either side of the barrier. Here we are displaying only non-degenerate states. See the high barrier case to gain an understanding of the degenerate cases.',
            },
            potential.HIGH_BARRIER.value: {
                "name": "High Barrier Potential",
                "text": "Here we have a higher barrier showing the degenerate states representing a particle isolated on either side.",
            },
            potential.MORSE.value: {
                "name": "Morse Potential",
                "text": "A Morse potential is a simple improvement on the harmonic oscillator. It is of the form V=De*(1-e^(-a*x))^2, where x (again) is the displacement from equlibrium, De is the 'well depth', and a controls the width of the well. As a model for a diatomic molecule, De can be thought of as the dissaciataion energy. The energy levels are quantized, with integer values starting from 0. However there is an upper bound to these numbers, representing a dissacosciated molecule.",
            },
            potential.HO.value: {
                "name": "Harmonic Oscillator",
                "text": "A harmonic oscillator potential is an idealized spring - the further you go from equilibrium, the stronger the restoring force is. This is represented in Hook's law, F=kx, where F is the force, k is the spring constant and x is the displacement from equilibrium. For our potential we are concerned with the potential energy, V = 1/2*k*x^2. For a quantum system the energy levels are proportional to n+1/2 where n is an integer value starting at 0. Harmonic oscilators are good for small displacements or small values of n. However, as you move further from equilibrium anharmonic components start to dominate.",
            },
            potential.OPEN.value: {
                "name": "Particle in a Box",
                "text": "A particle in a box is a standard starting point for studys of Quantum Mechanics. In a quantum system, a particle in a box can only have certain well defined energies, which limit the likelihood of the particle be measured at a given postion at any time. These probabilities take the form of a square of a sine function, with the requirement that the probability must be equal to 0 at either end of the box - that is, the particle can not exit the box. This second requirement means that the sine function must be of the form sin(nx), where n is a whole number. Although a simple model, it can be used to describe some real world situations, like a conjugated polyene in chemistry. A conjugated polyene is a long straight molecule whose structure allows electrons to traverse its length",
            },
        }

        return {
            "outro_text": "This widget was created as a way to explore Python, particularly numpy, matplotlib and tkinter. It is an exploration of the classic 'particle in a box' problem most students encounter in their first semester of Quantum Mechanics or Physical Chemistry. Please feel free to contribute to my explanatory text and make suggestions on how to improve this code.",
            "potential_info": potential_info[potential.value],
        }
