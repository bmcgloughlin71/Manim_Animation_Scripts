from manim import *
import numpy as np
from Pattern_Func import *

class MatchedFiltering(Scene):
    def construct(self):
        # Define the axes with specific configurations
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 0.5],
            axis_config={"color": BLUE, "include_numbers": False}
        )
        
        # Add the axes to the scene
        self.add(axes)

        labels = axes.get_axis_labels(x_label="t", y_label=MathTex("h(t) \\sim 10^{-25}"))
        self.add(axes, labels)

        # Define fixed values for the static plot parameters
        f_static = 1        # Frequency 
        fdot_static = -0.01   # Frequency derivative
        alpha_static = 0.5  # Parameter alpha
        delta_static = 0.1  # Parameter delta
         
        # Define the sine wave function with Gaussian noise
        def sine_wave(t, f, fdot, alpha, delta):
            signal = a("H1", alpha, delta, t) * np.cos(2 * PI * (f * t + 0.5 * fdot * (t ** 2))) + b("H1", alpha, delta, t) * np.sin(2 * PI * (f * t + 0.5 * fdot * (t ** 2)))
            return signal
        
        def sine_wave_with_noise(t, f, fdot, alpha, delta):
            noise = np.random.normal(0, 0.1)  # Gaussian noise with mean 0 and std dev 0.1
            signal = (a("H1", alpha, delta, t) *
                      np.cos(2 * PI * (f * t + 0.5 * fdot * (t ** 2))) +
                      b("H1", alpha, delta, t) *
                      np.sin(2 * PI * (f * t + 0.5 * fdot * (t ** 2))))
            return signal + noise

        # Generate data points for the scatter plot
        t_values = np.linspace(0, 10, 100)
        points = [axes.coords_to_point(t, sine_wave_with_noise(t, f_static, fdot_static, alpha_static, delta_static)) for t in t_values]

        # Create the scatter plot
        scatter_plot = VGroup(*[Dot(point, color=YELLOW) for point in points])
        
        # Add the scatter plot to the scene
        self.add(scatter_plot)

        # Parameters for the three sine waves
        sine_wave_params = [
            (2, 0.1, 0.4, 0.15, WHITE, 6.5),  # First sine wave parameters and F value
            (1, -0.01, 0.5, 0.1, BLUE, 9),  # Second sine wave parameters and F value
            (3, -0.1, 0.6, 0.3, RED, 5)     # Third sine wave parameters and F value
        ]

        grid = NumberPlane(
            x_range=[0, 12, 1], y_range=[-2, 2, 0.5],
            background_line_style={"stroke_color": LIGHTER_GREY, "stroke_opacity": 0.3}
        )

        self.add(grid)

        for params in sine_wave_params:
            f, fdot, alpha, delta, color, F_value = params
            sine_wave_graph = axes.plot(
                lambda t: sine_wave(t, f, fdot, alpha, delta),
                color=color
            )

            # Create labels for each sine wave's parameters
            f_label = MathTex(f"f = {f:.2f}").set_color(color).scale(0.7)
            fdot_label = MathTex(f"\\dot{{f}} = {fdot:.2f}").set_color(color).scale(0.7)
            alpha_label = MathTex(f"\\alpha = {alpha:.2f}").set_color(color).scale(0.7)
            delta_label = MathTex(f"\\delta = {delta:.2f}").set_color(color).scale(0.7)

            # Group and position the labels
            param_labels = VGroup(f_label, fdot_label, alpha_label, delta_label).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UR)

            # Box around the parameter labels
            value_box = SurroundingRectangle(param_labels, color=color, buff=0.2)

            # Additional equation label at the bottom of the scene
            equation_label = MathTex(
                f"2\\mathcal{{F}}={F_value}"
            ).set_color(color).to_edge(DOWN, buff=0.3)

            # Box around the equation label
            equation_box = SurroundingRectangle(equation_label, color=color, buff=0.2)

            # Add sine wave graph, labels, and boxes to the scene
            self.add(sine_wave_graph, param_labels, value_box, equation_label, equation_box)
            self.play(Create(sine_wave_graph), run_time=5)
            self.wait(1)  # Add a pause to allow viewing the sine wave with its parameters
            
            # Remove the added elements from the scene
            self.remove(sine_wave_graph, param_labels, value_box, equation_label, equation_box)

# Run the scene
if __name__ == "__main__":
    from manim import config
    config.media_width = "75%"
    config.verbosity = "WARNING"
    scene = MatchedFiltering()
    scene.render()
